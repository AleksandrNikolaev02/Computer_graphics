from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

im =Image.open('картинка.jpg').convert('LA')
w,h = im.size
im2 = Image.new('LA', (w,h))
kernelx = np.array([[1, 0], [0, -1]], dtype=int)
kernely = np.array([[0, 1], [-1, 0]], dtype=int)
for x in range(w-1):
    for y in range(h-1):
        sub =[[im.getpixel((x, y))[0], im.getpixel((x, y+1))[0]],[im.getpixel((x+1, y))[0], im.getpixel((x+1, y+1))[0]]]
        sub = np.array(sub)
        var_x =sum(sum(sub * kernelx))
        var_y = sum(sum(sub * kernely))

        var = abs(var_x) + abs(var_y)

        im2.putpixel((x,y), (var, 255))

plt.imshow(im2)
plt.show()