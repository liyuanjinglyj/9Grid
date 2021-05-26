from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

import gridUtils


class StartGridThread(QtCore.QThread):
    _signal = pyqtSignal(bool)
    _parValue=pyqtSignal(int)

    def __init__(self):
        super(StartGridThread, self).__init__()

    def setValue(self, switchNum, fileName):
        self.switchNum = switchNum
        self.fileName = fileName

    def run(self):
        try:
            self._parValue.emit(50)
            if self.switchNum == 1:
                gridUtils.grid9_image(self.fileName)
            elif self.switchNum == 2:
                gridUtils.grid9_gif2(self.fileName)
            elif self.switchNum == 3:
                gridUtils.grid9_gif(self.fileName)
                gridUtils.gird9_Video(self.fileName, '九宫格视频')
            else:
                return
            self._parValue.emit(100)
            self._signal.emit(True)
        except Exception:
            self._signal.emit(False)

