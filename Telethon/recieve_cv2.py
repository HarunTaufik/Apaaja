import cv2
import numpy as np
import os
from telethon import TelegramClient, events

# Ganti dengan API ID dan API Hash dari my.telegram.org
api_id = '25450488'
api_hash = 'acbb7918c2adedd458de3b64c4bac34f'

# Ganti dengan nomor telepon Anda yang terhubung dengan Telegram
phone_number = '+6285944608131'

# Inisialisasi client Telethon
client = TelegramClient('session_name', api_id, api_hash)

# Path folder untuk menyimpan foto yang diterima
PHOTO_SAVE_PATH = './'

# Buat folder jika belum ada
if not os.path.exists(PHOTO_SAVE_PATH):
    os.makedirs(PHOTO_SAVE_PATH)

@client.on(events.NewMessage(from_users='@Zfty_bot'))  # Ganti dengan username bot
async def handle_new_message(event):
    if event.photo:  # Mengecek apakah pesan berisi foto
        print("Foto diterima dari bot!")

        # Mendownload dan menyimpan foto
        photo_path = await event.download_media(file=PHOTO_SAVE_PATH)
        print(f"Foto berhasil disimpan di: {photo_path}")

        # Setelah foto diunduh, deteksi warna oranye
        detect_orange_color(photo_path)
    else:
        print("Pesan bukan foto.")

def detect_orange_color(image_path):
    # Membaca gambar
    image = cv2.imread(image_path)

    # Konversi gambar ke dalam format HSV (Hue, Saturation, Value)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definisikan rentang warna oranye dalam format HSV
    lower_orange = np.array([10, 100, 100])   # Nilai bawah untuk oranye
    upper_orange = np.array([25, 255, 255])   # Nilai atas untuk oranye

    # Membuat mask untuk mendeteksi warna oranye
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # Terapkan mask ke gambar asli
    result = cv2.bitwise_and(image, image, mask=mask)

    # Tampilkan hasil deteksi
    cv2.imshow('Detected Orange Color', result)
    cv2.waitKey(0)  # Tekan tombol untuk menutup jendela gambar
    cv2.destroyAllWindows()

    # Simpan hasil deteksi
    result_path = os.path.join(PHOTO_SAVE_PATH, 'result_orange_detected.jpg')
    cv2.imwrite(result_path, result)
    print(f"Hasil deteksi warna oranye disimpan di: {result_path}")

async def main():
    # Mulai client
    await client.start(phone_number)
    
    print("Menunggu pesan dari bot...")
    await client.run_until_disconnected()

# Menjalankan client
with client:
    client.loop.run_until_complete(main())
