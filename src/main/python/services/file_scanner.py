import os
import imghdr
from PIL import Image


# TODO Class ImageScanner?

def find_all_images_in(basepath):
    result = []
    # TODO check if this adds things that are on another drive.
    for root, dirs, files in os.walk(basepath):
        for name in files:
            file_path = os.path.join(root, name)
            file_type = imghdr.what(file_path)
            if file_type:
                size_in_bytes = os.path.getsize(file_path)
                size_in_mb = size_in_bytes / (1024 * 1024)
                path = os.path.normcase(file_path)
                path = os.path.normpath(path)
                path = os.path.abspath(path)
                result.append(
                    {"path": os.path.normpath(path),
                     "type": file_type,
                     "file_size": "{:.2f}".format(size_in_mb)})

    # for name in dirs:
    # print("Directory: " + os.path.join(root, name))
    return result
