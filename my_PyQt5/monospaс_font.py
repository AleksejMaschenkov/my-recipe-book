# -*- coding: utf-8 -*-
import sys
# =========================================================
#
# =========================================================


from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QFontMetrics, QFontDatabase
from PyQt5.QtWidgets import QComboBox, QWidget, QDialog, QDialogButtonBox, QPushButton, QLineEdit, QLabel


# https://it.kgsu.ru/Python_Qt/pyqt5_264.html
# https://github.com/Talljoe/plover/blob/f360756c6e9854f3615d539b420b8efd3cf2bbbb/plover/gui_qt/suggestions_dialog.py#L163

def get_mono():
    fdb = QFontDatabase()
    # __ = fdb.systemFont(QFontDatabase.FixedFont).family()
    filtr = QFontDatabase.Cyrillic  # QFontDatabase.Any
    return [f_str for f_str in fdb.families(filtr) if fdb.isFixedPitch(f_str)]


def get_size(families) -> dict:
    mydict = {}  # REF: {width:size}
    for p_size in range(1, 50):
        font = QFont(families, p_size)  # мухой
        w = QFontMetrics(font).width('ы')  # набирает время
        if mydict.get(w, None) is None:
            mydict[w] = p_size
    return mydict


# =========================================================
#
# =========================================================
class my_Dialog(QDialog):

    def __init__(self, curent_font):
        super().__init__()
        self.setWindowTitle('Выбор моноширного шрифта')
        self.setModal(True)
        self.w_lab_name = QLabel('Шрифт:')
        self.w_cmb_families = QComboBox()
        self.w_cmb_families.activated.connect(self.sl_w_cmb_families_activated)

        self.w_lab_width = QLabel('Ширина:')
        self.w_cmb_width = QComboBox()
        self.w_cmb_width.activated.connect(self.sl_w_cmb_width_activated)

        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setReadOnly(True)
        self.lineEdit1.setText('Съешь же ещё этих мягких французских булок, да выпей чаю')
        # lineEdit1.setStyleSheet('{font-family: Courier New; font-size: 48px;  }')

        QBtnOK, QBtnCn = QDialogButtonBox.Ok, QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(QBtnOK | QBtnCn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.setDefaultButton(QBtnOK)

        self.create_layout()
        self.w_cmb_families.addItems(get_mono())
        self.show()

        # ======================================
        vvvv = ["Courier New", str(14)]
        if isinstance(curent_font, QFont):
            vvvv = [curent_font.family(), str(curent_font.pointSize())]

        index = self.w_cmb_families.findText(vvvv[0])
        self.w_cmb_families.setCurrentIndex(index)
        self.w_cmb_families.activated.emit(index)

        self.set_pos_width(vvvv[1])

    def create_layout(self):
        grid = QtWidgets.QGridLayout()

        grid.addWidget(self.w_lab_name, 0, 0)
        grid.addWidget(self.w_cmb_families, 0, 1, 1, 3)
        grid.addWidget(self.w_lab_width, 0, 4)
        grid.addWidget(self.w_cmb_width, 0, 5)

        grid.addWidget(self.lineEdit1, 1, 0, 1, 6)
        grid.addWidget(self.button_box, 2, 3, 3, 5)
        grid.setColumnStretch(1, 2)

        self.setLayout(grid)

    def setDefaultButton(self, bt=QDialogButtonBox.Cancel):
        btn = self.button_box.button(bt)
        if btn is not None:
            btn.setAutoDefault(True)
            btn.setDefault(True)

    def set_pos_width(self, txt: str = '14'):
        ind_w = self.w_cmb_width.findText(txt)
        if ind_w > -1:
            self.w_cmb_width.setCurrentIndex(ind_w)
            self.w_cmb_width.activated.emit(ind_w)

    def sl_w_cmb_families_activated(self, index):
        font_name = self.w_cmb_families.itemText(index)
        self.connect(font_name)

    def connect(self, font_name):
        old = self.w_cmb_width.currentData()
        self.w_cmb_width.clear()
        for width, p_size in get_size(font_name).items():
            self.w_cmb_width.addItem(str(width), (width, QFont(font_name, p_size), p_size))
        # -------------------------------------
        if old is not None:
            self.set_pos_width(str(old[0]))
        self.setFocusProxy(self.w_cmb_width)

    def sl_w_cmb_width_activated(self, index):
        my_tuple = self.w_cmb_width.itemData(index)
        temp: QFont = my_tuple[1]

        self.lineEdit1.setFont(temp)

    def get_font(self):
        return self.lineEdit1.font()


# =========================================================
#
# =========================================================

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.bt_select = QPushButton("Выбор шрифта")
        self.bt_select.clicked.connect(self.run_exampl)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.bt_select, 0, 0)
        self.setLayout(grid)
        self.show()

    def run_exampl(self):
        dialog = my_Dialog(QFont('Courier New', 14))
        accepted = dialog.exec_()

        if accepted:
            print("Ok.. font :", dialog.get_font())




# =========================================================
#
# =========================================================

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
