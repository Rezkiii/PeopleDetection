import cv2
import requests
from datetime import datetime

# Inisialisasi deteksi wajah dengan Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Menggunakan kamera default
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Membuat jendela dengan ukuran yang dapat disesuaikan
cv2.namedWindow('Kamera', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Kamera', 800, 600)  # Mengubah ukuran jendela

while True:
    # Membaca frame dari kamera
    ret, frame = cap.read()
    if not ret:
        break

    # Mengubah frame ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Mendeteksi wajah
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Menjalankan URL tergantung pada deteksi wajah
    if len(faces) > 0:
        print("Wajah terdeteksi!")

        # Mengambil waktu saat ini
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Mengirim data ke API dengan IP yang benar dan port 5000
        payload = {
            'timestamp': current_time,
            'detected_people': "tidak_dikenali"
        }
        requests.post("http://10.2.3.161:5000/data", json=payload)

        # Mengambil URL untuk perangkat lain
        requests.get("http://10.2.3.193/1")

        # Menggambar bounding box untuk setiap wajah yang terdeteksi
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        print("Tidak ada wajah terdeteksi.")
        # Mengambil URL untuk perangkat lain
        requests.get("http://10.2.3.193/2")

    # Menampilkan frame
    cv2.imshow('Kamera', frame)

    # Keluar jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan kamera dan menutup jendela
cap.release()
cv2.destroyAllWindows()
