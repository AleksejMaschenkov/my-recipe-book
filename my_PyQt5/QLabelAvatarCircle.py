# -*- coding: utf-8 -*-

from typing import Union

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QBrush, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel


# =========================================================
#
# =========================================================
class AvatarLabel(QLabel):
    """ Circle avatar label """

    def __init__(self, image: Union[QPixmap, str, None], parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # --------------------------------------------
        if isinstance(image, str) and image:
            self.setPixmap(QPixmap(image))
        elif isinstance(image, QPixmap):
            self.setPixmap(image)
        else:
            self.setPixmap(QPixmap())

    def setPixmap(self, pixmap: QPixmap) -> None:
        self.__pixmap = pixmap
        self.update()

    def paintEvent(self, e):
        """ paint avatar """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        a = min(self.width(), self.height())
        r, rect = a // 2, QRect(0, 0, a, a)  # N0 self.rect()

        painter.setPen(Qt.NoPen)
        # [Qt.IgnoreAspectRatio, Qt.KeepAspectRatio, Qt.KeepAspectRatioByExpanding]

        temp = self.__pixmap.scaled(a, a, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.setBrush(QBrush(temp))
        painter.drawRoundedRect(rect, r, r)

# =========================================================
#
# =========================================================
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    f_name = r'C:\PYTHON_LEXA\PY_BookCase1\bookcase\bibl_widgets\labels\Tsar_Alexander_III_of_Russia_2.jpg'
    app = QApplication([])
    # -----------------------------------------
    def get_bytes(file):
        with open(file, 'rb') as f:
            h = f.read()
            return h


    pm = QPixmap()
    pm.loadFromData(get_bytes(f_name))

    ll = [pm, f_name, None]
    my_label = AvatarLabel(ll[1])
    my_label.show()
    # ---------------------------------------------
    sys.exit(app.exec_())

