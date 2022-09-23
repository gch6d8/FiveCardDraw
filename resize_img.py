from PIL import Image
import PIL
import os

f = 'visualAssets/card_fronts'

for file in os.listdir(f):
    f_img = f+"/"+file
    print(f_img)
    img = Image.open(f_img)
    img.thumbnail((100,140))
    print(img.size)
    img.save(f_img)

#image = Image.open('visualAssets/card_fronts/ace_club.png')

#image.thumbnail((100,140))

#image.save('visualAssets/card_fronts/ace_club.png')

