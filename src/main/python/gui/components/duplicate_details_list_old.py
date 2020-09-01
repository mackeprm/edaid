from PIL import Image, ImageQt
from PyQt5 import QtGui, QtWidgets, QtCore
import subprocess, os, platform


class DuplicateSelector:
    def __init__(self, display_widget, item_widgets):
        self.selected_duplicates = []
        self.display_widget = display_widget
        self.item_widgets = item_widgets
        self.display_widget.setText("0 Bilder ausgewählt")

    def toggle(self, id):
        if id in self.selected_duplicates:
            self.selected_duplicates.remove(id)
        else:
            self.selected_duplicates.append(id)
        self.display_widget.setText("{0} Bilder ausgewählt".format(len(self.selected_duplicates)))

    # Def remove all, add all


class DuplicateDetailListAdapter:
    def __init__(self, scrollarea, num_selected_label, image_repository, duplicate_service):
        self.widget = scrollarea
        self.num_selected_label = num_selected_label
        self.image_repository = image_repository
        self.duplicate_service = duplicate_service
        self.duplicates = []
        self.widgets = []
        self.duplicate_selector = DuplicateSelector(self.num_selected_label, [])

    def show_details_for(self, phash):
        duplicate_details_layout = self.widget.layout()
        self.duplicates = self.image_repository.get_duplicates_for_phash(phash)
        # Remove all existing widgets:
        self.duplicate_selector = DuplicateSelector(self.num_selected_label, [])
        for i in reversed(range(duplicate_details_layout.count())):
            child = duplicate_details_layout.takeAt(i).widget()
            child.setParent(None)
            child.deleteLater()

        for duplicate in self.duplicates:
            current_entry = DuplicateDetailListEntry(duplicate, self.duplicate_service, self.duplicate_selector)
            self.duplicate_selector.item_widgets.append(current_entry)
            duplicate_details_layout.addWidget(current_entry)


# TODO this should be it's own viewmodel, based on custom delegates
# https://doc.qt.io/qt-5/model-view-programming.html#delegate-classes
# https://doc.qt.io/qt-5/qtwidgets-itemviews-stardelegate-example.html
class DuplicateDetailListEntry(QtWidgets.QWidget):
    def enterEvent(self, event):
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.lightGray)
        self.setPalette(p)

    def leaveEvent(self, event):
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)

    def mousePressEvent(self, event):
        self.duplicate_selector.toggle(self.id)
        self.checkbox.toggle()

    def mouseDoubleClickEvent(self, event):
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', self.path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(self.path)
        else:  # linux variants
            subprocess.call(('xdg-open', self.path))

    def create_thumbnail_from(self, path):
        # QImage result = img.scaled(200, 150, Qt::IgnoreAspectRatio, Qt::FastTransformation);
        try:
            im = Image.open(path)
            imageQT = ImageQt.ImageQt(im)
            imageQTRescaled = imageQT.scaled(128, 128, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
            pixmap = QtGui.QPixmap.fromImage(imageQTRescaled)
            qt_thumbnail = QtWidgets.QLabel("", self)
            qt_thumbnail.setPixmap(pixmap)
        except FileNotFoundError:
            qt_thumbnail = QtWidgets.QLabel("Bild nicht gefunden", self)
        return qt_thumbnail

    # TODO onclick-handle: Select Multiselect.
    # TODO sort
    def __init__(self, image_data, duplicate_service, duplicate_selector):
        self.id = image_data["id"]
        self.path = image_data["path"]
        self.duplicate_service = duplicate_service
        self.duplicate_selector = duplicate_selector

        # TODO save handled or not
        # TODO save hash?
        QtWidgets.QWidget.__init__(self)
        self.setAutoFillBackground(True)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(128)
        self.setMaximumHeight(128)
        entry_layout = QtWidgets.QHBoxLayout()
        self.checkbox = QtWidgets.QCheckBox("", self)

        self.thumbnail = self.create_thumbnail_from(image_data["path"])

        self.metadata_frame = QtWidgets.QFrame(self)
        metadata_vertical_layout = QtWidgets.QVBoxLayout()
        self.metadata_frame.setLayout(metadata_vertical_layout)
        self.path_label = QtWidgets.QLabel(image_data["path"], self)

        self.image_property_frame = QtWidgets.QFrame(self.metadata_frame)
        metadata_horizontal_layout = QtWidgets.QHBoxLayout()
        self.image_property_frame.setLayout(metadata_horizontal_layout)
        self.size_label = QtWidgets.QLabel(image_data["image_size"])
        self.filesize_label = QtWidgets.QLabel(image_data["file_size"])
        metadata_horizontal_layout.addWidget(self.size_label)
        metadata_horizontal_layout.addWidget(self.filesize_label)

        metadata_vertical_layout.addWidget(self.path_label)
        metadata_vertical_layout.addWidget(self.image_property_frame)

        self.removeButton = QtWidgets.QPushButton("Löschen")
        self.removeButton.clicked.connect(self.remove)
        self.ignoreButton = QtWidgets.QPushButton("Ignorieren")
        self.ignoreButton.setEnabled(False)
        # TODO ignore button => Update Database Only
        # TODO ignore button: remove from database?

        entry_layout.addWidget(self.checkbox, 5, QtCore.Qt.AlignLeft)
        entry_layout.addWidget(self.thumbnail, 15, QtCore.Qt.AlignLeft)
        entry_layout.addWidget(self.metadata_frame, 70, QtCore.Qt.AlignLeft)
        entry_layout.addWidget(self.removeButton, 5, QtCore.Qt.AlignLeft)
        entry_layout.addWidget(self.ignoreButton, 5, QtCore.Qt.AlignLeft)

        self.setLayout(entry_layout)

    def remove(self):
        # TODO try/catch
        self.duplicate_service.delete(self.id, self.path)
        self.deleteLater()
        # TODO redraw: Duplicate List (handled)
        # TODO redraw:
