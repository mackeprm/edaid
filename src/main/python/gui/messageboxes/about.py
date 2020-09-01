from PyQt5 import QtWidgets

from config import config


def show_about():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Edaid V. " + config['version'] + " : " + config['timestamp'])
    msg.setWindowTitle("Edaid v. 0.0.1-SNAPSHOT")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()
