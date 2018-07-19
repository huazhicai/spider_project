import os
from PIL import ImageFilter
from pytesseract import pytesseract
# import pytesseract
from PIL import Image


def resize(im):
    w, h = im.size
    im.resize((2 * w, 2 * h))
    return pytesseract.image_to_string(im)


def thumbnail(im):
    w, h = im.size
    im.thumbnail((2 * w, 2 * h))
    return pytesseract.image_to_string(im)


def detail(image):
    im = image.filter(ImageFilter.DETAIL)
    return pytesseract.image_to_string(im)


def main():
    for img_file in os.listdir('F:\Project\spider_project\phone58\phone58\spiders\images'):
        # img_file = os.path.abspath(img_file)
        text1 = pytesseract.image_to_string(Image.open('F:\Project\spider_project\phone58\phone58\spiders\images\%s' % img_file))
        im = Image.open('F:\Project\spider_project\phone58\phone58\spiders\images\%s' % img_file).convert("L")
        text2 = resize(im)
        text3 = thumbnail(im)
        text4 = detail(im)
        print(text1, text2, text3, text4)


if __name__ == '__main__':
    main()
