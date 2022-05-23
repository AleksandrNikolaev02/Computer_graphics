from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def histogram_count(img):
    width, height = img.size
    array = np.zeros(width * height)
    count = 0
    for i in range(width):
        for j in range(height):
            RGB = img.getpixel((i, j))
            R, G, B = RGB
            lum = 0.3 * R + 0.59 * G + 0.11 * B
            array[count] = round(lum)
            count += 1
    return array


def histogram_visual(img):
    mas = histogram_count(img)
    plt.hist(mas, color='black', bins = 255)
    plt.title('Гистограмма изображения')
    plt.xlabel('Яркость тонов')
    plt.ylabel('Число пикселей')
    plt.show()


def gamma_correction(img):
    row = img.size[0]
    col = img.size[1]
    gamma = 3
    result_img = Image.new("L", (row, col))
    for x in range(1, row):
        for y in range(1, col):
            value = pow(img.getpixel((x, y))[0]/255, gamma) * 255
            if value >= 255:
                value = 255
            result_img.putpixel((x, y), int(value))
    result_img = result_img.convert('RGB')
    plt.imshow(result_img)
    plt.show()

if __name__ == '__main__':
    image1 = Image.open('картинка.jpg').convert('LA')
    plt.imshow(image1)
    plt.show()
    image2 = Image.open('картинка.jpg').convert('RGB')
    gamma_correction(image1)
    histogram_visual(image2)