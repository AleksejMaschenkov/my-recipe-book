class EXAMPLE(QTextBrowser):
  ...
  def mousePressEvent(self, event):
           if event.button() == Qt.RightButton:
               # Rewrite the mouse event to a left button event so the cursor is
               # moved to the location of the pointer.
               event = QMouseEvent(QEvent.MouseButtonPress, 
                                   event.pos(),
                                   Qt.LeftButton, 
                                   Qt.LeftButton, 
                                   Qt.NoModifier)
           super().mousePressEvent(self, event)
