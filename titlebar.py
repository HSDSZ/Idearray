################Below are widgets for titlebar################
from PyQt5.QtWidgets import QLabel,QLineEdit,QCompleter,QPushButton,QApplication,QHBoxLayout
from PyQt5.QtCore import Qt, QStringListModel, pyqtSignal
from PyQt5.QtGui import QCursor
from stylesheetsum import *
from constants import *
from settings import readconfig

class CustomGap(QLabel):
    # this label emit doubleclicked signal
    def __init__(self, parent=None):
        super(CustomGap, self).__init__(parent)
        self.parent = parent

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.parent.doubleclicked = True
        self.parent.max()

class CustomLineEdit(QLineEdit):
    # CustomLineEdit has a CustomCompleter(below) embedded inside
    # define a custom signal which emmit a str
    dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.setFixedHeight(25)
        self.setPlaceholderText(" Search tags or drag link/file here")
        self.setAcceptDrops(True)

        # set the completer. Note the CustomCompleter has built-in QstringModel, so donnot need to input a str list
        self.completer = CustomCompleter(parent=self)
        self.setCompleter(self.completer)

    def dragEnterEvent(self, event):
        # hasText means once the drag in has text, allow
        if event.mimeData().hasText():
            event.accept()

    # use the emit in the dropevent to trigger our dropped event
    def dropEvent(self, event):
        dragtext = event.mimeData().text()
        # haslinks means drag in a file or link
        if event.mimeData().hasUrls():
            # emit to trigger the dropped event
            self.dropped.emit(dragtext)
        else:
            self.setText(self.text() + ' ' + dragtext)

class CustomCompleter(QCompleter):
    def __init__(self, parent=None):
        super(CustomCompleter, self).__init__(parent)
        self.alltags = []
        # Emtyp hottags.
        self.hottags = []
        # MatchContains means showing the result contains this input. MatchExactly means the exact result
        self.setFilterMode(Qt.MatchContains)
        self.setCaseSensitivity(Qt.CaseInsensitive)

        # build stringlistmodel. taglist the dropdown list shown
        self.taglist = QStringListModel()
        self.setModel(self.taglist)

    # Add texts instead of replace
    def pathFromIndex(self, index):
        path = QCompleter.pathFromIndex(self, index)
        lst = str(self.widget().text()).split()

        if len(lst) > 1:
            path = '%s %s' % (' '.join(lst[:-1]), path)

        return path

    # Add operator to separate between texts. splitPath function is the default function of QCompleter
    def splitPath(self, path):
        # get the str after the last ' ' (space) as the new path
        path = str(path.split(' ')[-1])  # .lstrip(' ')
        if path == "":
            # if the path is empty meaning, the user input a simple space and ready to input another tag
            self.taglist.setStringList(self.hottags)
        else:
            self.taglist.setStringList(self.alltags)

        return [path]

class TitleBar(QLabel):
    def __init__(self, parent):
        super(TitleBar, self).__init__(parent)
        # here parent is the mainwindow
        self.mainwindow = parent
        self.setFixedHeight(50)
        self.mode = 'bar'
        self.previousmode = 'bar'
        self.m_drag = False

        # create a searchbar
        self.searchbar = CustomLineEdit(parent=self)
        self.searchbar.setStyleSheet(searchbarstyle)
        # self.searchbar.setMaximumWidth(400)

        # gap is  for icon and double click use
        self.icon = CustomGap(parent=self)
        self.icon.setFixedWidth(50)
        self.icon.setStyleSheet(hsdsz)

        # create a some quick tool button
        self.pinbutton = NoMoveButton()
        self.pinbutton.setFixedSize(27, 27)
        self.pinned = False
        self.pinbutton.setStyleSheet(unpinned)
        self.miniwinbutton = NoMoveButton()
        self.miniwinbutton.setFixedSize(27, 27)
        self.miniwinbutton.setStyleSheet(down)
        self.minibutton = QPushButton()
        self.minibutton.setFixedSize(27, 27)
        self.minibutton.setStyleSheet(minimize)
        self.maxbutton = NoMoveButton()
        self.maxbutton.setFixedSize(27, 27)
        self.maxbutton.setStyleSheet(originmode)
        self.closebutton = NoMoveButton()
        self.closebutton.setFixedSize(27, 27)
        self.closebutton.setStyleSheet(closeicon)

        # arrange these in a horizontal way
        hbx = QHBoxLayout()
        hbx.addWidget(self.icon)
        hbx.addWidget(self.searchbar)
        hbx.addWidget(self.pinbutton)
        hbx.addWidget(self.miniwinbutton)
        hbx.addWidget(self.minibutton)
        hbx.addWidget(self.maxbutton)
        hbx.addWidget(self.closebutton)
        hbx.setContentsMargins(0, 0, 0, 0)
        hbx.setSpacing(0)
        self.setLayout(hbx)

        # signals
        self.pinbutton.clicked.connect(self.pin)
        self.miniwinbutton.clicked.connect(self.miniwin)
        self.minibutton.clicked.connect(self.min)
        self.maxbutton.clicked.connect(self.max)
        self.closebutton.clicked.connect(self.shutdown)

    def swithcmodeto(self, modeto='bar'):
        self.previousmode = self.mode
        if modeto == 'max':
            self.mainwindow.belowwidget.show()
            self.maxbutton.setStyleSheet(maxmode)
            self.miniwinbutton.setStyleSheet(up)
            self.mode = 'max'
            self.mainwindow.showMaximized()
        elif modeto == 'normal':
            self.mainwindow.belowwidget.show()
            self.mainwindow.maintab.show()
            self.maxbutton.setStyleSheet(originmode)
            self.miniwinbutton.setStyleSheet(up)
            self.mode = 'normal'
            self.mainwindow.showNormal()
            self.mainwindow.resize(startupwidth, startupheight)

        elif modeto == 'detail':
            self.mainwindow.belowwidget.show()
            self.mainwindow.maintab.hide()
            self.mainwindow.toolarea.show()
            self.maxbutton.setStyleSheet(originmode)
            self.miniwinbutton.setStyleSheet(down)
            self.mode = 'detail'
            self.mainwindow.showNormal()
            self.mainwindow.resize(picwidth + 10, 600)

        elif modeto == 'bar':
            self.mainwindow.belowwidget.hide()
            QApplication.processEvents()
            self.maxbutton.setStyleSheet(originmode)
            self.miniwinbutton.setStyleSheet(down)
            self.mode = 'bar'
            self.mainwindow.showNormal()
            self.mainwindow.resize(picwidth + 10, 60)
            self.mainwindow.resize(picwidth + 10, 60)
        else:
            pass

    def shutdown(self):
        self.mainwindow.previewwindow.close()
        self.mainwindow.dbcon.close()
        self.mainwindow.close()

    def pin(self):
        if self.pinned:
            self.pinbutton.setStyleSheet(unpinned)
            self.mainwindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget)
            self.mainwindow.show()
        else:
            self.pinbutton.setStyleSheet(pinned)
            self.mainwindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.mainwindow.show()

        self.pinned = not (self.pinned)

    def miniwin(self):
        if self.mode == 'bar' or self.mode == 'detail':
            self.swithcmodeto('normal')
        elif self.mode == 'normal':
            self.swithcmodeto('bar')
        elif self.mode == 'max':
            self.mainwindow.showNormal()
            self.swithcmodeto('bar')

    def max(self):
        # if this icon is max, then make the mainwindow original mode
        if self.mode == 'normal' or self.mode == 'bar' or self.mode == 'detail':
            self.swithcmodeto('max')

        elif self.mode == 'max':
            self.swithcmodeto('normal')

        else:
            pass

    def min(self):
        self.mainwindow.showMinimized()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.start_x = QMouseEvent.x()
            self.start_y = QMouseEvent.y()
            self.m_drag = True

    def mouseMoveEvent(self, QMouseEvent):
        if self.mode == 'max' and self.m_drag == True:
            # after moving, if the current icon is max style, change it into originnal
            self.swithcmodeto('normal')

        # change cursor to hand
        if self.m_drag:
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            dis_x = QMouseEvent.x() - self.start_x
            dis_y = QMouseEvent.y() - self.start_y
            self.mainwindow.move(self.mainwindow.x()+dis_x, self.mainwindow.y()+dis_y)

    def mouseReleaseEvent(self, QMouseEvent):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.m_drag = False

class NoMoveButton(QPushButton):
    def __init__(self, parent=None):
        super(NoMoveButton, self).__init__(parent)

    def mouseMoveEvent(self, QMouseEvent):
        pass

startupDBpath, startupwidth, startupheight, startuplook = readconfig()
