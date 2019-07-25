import cv2
import numpy as np
import imutils
import pytesseract
import pdf_to_image
import os
import time
import shutil

def isloate_text(filename):
    os.mkdir('pages')
    path = 'input/' + filename
    if filename[-3:] == 'pdf' or filename[-3:] == 'PDF':
        pdf_to_image.pdfToImages(path)
    else:
        img = cv2.imread(path)
        cv2.imwrite('pages/' + filename, img)
    i = 1
    for page in os.listdir('pages/'):
        path = 'pages/' + page
        rgb = cv2.imread(path)
        rgb = imutils.resize(rgb, width = int(rgb.shape[1]/4))
        small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        _, bw = cv2.threshold(small, 0.0, 255.0, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
        connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

        contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        with open('headers.txt') as f:
            lines = f.read().upper().splitlines()

        header_cords = []

        for idx in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[idx])
            cv2.rectangle(rgb, (x, y, x+w, y+h), (0, 0, 255), 2)
            try:
                cropped = rgb[y-5:y+h+5, x-5:x+w+5]
                text = pytesseract.image_to_string(cropped)
            except:
                continue
            text = text.lower()
            print(text)
            if text in lines or text[:-1] in lines:
                if text[len(text) - 1] != '.':
                    header_cords.append([x, y, x+w, y+h])
        cv2.imwrite('result/' + filename[:-4] + '-' + str(i) + '.jpg', rgb)
        i = i + 1
    shutil.rmtree('./pages/')
    return header_cords

total = 0
count = 0
for each in os.listdir('input/'):
    start = time.time()
    print('Working on: ' + each)
    isloate_text(each)
    total_time = time.time() - start
    print('Time taken: ' + str(total_time) + ' seconds')
    total = total + total_time
    count = count + 1
print('Total time taken: ' + str(total) + ' seconds')
print('Average time taken: ' + str(total/count) + ' seconds')