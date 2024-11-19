import signal
import sys
import os
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMediaRequest
import cv2
import numpy as np
from PIL import Image

api_id = '25450488'
api_hash = 'acbb7918c2adedd458de3b64c4bac34f'
phone_number = '+6285944608131'
bot_username = '@Zfty_bot'  # Ganti dengan username bot Anda
overlay_png_path = '../Api.png'  # Ganti dengan path gambar PNG yang akan di-overlay

client = TelegramClient('session_name', api_id, api_hash)
PHOTO_SAVE_PATH = './downloaded_photos/'

if not os.path.exists(PHOTO_SAVE_PATH):
    os.makedirs(PHOTO_SAVE_PATH)

@client.on(events.NewMessage(from_users='@Zfty_bot'))
async def handle_new_message(event):
    if event.photo:
        print("Foto diterima dari bot!")
        photo_path = await event.download_media(file=PHOTO_SAVE_PATH)
        print(f"Foto berhasil disimpan di: {photo_path}")

        # Deteksi warna oranye dan overlay PNG
        result_path = detect_orange_color_and_overlay(photo_path, overlay_png_path)

        # Kirim foto hasil deteksi warna kembali ke bot
        await client.send_file(bot_username, result_path)
        print(f"Hasil deteksi warna oranye dikirim ke bot: {result_path}")

def detect_orange_color_and_overlay(image_path, overlay_png_path):
    # Baca gambar asli
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Rentang warna oranye
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])
    
    # Mask untuk warna oranye
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    
    # Cari kontur untuk area warna oranye
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Jika tidak ada deteksi warna oranye, kembalikan gambar asli
    if len(contours) == 0:
        result_path = os.path.join(PHOTO_SAVE_PATH, 'no_orange_detected.jpg')
        cv2.imwrite(result_path, image)
        return result_path

    # Baca gambar overlay (PNG)
    overlay = Image.open(overlay_png_path).convert("RGBA")
    
    # Inisialisasi variabel untuk bounding box terbesar
    largest_area = 0
    largest_rect = None

    # Cari bounding box terbesar dari deteksi warna oranye
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > largest_area:
            largest_area = area
            largest_rect = (x, y, w, h)

    # Ambil bounding box terbesar
    if largest_rect:
        x, y, w, h = largest_rect
        
        # Cari titik tengah dari bounding box terbesar
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Ambil ukuran asli overlay
        overlay_width, overlay_height = overlay.size
        
        # Tentukan skala untuk resize (misalnya berdasarkan lebar dari bounding box)
        scale = w / overlay_width  # Skala mengikuti lebar
        
        # Hitung ukuran baru dengan skala yang sama untuk kedua dimensi
        new_width = int(overlay_width * scale * 4)
        new_height = int(overlay_height * scale * 4)

        # Resize gambar PNG (overlay) agar sesuai dengan bounding box deteksi
        overlay_resized = overlay.resize((new_width, new_height), Image.ANTIALIAS)
        
        # Konversi gambar OpenCV ke format PIL untuk penumpukan
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Hitung posisi kiri atas (top-left) untuk menempatkan overlay di tengah bounding box
        top_left_x = center_x - new_width // 2
        top_left_y = center_y - new_height // 2
        
        # Gabungkan overlay dengan gambar asli
        image_pil.paste(overlay_resized, (top_left_x, top_left_y), overlay_resized)
        
        # Konversi kembali gambar hasil ke format OpenCV
        result_image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        
        # Gambar kotak hijau di sekitar area oranye terbesar
        #cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Simpan hasil gambar yang sudah ditumpuk overlay
        result_path = os.path.join(PHOTO_SAVE_PATH, 'result_with_overlay_and_boxes.jpg')
        cv2.imwrite(result_path, result_image)
        
        return result_path

async def main():
    await client.start(phone_number)
    print("Menunggu pesan dari bot...")
    await client.run_until_disconnected()

def graceful_exit(signal, frame):
    print("Program dihentikan secara manual. Menutup koneksi...")
    client.disconnect()  # Memutuskan koneksi Telethon
    sys.exit(0)  # Keluar dari program dengan status sukses

# Menangkap sinyal Ctrl+C dan memanggil fungsi graceful_exit
signal.signal(signal.SIGINT, graceful_exit)

with client:
    client.loop.run_until_complete(main())
