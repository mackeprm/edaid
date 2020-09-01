from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property

import os
import sys

from gui.splash_screen import SplashScreen


class EdaidContext(ApplicationContext):

    def run(self):
        splash_screen = SplashScreen(self)
        splash_screen.show()
        return appctxt.app.exec_()


if __name__ == '__main__':
    print("Starting Up.")
    print("Running in: " + os.getcwd())
    appctxt = EdaidContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
