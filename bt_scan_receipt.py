# import the necessary packages
#from imutils.perspective import four_point_transform
import pytesseract
import argparse
import imutils
import cv2
import re
import os
from PIL import Image
import json

def deleteFiles(path):
    # Check if the file exists before attempting to delete it
    dir_list = os.listdir(path)
    for file in dir_list:
        os.remove(path+"/"+file)
        print(f"The file {file} has been deleted.")

def readReceipts(srcPath, trgtPath):
    dir_list = os.listdir(srcPath)
    for receiptFile in dir_list:
        f = receiptFile.split(".")
        if f[-1] == "jpg":
            jpegFile = srcPath + "/" + f[0] + ".jpg"
            txtFile = trgtPath + "/" + f[0] + ".txt"
            print("[INFO] reading image file {} ".format(jpegFile))
            receipt = cv2.imread(jpegFile)
            options = "--psm 4"
            receiptTxt = pytesseract.image_to_string(
                image=cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
                lang="tur",
                config=options)
            txt = open(txtFile, "w")
            txt.write(receiptTxt)
            txt.close()

def extractSupplierName(receiptTxt):
    for row in receiptTxt.split("\n"):
        supplierNamePattern = r'([0-9]+\.[0-9]+)'
        if re.search(supplierNamePattern, row) is not None:
            return row
    return "bilemedim"

def extractSupplierVKN(receiptTxt):
    for row in receiptTxt.split("\n"):
        supplierVKNPattern = r'([0-9]+\.[0-9]+)'
        if re.search(supplierVKNPattern, row) is not None:
            return row
    return "bilemedim"

def extractTaxAmount(receiptTxt):
    for row in receiptTxt.split("\n"):
        taxAmountPattern = r'([0-9]+\.[0-9]+)'
        if re.search(taxAmountPattern, row) is not None:
            return row
    return "bilemedim"

def extractTotalAmount(receiptTxt):
    for row in receiptTxt.split("\n"):
        totalAmountPattern = r'([0-9]+\.[0-9]+)'
        if re.search(totalAmountPattern, row) is not None:
            return row
    return "bilemedim"

def extractCurrencyCode(receiptTxt):
    for row in receiptTxt.split("\n"):
        currencyCodePattern = r'([0-9]+\.[0-9]+)'
        if re.search(currencyCodePattern, row) is not None:
            return row
    return "bilemedim"

def extractAttributes(txtFile):
    txt = open(txtFile, "r")
    receiptTxt = txt.read()
    txt.close()
    value = {
        "supplierName": extractSupplierName(receiptTxt),
        "supplierVKN": extractSupplierVKN(receiptTxt),
        "taxAmount": extractTaxAmount(receiptTxt),
        "totalAmount": extractTotalAmount(receiptTxt),
        "currencyCode": extractCurrencyCode(receiptTxt)
    }
    return json.dumps(value)

def createJsonFiles(srcPath, trgtPath):
    dir_list = os.listdir(srcPath)
    for receiptFile in dir_list:
        f = receiptFile.split(".")
        if f[-1] == "txt":
            txtFile = srcPath + "/" + f[0] + ".txt"
            jsonFile = trgtPath + "/" + f[0] + ".json"
            f = open(jsonFile, "w")
            f.write(extractAttributes(txtFile))
            f.close()

if __name__ == '__main__':
    #deleteFiles('Text')
    deleteFiles('Json')
    #readReceipts('Faturalar','Text')
    createJsonFiles('Text','Json')


