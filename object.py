import cv2
import requests

# Menggunakan webcam (biasanya index 0 untuk webcam pertama)
cap = cv2.VideoCapture(0)

# Inisialisasi detektor HOG
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

if not cap.isOpened():
    print("Tidak dapat mengakses kamera.")
else:
    while True:
        # Membaca frame dari webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Tidak dapat membaca frame.")
            break
        
        # Memutar frame 180 derajat
        frame_rotated = cv2.rotate(frame, cv2.ROTATE_180)

        # Mengubah ukuran frame untuk mempercepat deteksi
        frame_resized = cv2.resize(frame_rotated, (640, 480))

        # Deteksi orang
        boxes, weights = hog.detectMultiScale(frame_resized, winStride=(8, 8))

        # Menggambar kotak di sekitar orang yang terdeteksi
        people_detected = len(boxes) > 0
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Menampilkan frame
        cv2.imshow('Deteksi Orang', frame_resized)

        # Kirim permintaan HTTP berdasarkan hasil deteksi
        if people_detected:
            requests.get('http://10.2.3.193/2')  # Jika ada orang
        else:
            requests.get('http://10.2.3.193/1')  # Jika tidak ada orang

        # Keluar dari loop jika tombol 'q' ditekan
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Melepaskan objek dan menutup jendela
cap.release()
cv2.destroyAllWindows()
