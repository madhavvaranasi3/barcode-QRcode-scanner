import cv2
from pyzbar import pyzbar
import time

def read_barcode(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        print(f"{barcode.type} : {barcode_info}")
        time.sleep(1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (8, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 0.5, (255, 255, 255), 1)

        write_to_file(barcode_info)
    return frame

def write_to_file(barcode_info):
    try:
        with open("barcode_result.txt", mode='a') as file:
            file.write(f"Recognized Barcode: {barcode_info}\n")
    except Exception as e:
        print(f"Failed to write to file: {e}")

def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open video stream.")
        return
    
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            frame = read_barcode(frame)
            cv2.imshow("Barcode/QR code reader", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        camera.release()
        cv2.destroyAllWindows()

if name == 'main':
    main()
