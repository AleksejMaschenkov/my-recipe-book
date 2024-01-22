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
