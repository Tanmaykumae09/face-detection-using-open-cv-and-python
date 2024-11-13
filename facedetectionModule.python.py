import cv2
from cvzone.FaceDetectionModule import FaceDetector
import serial
import time

cap = cv2.VideoCapture(0)
detector = FaceDetector()

# Initialize serial connection
arduino = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)  # Wait for connection to establish

print("Arduino connected successfully.")

while True:
    success, img = cap.read()
    if not success:
        break

    img, bBoxes = detector.findFaces(img)

    try:
        if bBoxes:
            arduino.write(b'1')
            print("Sending '1' to Arduino - Face detected")
        else:
            arduino.write(b'0')
            print("Sending '0' to Arduino - No face detected")
    except serial.SerialException as e:
        print(f"Error sending data: {e}")
        break

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.5)  # Adjust delay if needed

cap.release()
cv2.destroyAllWindows()
arduino.close()
