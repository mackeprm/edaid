from PyQt5 import QtGui, QtCore, QtWidgets
import os

from anytree import RenderTree

from utils.file_prefix_tree import FilePrefixTree


def recursively_add_tree_widgets(current_directory, parent_widget):
    path_item = [QtGui.QStandardItem(current_directory.name), QtGui.QStandardItem(str(current_directory.files))]
    parent_widget[0].appendRow(path_item)
    for child in current_directory.children:
        recursively_add_tree_widgets(child, path_item)


# TODO implement viewmodel functions
class FileTreeModel(QtGui.QStandardItemModel):
    FOLDER_NAME, FOUND_IMAGES = range(2)

    # TODO remove
    def reset_paths(self):
        rootItem = self.invisibleRootItem()

        # Get all paths that are existing in the app.
        paths = self.image_repository.get_all_paths()
        if paths:
            common_prefix = os.path.commonpath(paths) + os.path.sep
            # TODO this is still broken (im not sure why)
            # Input
            # e:\\
            # ['e:\\projects\\python\\lothren\\test\\images\\a-duplicate.jpg', 'e:\\projects\\python\\lothren\\test\\images\\a-resized.jpg', 'e:\\projects\\python\\lothren\\test\\images\\a.bmp', 'e:\\projects\\python\\lothren\\test\\images\\a.gif', 'e:\\projects\\python\\lothren\\test\\images\\a.jpg', 'e:\\projects\\python\\lothren\\test\\images\\a.png', 'e:\\projects\\python\\lothren\\test\\images\\b.jpg', 'e:\\projects\\python\\lothren\\test\\images\\öäü.jpg', 'e:\\projects\\python\\lothren\\test\\images\\dirtest\\a.jpg', 'e:\\pictures\\tmp\\img_20200522_142802.jpg', 'e:\\pictures\\tmp\\img_20200522_191209.jpg', 'e:\\pictures\\tmp\\img_20200522_191256.jpg', 'e:\\pictures\\tmp\\img_20200522_192324.jpg', 'e:\\pictures\\tmp\\img_20200522_194323.jpg', 'e:\\pictures\\tmp\\img_20200522_201351.jpg', 'e:\\pictures\\tmp\\img_20200522_202724.jpg', 'e:\\pictures\\tmp\\img_20200522_212214.jpg']
            # Produces
            # Node('/ROOT')
            # └── Node('/ROOT/', files=0)
            #     ├── Node('/ROOT//pictures', files=0)
            #     └── Node('/ROOT//projects', files=0)
            print(common_prefix)
            print(paths)
            tree = FilePrefixTree(common_prefix, paths)
            print(RenderTree(tree.root))
            if tree.root:
                recursively_add_tree_widgets(tree.basedir, [rootItem, None])

    def __init__(self, parent, image_repository):
        QtGui.QStandardItemModel.__init__(self, 0, 2, parent)
        self.image_repository = image_repository
        self.setHeaderData(self.FOLDER_NAME, QtCore.Qt.Horizontal, "Name")
        self.setHeaderData(self.FOUND_IMAGES, QtCore.Qt.Horizontal, "Anzahl Bilder")
        rootItem = self.invisibleRootItem()
        # TODO set name of root item.

        # Get all paths that are existing in the app.
        paths = self.image_repository.get_all_paths()
        if paths:
            common_prefix = os.path.commonpath(paths) + os.path.sep
            # TODO this is still broken (im not sure why)
            # Input
            # e:\\
            # ['e:\\projects\\python\\lothren\\test\\images\\a-duplicate.jpg', 'e:\\projects\\python\\lothren\\test\\images\\a-resized.jpg', 'e:\\projects\\python\\lothren\\test\\images\\a.bmp', 'e:\\projects\\python\\lothren\\test\\images\\a.gif', 'e:\\projects\\python\\lothren\\test\\images\\a.jpg', 'e:\\projects\\python\\lothren\\test\\images\\a.png', 'e:\\projects\\python\\lothren\\test\\images\\b.jpg', 'e:\\projects\\python\\lothren\\test\\images\\öäü.jpg', 'e:\\projects\\python\\lothren\\test\\images\\dirtest\\a.jpg', 'e:\\pictures\\tmp\\img_20200522_142802.jpg', 'e:\\pictures\\tmp\\img_20200522_191209.jpg', 'e:\\pictures\\tmp\\img_20200522_191256.jpg', 'e:\\pictures\\tmp\\img_20200522_192324.jpg', 'e:\\pictures\\tmp\\img_20200522_194323.jpg', 'e:\\pictures\\tmp\\img_20200522_201351.jpg', 'e:\\pictures\\tmp\\img_20200522_202724.jpg', 'e:\\pictures\\tmp\\img_20200522_212214.jpg']
            # Produces
            # Node('/ROOT')
            # └── Node('/ROOT/', files=0)
            #     ├── Node('/ROOT//pictures', files=0)
            #     └── Node('/ROOT//projects', files=0)
            print(common_prefix)
            print(paths)
            tree = FilePrefixTree(common_prefix, paths)
            print(RenderTree(tree.root))
            if tree.root:
                recursively_add_tree_widgets(tree.basedir, [rootItem, None])
