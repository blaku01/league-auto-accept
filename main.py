from gui import *
from accepter_obj import *
from PyQt5.QtCore import QThread
import pandas as pd
import sys
from config import *

class WorkerThread(QThread):
    def __init__(self, accepter):
        super().__init__()
        self.acc = accepter
    def run(self):
        self.acc.defineAfterStartButton()
        self.acc.startRunning()

class AcceptApp(Ui_main_window):
    def __init__(self, window):
        self.program = Accepter(path)
        self.setupUi(window)
        self.clear_picks.clicked.connect(self.clr_picks)
        self.clear_bans.clicked.connect(self.clr_bans)
        self.clear_items.clicked.connect(self.clr_items)
        self.add_picks.clicked.connect(self.insertToPicks)
        self.add_bans.clicked.connect(self.insertToBans)
        self.add_items.clicked.connect(self.insertToItems)
        self.start_button.clicked.connect(self.start_searching)

    def clr_picks(self):
        self.program.picks = []
        self.pick_list.clear()

    def clr_bans(self):
        self.program.bans = []
        self.ban_list.clear()

    def clr_items(self):
        self.program.items = []
        self.item_list.clear()

    def insertToPicks(self):
        pick = self.typed_pick.text()
        if pick != "":
            self.pick_list.insertItem(20, pick)
            self.program.picks.append(pick)

    def insertToBans(self):
        ban = self.typed_ban.text()
        if ban != "":
            self.ban_list.insertItem(20, ban)
            self.program.bans.append(ban)

    def insertToItems(self):
        item = self.typed_item.text()
        if item != "":
            self.item_list.insertItem(20, item)
            self.program.items.append(item)

    def start_searching(self):
        if self.start_button.text() == "STOP":
            self.start_button.setText("START")
            self.status_viewer.setText(QtCore.QCoreApplication.translate("main_window","<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">PRESS START</span></p></body></html>"))
            self.worker.terminate()
        else:
            self.start_button.setText("STOP")
            self.status_viewer.setText(QtCore.QCoreApplication.translate("main_window","<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">RUNNING</span></p></body></html>"))
            self.worker = WorkerThread(self.program)
            self.worker.start()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

ui = AcceptApp(MainWindow)
MainWindow.show()
app.exec_()
