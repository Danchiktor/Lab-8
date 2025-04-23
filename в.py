import cv2
import numpy as np

#1

image = cv2.imread('variant-5.jpg')

#шум
def add_noise(image):
    mean = 0
    sigma = 25
    noisy = np.random.normal(mean, sigma, image.shape).astype('uint8')
    noisy_image = cv2.add(image, noisy)
    return noisy_image

noisy_image = add_noise(image)

#сохранение и вывод
cv2.imwrite('noisy_image.jpg', noisy_image)
cv2.imshow('Noisy Image', noisy_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



#2,3


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

#камера
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #метка
    corners, ids, _ = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if ids is not None:
        center_x = int(np.mean(corners[0][0][:, 0]))
        center_y = int(np.mean(corners[0][0][:, 1]))

        #область
        height, width = frame.shape[:2]
        left_top = (0, 0, 50, 50)  # x1, y1, x2, y2
        right_bottom = (width - 50, height - 50, width, height)

        if (left_top[0] <= center_x < left_top[2]) and (left_top[1] <= center_y < left_top[3]):
            color = (255, 0, 0)  # Синий (BGR)
        elif (right_bottom[0] <= center_x < right_bottom[2]) and (right_bottom[1] <= center_y < right_bottom[3]):
            color = (0, 0, 255)  # Красный
        else:
            color = (0, 255, 0)  # Зеленый

        #контур метки
        cv2.aruco.drawDetectedMarkers(frame, corners, ids, color)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()