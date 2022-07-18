###
### MAIN FILE
###
### Author: Daniel Martins Vieira

from leitor import Leitor

#path = '../data/print_only_images/raw/1.jpg'
path = '../data/photo_only_images/8.jpg'

leitor = Leitor()
leitor.extract(path, save='../docs/last_output/')

