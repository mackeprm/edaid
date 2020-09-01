from PyQt5 import QtWidgets, QtGui, uic

from gui.main_window import MainWindow
from gui.messageboxes.error import show_error


class UserCancelledError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super(SplashScreen, self).__init__()
        self.ctx = ctx
        self.main_window = None
        uic.loadUi(ctx.get_resource("ui/splash_screen.ui"), self)
        self.setWindowIcon(QtGui.QIcon(ctx.get_resource("Icon.ico")))

        self.create_new_project_button.clicked.connect(self.create_new_project)
        self.open_existing_project_button.clicked.connect(self.open_existing_project)
        self.exit_button.clicked.connect(self.exit)

    def create_new_project(self):
        # TODO create a new file?
        project = {"path": "tmp.eproj"}

        self.main_window = MainWindow(self.ctx, project)
        self.main_window.show()
        self.close()

    # move code to project service?
    def open_project(self):
        project_file = QtWidgets.QFileDialog.getOpenFileName(self, "Projektdatei auswählen.", "C:\\",
                                                             "Edaid Project Files (*.eproj)")
        if project_file:
            if project_file[0]:
                # TODO open the project. Check if there are settings inside.
                return {"path": project_file[0]}
            else:
                raise UserCancelledError("User pressed the cancel button.")
        raise FileNotFoundError

    def open_existing_project(self):
        try:
            project = self.open_project()
            self.main_window = MainWindow(self.ctx, project)
            self.main_window.show()
            self.close()
        except UserCancelledError:
            return
        except Exception as e:
            show_error(e)

    def exit(self):
        self.close()
