from PyQt5 import QtWidgets


def show_error(exception):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Es ist ein Fehler aufgetreten.")
    msg.setDetailedText("Fehler: {0}".format(exception))
    #TODO get version from config!
    msg.setWindowTitle("Edai v. 0.0.3-SNAPSHOT - Fehler")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()
