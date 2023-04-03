import cv2


# Obtener información sobre las cámaras disponibles
def contar_camaras():
    num_cameras = 0
    while True:
        try:
            cap = cv2.VideoCapture(num_cameras)
            if not cap.read()[0]:
                break
        except Exception:
            print("si")
            break

        num_cameras += 1
        cap.release()
    return num_cameras


num_cameras = contar_camaras()
# Imprimir el número de cámaras disponibles
print(f"Se encontraron {num_cameras} cámaras disponibles.")
