from PyQt5 import QtWidgets


class DuplicateDetailsList(QtWidgets.QListView):
    def __init__(self):
        # TODO this should also include a groupBox that shows as a title the current phash
        QtWidgets.QListView.__init__(self)
        # self.setModel()
        # self.setItemDelegate()

 # TODO https://doc.qt.io/qtforpython/PySide2/QtWidgets/QAbstractItemDelegate.html#PySide2.QtWidgets.QAbstractItemDelegate