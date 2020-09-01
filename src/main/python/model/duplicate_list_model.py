from PyQt5 import QtCore
from services.image_repository import ImageRepository

OnClickRole = 849561745


class DuplicateListModel(QtCore.QAbstractListModel):
    # TODO remove this
    def reset_duplicates(self):
        self.duplicates = self.imageRepository.get_duplicates()

    def __init__(self, image_repository, image_detail_component):
        QtCore.QAbstractListModel.__init__(self)
        self.imageRepository = image_repository
        self.image_detail_component = image_detail_component
        self.duplicates = self.imageRepository.get_duplicates()

    # TODO number_of_unhandled_duplicates, number_of_handled_duplicates
    def data(self, index, role):
        # TODO move this to the duplicate_service
        if role == QtCore.Qt.DisplayRole:
            phash, number_of_duplicates, number_of_handled = self.duplicates[index.row()]
            return "" + phash + " : " + str(number_of_duplicates)
        if role == OnClickRole:
            return self.duplicates[index.row()]

    def rowCount(self, index):
        # TODO move this to the duplicate_service
        return len(self.duplicates)

    def clicked(self, index):
        self.image_detail_component.show_details_for(self.data(index, OnClickRole)[0])
