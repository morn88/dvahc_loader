from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import sys
import os
from pyconacc import connect, download, check_folder
import urllib


class MyWind(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 100, 400, 200)
        self.setWindowIcon(QtGui.QIcon('eba.png'))

        self.tray_icon = SystemTrayIcon(QtGui.QIcon('eba.png'), self)
        self.tray_icon.setToolTip('Готов к закачке')
        self.tray_icon.show()

        self.progress_bar = QtWidgets.QProgressBar(self)

        timer = QTimer(self)
        self.btn_copy = QtWidgets.QPushButton("Download")
        self.btn_copy.clicked.connect(self.copy_files)

        self.btn_connect = QtWidgets.QPushButton("Connect")
        self.btn_connect.clicked.connect(self.connect_to_url)

        self.label_out = QtWidgets.QLabel()
        self.line_uri = QtWidgets.QLineEdit()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.line_uri, 0, 0)
        grid.addWidget(self.label_out, 1, 0)
        grid.addWidget(self.progress_bar, 2, 0)
        grid.addWidget(self.btn_connect, 3, 0)
        grid.addWidget(self.btn_copy, 4, 0)

        self.setLayout(grid)
        self.show()

    def connect_to_url(self):
        try:
            self.label_out.setText(connect(self.line_uri.text()))
        except Exception as e:
            self.label_out.setText(str(e))

    def copy_files(self):
        try:
            check_folder()
            downl_set = download(self.line_uri.text())
            if downl_set is not None:
                downl_set = list(downl_set)
                step = 100 / len(downl_set)
                value = step
                count_of_files = len(downl_set)
                self.label_out.setText('Файлов в папке: ' + str(count_of_files))
                for i in range(len(downl_set)):
                    QtWidgets.qApp.processEvents()
                    urllib.request.urlretrieve(downl_set[i], os.path.join('done_webm',downl_set[i].split('/')[-1]))
                    self.progress_bar.setValue(value)
                    value += step
                    count_of_files -= 1
                    self.label_out.setText('Файлов: ' + str(count_of_files))
                    self.tray_icon.setToolTip('Файлов: ' + str(count_of_files))

            self.label_out.setText('None')
            self.tray_icon.setToolTip('Ready')
        except Exception as e:
            print(str(e))
            self.label_out.setText(str(e))


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Выйти")
        exitAction.triggered.connect(parent.close)
        maximase_action = menu.addAction("Показать")
        maximase_action.triggered.connect(self.size_change)
        self.setContextMenu(menu)

    def size_change(self):
        if self.parent().isMaximized:
            self.parent().showMinimized()
        else:
            self.parent().showMaximized()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWind()
    w.setWindowTitle('2ch downloader')
    sys.exit(app.exec_())