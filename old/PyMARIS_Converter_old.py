import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from main_gui import MainView


class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)

        self.main_view = MainView()
        self.main_view.show()


def main():
    app = QApplication(sys.argv)
    form = App(sys.argv)
    #form.show()
    app.exec_()


if __name__ == '__main__':
    main()
"""
if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
"""