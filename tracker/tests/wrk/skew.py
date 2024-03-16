import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import pytesseract
from imutils import rotate_bound
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def deskew_image(image_path):
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    # Threshold the image to binary
    _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Invert the image
    img_bin = 255 - img_bin

    # Define a rectangular structuring element
    kernel_length = np.array(img).shape[1] // 80
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

    # Apply morphological operations
    img_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=3)
    img_temp2 = cv2.dilate(img_temp1, vertical_kernel, iterations=3)
    cv2.imwrite("img_temp2.jpg", img_temp2)

    # Find contours in the image
    contours, _ = cv2.findContours(img_temp2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through each contour and find the bounding rectangle for each one
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Rotate the image back to straight
        if w > h:
            img = cv2.transpose(img)
            img = cv2.flip(img, flipCode=1)

    # Save the straightened image
    cv2.imwrite("straightened.jpg", img)

    return img

# Example usage:
current_directory = Path(__file__).resolve().parent
input_image_path = current_directory / 'xxx.jpg'


deskewed_image = deskew_image(input_image_path)

# Save the deskewed image
cv2.imwrite('deskewed_image.png', deskewed_image)
