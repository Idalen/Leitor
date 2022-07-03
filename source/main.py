###
### MAIN FILE
###
### Author: Daniel Martins Vieira

from leitor import Leitor

dir = '../data/print_only_images/mask'
#path = '../data/photo_only_images/8.jpg'

leitor = Leitor()
leitor.load(dir)
image = leitor.open()

print(image.max())
print(image.min())
