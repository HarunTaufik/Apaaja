import signal
import sys
import os
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMediaRequest
import cv2
import numpy as np

api_id = '25450488'
api_hash = 'acbb7918c2adedd458de3b64c4bac34f'
phone_number = '+6285944608131'
bot_username = '@Zfty_bot'  # Ganti dengan username bot Anda

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

        # Deteksi warna oranye
        result_path = detect_orange_color(photo_path)

        # Kirim foto hasil deteksi warna kembali ke bot
        await client.send_file(bot_username, result_path)
        print(f"Hasil deteksi warna oranye dikirim ke bot: {result_path}")

#def detect_orange_color(image_path):
#    image = cv2.imread(image_path)
#    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#    lower_orange = np.array([10, 100, 100])
#    upper_orange = np.array([25, 255, 255])
#    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
#    result = cv2.bitwise_and(image, image, mask=mask)
#    result_path = os.path.join(PHOTO_SAVE_PATH, 'result_orange_detected.jpg')
#    cv2.imwrite(result_path, result)
#    return result_path

def detect_orange_color(image_path):
    # Baca gambar
    image = cv2.imread(image_path)
    
    # Konversi gambar dari BGR ke HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Definisikan rentang warna oranye dalam ruang warna HSV
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])
    
    # Buat mask untuk mendeteksi warna oranye
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    
    # Cari kontur pada area yang terdeteksi sebagai warna oranye
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Gambar kotak di sekitar kontur yang ditemukan
    for contour in contours:
        # Dapatkan bounding box untuk setiap kontur
        x, y, w, h = cv2.boundingRect(contour)
        
        # Gambar kotak (rectangle) di sekitar area oranye
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Warna hijau dengan ketebalan 2
    
    # Simpan gambar hasil dengan kotak
    result_path = os.path.join(PHOTO_SAVE_PATH, 'result_orange_with_boxes.jpg')
    cv2.imwrite(result_path, image)
    
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
