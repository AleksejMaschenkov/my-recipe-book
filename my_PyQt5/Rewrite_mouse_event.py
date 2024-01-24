def get_app():
    app = QApplication.instance()
    if app is None:
        # if it does not exist then a QApplication is created
        app = QApplication([])
    return app

class EXAMPLE(QTextBrowser):
  ...
  def mousePressEvent(self, event):
    if event.button() in [Qt.RightButton, Qt.LeftButton]:
        print(" @00000 rewrite   Qt.RightButton ")
                # Rewrite the mouse event to a left button event so the cursor is
                # moved to the location of the pointer.
        event = QMouseEvent(QEvent.MouseButtonPress,
                                    event.pos(),
                                    Qt.LeftButton,
                                    Qt.LeftButton,
                                    Qt.NoModifier)
        get_app().postEvent(self.parent(), event)
         
