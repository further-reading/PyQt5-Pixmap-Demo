from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Raid Warning')
        self.setWindowIcon(QIcon(r'images\RaidWarning.ico'))
        self.splashScreen =  SplashScreen(parent = self)
        self.setCentralWidget(self.splashScreen)
        self.setFixedSize(360, 520)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.drag_position = event.globalPos() - self.pos();
        event.accept()

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            self.move(event.globalPos().x() - self.drag_position.x(),
                      event.globalPos().y() - self.drag_position.y());
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap(r"images\splash.png"))
        QWidget.paintEvent(self, event)


class SplashScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setFixedSize(360, 520)
        self.filterButton = HearthstoneButton(self, buttonText="Filter Settings")
        self.filterButton.move(50, 337)

        self.alertsButton = HearthstoneButton(self, buttonText="Alert Settings")
        self.alertsButton.move(50, 387)

        self.listenButton = HearthstoneButton(self, buttonText="Begin Listening")
        self.listenButton.move(50, 437)

        self.closeButton = CloseButton(self)
        self.closeButton.move(310, 0)
        self.closeButton.clicked.connect(self.closeAction)

        self.closeButton = MinimiseButton(self)
        self.closeButton.move(260, 0)
        self.closeButton.clicked.connect(self.parent.showMinimized)

    def closeAction(self):
        message = QMessageBox()
        message.setWindowTitle("Exit?")
        message.setWindowIcon(QIcon(r'images\RaidWarning.ico'))
        message.setIcon(QMessageBox.Question)
        message.setText("Are you sure you want to quit?")
        message.addButton("Yes", QMessageBox.AcceptRole)
        message.addButton("No", QMessageBox.ApplyRole)
        message.exec_()
        clicked = message.clickedButton().text()

        if clicked == "Yes":
            sys.exit()


class HearthstoneButton(QAbstractButton):
    mouseHover = pyqtSignal(bool)
    def __init__(self, *args, buttonText, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.images = {"selected" : r"images\selected.png",
                       "unselected" : r"images\unselected.png"}

        self.pixmap = QPixmap(self.images["unselected"])
        self.setMaximumSize(self.pixmap.size())
        self.setMinimumSize(self.pixmap.size())
        QFontDatabase.addApplicationFont(r"fonts\Hearthstone.ttf")
        self.setStyleSheet("""QAbstractButton {font-family: "Belwe Bd BT";
                                               color: #614326;
                                               font: 16pt}""")

        self.update()
        self.setText(buttonText)

    def enterEvent(self, event):
        self.mouseHover.emit(True)
        self.pixmap = QPixmap(self.images["selected"])
        self.update()

    def leaveEvent(self, event):
        self.pixmap = QPixmap(self.images["unselected"])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)
        painter.drawText(event.rect(), Qt.AlignCenter, self.text())
        self.update()

class CloseButton(QAbstractButton):
    mouseHover = pyqtSignal(bool)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.images = {"selected" : r"images\CloseSelected.png",
                       "unselected" : r"images\Close.png"}

        self.pixmap = QPixmap(self.images["unselected"])
        self.setMaximumSize(self.pixmap.size())
        self.setMinimumSize(self.pixmap.size())

        self.update()

    def enterEvent(self, event):
        self.mouseHover.emit(True)
        self.pixmap = QPixmap(self.images["selected"])
        self.update()

    def leaveEvent(self, event):
        self.pixmap = QPixmap(self.images["unselected"])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)
        self.update()

class MinimiseButton(QAbstractButton):
    mouseHover = pyqtSignal(bool)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.images = {"selected" : r"images\MinimiseSelected.png",
                       "unselected" : r"images\Minimise.png"}

        self.pixmap = QPixmap(self.images["unselected"])
        self.setMaximumSize(self.pixmap.size())
        self.setMinimumSize(self.pixmap.size())

        self.update()

    def enterEvent(self, event):
        self.mouseHover.emit(True)
        self.pixmap = QPixmap(self.images["selected"])
        self.update()

    def leaveEvent(self, event):
        self.pixmap = QPixmap(self.images["unselected"])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)
        self.update()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        main = Main()
        main.show()
        sys.exit(app.exec_())
