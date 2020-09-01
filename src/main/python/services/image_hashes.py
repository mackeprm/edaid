from PIL import Image
from functools import partial
import imagehash
from src.main.python.services.file_scanner import *

hashfuncs = [
    ('ahash', imagehash.average_hash),
    ('phash', imagehash.phash),
    ('dhash', imagehash.dhash),
    ('whash-haar', imagehash.whash),
    ('whash-db4', lambda img: imagehash.whash(img, mode='db4')),
    ('colorhash', imagehash.colorhash),
    ('phash_large', partial(imagehash.phash, hash_size=32)),
]


def image_loader(hashfunc):
    def function(path):
        image = Image.open(path)
        return hashfunc(image)

    return function




hashfuncopeners = [(name, image_loader(func)) for name, func in hashfuncs]

# https://github.com/philipbl/duplicate-images
if __name__ == '__main__':
    path = "../../../../test/images"
    image_files = find_all_images_in(path)
    tableformatter = '{0:<40s}|{1[0]:<16s}|{1[1]:<16s}|{1[2]:<16s}|{1[3]:<16s}|{1[4]:<49s}|{1[5]:<16s}|{1[6]}'

    # TODO add path to image_hashes?
    # with sqlite3.connect('imageHashes.db') as connection:
    #   db.init(connection)
    print(tableformatter.format('Filename', [t[0] for t in hashfuncs]))
    for path in [image_file['path'] for image_file in image_files]:
        with Image.open(path) as image:
            hashes = [str(hashfuncopener(path)) for name, hashfuncopener in hashfuncopeners]
            #:[[<fill>]<align>][<sign>][#][0][<width>][<group>][.<prec>][<type>]
            # Header
            print(tableformatter.format(path, hashes))
            # db.add_info(connection, {"path": path, "phash_large": hashes[6]})
            print(path, ' '.join(hashes))
print("Shutting Down")
