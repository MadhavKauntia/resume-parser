import pdf2image
from pdf2image import convert_from_path

def pdfToImages(filename):
    pages = convert_from_path(filename, 500)

    i = 1
    for page in pages:
        page.save('pages/' + str(i) + '.jpg', 'JPEG')
        i = i + 1