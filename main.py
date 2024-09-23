from pytesseract import Output
from PIL import Image
from PIL import ImageOps
import pytesseract
import cv2
import os

# Get the list of all files and directories
path = "Faturalar"
dir_list = os.listdir(path)
print("Files and directories in '", path, "' :")
# prints all files
#print(dir_list)

for files in dir_list:
	f =files.split(".")
	if f[-1] == "jpg":
		jpegFile="Faturalar/"+f[0]+".jpg"
		decolorJpegFile="Rotated/"+f[0]+"_b.jpg"
		rotatedJpegFile="Rotated/"+f[0]+"_r.jpg"
		txtFile="Text/"+f[0]+".txt"
		print("[INFO] reading image file {} ".format(jpegFile))
		image = cv2.imread(jpegFile)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		a,b=cv2.decolor(image)
		results = pytesseract.image_to_osd(image=rgb, output_type=Output.DICT)
		print(results)
		print("[INFO] rotating {} degrees image file  ".format(results["orientation"]))
		print("[INFO] creating text file {} ".format(txtFile))
		rotatedImage=Image.open(jpegFile).rotate(angle=results["orientation"])
		c=ImageOps.grayscale(rotatedImage)
		c.save(decolorJpegFile)
		rotatedImage.save(rotatedJpegFile)
		txt = open(txtFile, "w")
		txt.write(pytesseract.image_to_string(image=c,lang="tur"))
		txt.close()


#print("[INFO] rotate by {} degrees to correct".format(results["rotate"]))

#print(results)
#print("[INFO] detected orientation: {}".format(
#	results["orientation"]))
#print("[INFO] detected script: {}".format(results["script"]))



#print(pytesseract.image_to_string(image=Image.open('Faturalar/20240905_091443.jpg').rotate(angle=-90),lang="tur"))
