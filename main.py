import sys
import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import lyj_progressBar
from StartGridThread import StartGridThread


class MyFrom(QWidget):
    def __init__(self, parent=None):
        super(MyFrom, self).__init__(parent=parent)
        self.setWindowTitle('9宫格生成程序')
        self.resize(600, 200)
        self.init()

    def init(self):
        self.gridlayout = QGridLayout()
        self.label1 = QLabel('选择需要转换为9宫格的文件：')
        self.gridlayout.addWidget(self.label1, 0, 0, 2, 1)
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setEnabled(False)
        self.gridlayout.addWidget(self.lineEdit1, 0, 2, 2, 1)
        self.button1 = QPushButton('选择图片')
        self.gridlayout.addWidget(self.button1, 0, 4, 2, 1)
        self.submitButton = QPushButton('生成9宫格')
        self.gridlayout.addWidget(self.submitButton, 3, 2, 2, 1)
        self.button1.clicked.connect(self.button_connect)
        self.submitButton.clicked.connect(self.submitButton_connect)

        self.grid9Thread = StartGridThread()
        self.grid9Thread._signal.connect(self.grid9Thread_callbacklog)
        self.grid9Thread._parValue.connect(self.callbacklog_par)
        self.setLayout(self.gridlayout)

    def button_connect(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", './',
                                                         "Image files (*.jpg *.gif *.png);;Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        self.lineEdit1.setText(fileName)

    def grid9Thread_callbacklog(self, result):
        self.button1.setEnabled(True)
        self.submitButton.setEnabled(True)
        self.Dialog.close()
        if result:
            QMessageBox.question(self, '消息', '导出9宫格成功',
                                 QMessageBox.Yes)
        else:
            QMessageBox.question(self, '消息', '导出9宫格失败',
                                 QMessageBox.Yes)

    def submitButton_connect(self):
        fileName = self.lineEdit1.text()
        if fileName.endswith('.gif'):
            self.grid9Thread.setValue(2, fileName)
            self.grid9Thread.start()
        elif fileName.endswith('.jpg') or fileName.endswith('.png'):
            self.grid9Thread.setValue(1, fileName)
            self.grid9Thread.start()
        else:
            self.grid9Thread.setValue(3, fileName)
            self.grid9Thread.start()
        self.button1.setEnabled(False)
        self.submitButton.setEnabled(False)
        self.Dialog = QtWidgets.QDialog()
        self.ui = lyj_progressBar.Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.Dialog.show()
        self.Dialog.exec()

    def callbacklog_par(self, value):
        self.ui.set_progressBar(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myUI = MyFrom()
    myUI.setWindowFlag(Qt.WindowMinimizeButtonHint)  # 禁止放大界面
    myUI.setFixedSize(myUI.width(), myUI.height())  # 静止拖拽放大界面
    myUI.show()
    sys.exit(app.exec_())
