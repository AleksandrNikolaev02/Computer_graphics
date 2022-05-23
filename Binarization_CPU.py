from PIL import Image
import matplotlib.pyplot as plt

def Binarization(img,threshold):
    for i in range(img.width):
        for j in range(img.height):
            RGB = img.getpixel((i, j))
            R = RGB[0]
            G = RGB[1]
            B = RGB[2]
            Y = 0.299 * R + 0.587 * G + 0.114 * B
            if Y>threshold: img.putpixel((i,j),(255,255,255))
            else: img.putpixel((i,j),(0,0,0))
    return img

if __name__ == '__main__':
    image = Image.open('картинка.jpg')
    image1 = Binarization(image, 127)
    plt.imshow(image1)
    plt.show()