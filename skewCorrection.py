import os
import cv2
import numpy as np
from PIL import Image
import pytesseract


def deleteFiles(path):
    # Check if the file exists before attempting to delete it
    dir_list = os.listdir(path)
    for file in dir_list:
        os.remove(path+"/"+file)
        print(f"The file {file} has been deleted.")

def correct_skew(image, delta = 0.1, limit = 5):
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(gray, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # draw the correction angle on the image so we can validate it
    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))
    #cv2.imshow("Input", image)
    #cv2.imshow("Rotated", rotated)
    return angle,rotated

if __name__ == '__main__':
    deleteFiles('Rotated')
    path = "Faturalar"
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :")
    # prints all files
    # print(dir_list)

    for files in dir_list:
        f = files.split(".")
        if f[-1] == "jpg":
            jpegFile = "Faturalar/" + f[0] + ".jpg"
            rotatedJpegFile = "Rotated/" + f[0] + "_r.jpg"
            txtFile = "Text/" + f[0] + ".txt"
            print("[INFO] reading image file {} ".format(jpegFile))
            image = cv2.imread(jpegFile)
            angle, corrected = correct_skew(image)
            print('Skew angle:', angle)
            cv2.imwrite(rotatedJpegFile, corrected)

    deleteFiles('Text')
    path = "Rotated"
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :")
    # prints all files
    # print(dir_list)

    for files in dir_list:
        f = files.split(".")
        if f[-1] == "jpg":
            jpegFile = path + "/" + f[0] + ".jpg"
            txtFile = "Text/" + f[0] + ".txt"
            print("[INFO] reading image file {} ".format(jpegFile))
            image = Image.open(jpegFile)
            txt = open(txtFile, "w")
            txt.write(pytesseract.image_to_string(image=image, lang="tur"))
            txt.close()


