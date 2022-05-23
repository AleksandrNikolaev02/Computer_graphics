from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import random as rd

def box_blur(img, r):
    new_img = img.copy()
    width, height = img.size
    div = pow(2*r+1, 2)
    for x in range(100, width - 100):
        for y in range(100, height - 100):
            Sum_R = 0
            Sum_G = 0
            Sum_B = 0
            for i in range(x-r, x+r+1):
                for j in range(y-r, y+r+1):
                    Sum_R = Sum_R + img.getpixel((i, j))[0]
                    Sum_G = Sum_G + img.getpixel((i, j))[1]
                    Sum_B = Sum_B + img.getpixel((i, j))[2]
            Sum_R = Sum_R // div
            Sum_G = Sum_G // div
            Sum_B = Sum_B // div
            new_img.putpixel((x, y), (Sum_R, Sum_G, Sum_B))
    plt.imshow(new_img)
    plt.show()

def glass_effect():
    image = Image.open('картинка.jpg')
    width, height = image.size
    max_random = 15
    width = width - max_random
    height = height - max_random
    result_image = Image.new('RGB', (width, height))
    for x in range(width - max_random):
        for y in range(height - max_random):
            RGB = image.getpixel((x + round(np.random.randint(0, max_random) - 0.5), y + round(np.random.randint(0, max_random) - 0.5)))
            result_image.putpixel((x, y), RGB)
    plt.imshow(result_image)
    plt.show()

if __name__ == '__main__':
    glass_effect()