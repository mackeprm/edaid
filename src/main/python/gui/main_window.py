import os
from datetime import datetime

import imagehash
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from gui.components.duplicate_details_list_old import DuplicateDetailListAdapter
from gui.messageboxes import about
from model.duplicate_list_model import DuplicateListModel
from model.file_tree_model import FileTreeModel
from services.duplicate_service import DuplicateService
from services.file_scanner import find_all_images_in
from services.image_repository import ImageRepository


class MainWindow(QtWidgets.QMainWindow):
    RETVAL_OK = 1024

    def init_menu(self):
        self.actionQuit.triggered.connect(self.exit)
        self.actionAbout.triggered.connect(about.show_about)

    def __init__(self, ctx, project):
        QtWidgets.QMainWindow.__init__(self)
        self.ctx = ctx
        uic.loadUi(ctx.get_resource("ui/main_window.ui"), self)
        self.setWindowIcon(QtGui.QIcon(ctx.get_resource("Icon.ico")))
        self.setWindowTitle("Unbenanntes Projekt - " + str(datetime.now()))

        self.project = project
        self.image_repository = ImageRepository(project['path'])
        self.duplicate_service = DuplicateService(self.image_repository)

        self.init_menu()
        self.add_folder_button.clicked.connect(self.add_folder)
        self.file_tree_model = FileTreeModel(self, self.image_repository)
        self.file_tree.setModel(self.file_tree_model)
        # TODO add keyboard shortcuts

        # duplicateDetail box
        self.duplicate_details_list_adapter = DuplicateDetailListAdapter(self.duplicate_details_scrollarea,
                                                                         self.num_selected_label,
                                                                         self.image_repository,
                                                                         self.duplicate_service)

        self.duplicate_list_model = DuplicateListModel(self.image_repository, self.duplicate_details_list_adapter)
        self.duplicate_list.setModel(self.duplicate_list_model)
        self.duplicate_list.clicked.connect(self.duplicate_list_model.clicked)

    def exit(self):
        self.close()

    def add_folder(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:',
                                                         os.getcwd(),
                                                         QtWidgets.QFileDialog.ShowDirsOnly)
        image_files = find_all_images_in(dir)

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText(str(len(image_files)) + " Bilder gefunden. Alle importieren?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        retval = msg.exec_()
        maximum_progress = len(image_files)
        if retval == self.RETVAL_OK:
            progress = QtWidgets.QProgressDialog("Importiere Bilder...", "Abbrechen", 0, maximum_progress, self)
            progress.setWindowModality(QtCore.Qt.WindowModal)
            # TODO parallelize?
            for i in range(0, maximum_progress):
                QtWidgets.QApplication.processEvents()
                progress.setValue(i)
                if progress.wasCanceled():
                    break
                image_file = image_files[i]
                print("Now handling: " + image_file['path'])
                with Image.open(image_file['path']) as image:
                    image_file['image_size'] = str(image.size[0]) + " x " + str(image.size[1])
                    image_file['phash'] = str(imagehash.phash(image))
                    self.duplicate_service.upsert(image_file)
            progress.setValue(maximum_progress)
            self.duplicate_list_model.reset_duplicates()
            self.duplicate_list_model.layoutChanged.emit()
            self.file_tree_model.reset_paths()
            self.file_tree_model.layoutChanged.emit()
