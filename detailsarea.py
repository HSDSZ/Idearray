from QTrelated import *
from SQLiterelated import *
from stylesheetsum import *
from webrelated import *
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QScrollArea, QGridLayout, QLabel, QHBoxLayout, \
    QPushButton, QTextEdit, QLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QRegion
from constants import *
import mss

class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.iseditmode = False

    def enterEvent(self, *args, **kwargs):
        self.iseditmode = True

    def leaveEvent(self, *args, **kwargs):
        focused_widget = QApplication.focusWidget()
        self.iseditmode = isinstance(focused_widget, QTextEdit)


class PixmapArea(QLabel):
    def __init__(self, parent=None):
        super(PixmapArea, self).__init__(parent)
        # setup the layout
        self.mainwindow = parent
        self.birthday = 0
        self.setAlignment(Qt.AlignBottom)
        self.emptygap = QLabel(self)
        # below are creating a textbrowser, set transparent/no boarder, set arial and 10 size
        self.title = TextEdit(self)
        self.title.setStyleSheet("QTextEdit {border: none}")
        self.title.setFont(QFont('Arial', 10))
        self.title.setFixedSize(picwidth, 40)
        self.title.move(0, 20)

        self.closebutton = QPushButton(self)
        self.closebutton.setFixedSize(20, 20)
        self.closebutton.setStyleSheet(removebuton2)
        self.closebutton.setToolTip('Close detail area')

        self.capturebutton = QPushButton(self)
        self.capturebutton.setFixedSize(20, 20)
        self.capturebutton.setStyleSheet(camerabutton)
        self.capturebutton.move(30, 0)
        self.capturebutton.setToolTip('Grab a new thumbnail')

        self.setFixedSize(picwidth, picheight + 60)

        self.title.textChanged.connect(self.titleeditted)
        self.closebutton.clicked.connect(self.closedetailarea)

    def closedetailarea(self):
        if self.mainwindow.titlebar.mode == 'normal' or self.mainwindow.titlebar.mode == 'max':
            self.mainwindow.toolarea.hide()
        elif self.mainwindow.titlebar.mode == 'detail':
            self.mainwindow.titlebar.swithcmodeto('bar')
            self.mainwindow.toolarea.hide()
        else:
            pass

    def showpixandtitle(self, birthday):
        self.birthday = birthday
        pix = getpixmapbybirthday(birthday)
        self.setPixmap(byte2pixmap(pix))
        title = gettitlebybirthday(birthday)
        self.title.setText(title)

    def titleeditted(self):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QTextEdit) and self.title.iseditmode:
            updatebybirthday(self.birthday, title=self.title.toPlainText())
            self.mainwindow.triggermodify(self.birthday, 'title')

    def updatepixmap(self, bytedata):
        updatebybirthday(birthday=self.birthday, pixmap=bytedata)


class CommentArea(QTextEdit):
    def __init__(self, parent):
        super(CommentArea, self).__init__(parent)
        self.mainwindow = parent
        self.textChanged.connect(self.textmodded)
        self.dbcon = None

    def showcomment(self, birthday, comment='3.141592653'):
        self.birthday = birthday
        if comment == '3.141592653':
            comment = getcommentbybirthday(self.birthday)

        self.setText(comment)

    def textmodded(self):
        # text modified, and the focus in on textedit
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QTextEdit):
            updatebybirthday(comment=self.toPlainText(), birthday=self.birthday)
            self.dbcon.commit()
            self.mainwindow.triggermodify(self.birthday, 'comment')


class TagArea(QScrollArea):
    def __init__(self, parent=None):
        super(TagArea, self).__init__(parent)
        self.mainwindow = parent
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setStyleSheet('QScrollArea { border: none}')
        self.dbcon = None
        self.birthday = -1000

        # setup the gridlayout in this scrollarea
        # this gradlayout has 5 coloumn
        self.gridlayout = QGridLayout(self)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        self.gridlayout.setSizeConstraint(QLayout.SetFixedSize)
        # draw the gridlayout on a widget. use the scrollare to scroll the widget
        widget = QWidget(self)
        widget.setLayout(self.gridlayout)
        self.setWidget(widget)

        # add a lineedit at the begining
        self.newinput = QLineEdit(self)
        self.newinput.setPlaceholderText('add new tag then press enter')
        self.newinput.setStyleSheet(searchbarstyle2)
        self.newinput.setFixedWidth(picwidth - 20)
        self.newinput.returnPressed.connect(self.addtag)
        self.gridlayout.addWidget(self.newinput, 0, 0, 1, 3)

    def showtags(self, birthday):
        # clear the layout, keep the newinput lineedit
        for i in range(self.gridlayout.count() - 1):
            self.gridlayout.itemAt(1).widget().close()
            self.gridlayout.takeAt(1)

        self.birthday = birthday
        # get tag list first
        tags = gettagbybirthday(self.birthday)
        taglist = tags.split()
        self.length = len(taglist)

        # insert them
        for i in range(self.length):
            label = taglist[i]  # label is the tag text
            tagbutton = RemovableButton(parent=self)
            tagbutton.setText(label)
            tagbutton.setFixedWidth(int(picwidth / 3 - 6.66))
            if len(label) > 10:
                # if the str is too long, show a tooltip
                tagbutton.setToolTip(taglist[i])
            self.gridlayout.addWidget(tagbutton, (i + 3) // 3, (i + 3) % 3, Qt.AlignCenter)

    def showtagsbylist(self, taglist):
        # clear the layout, keep the newinput lineedit
        for i in range(self.gridlayout.count() - 1):
            self.gridlayout.itemAt(1).widget().close()
            self.gridlayout.takeAt(1)

        # get tag list first
        self.length = len(taglist)
        # setup the gridlayout in this scrollarea
        # insert them
        for i in range(self.length):
            label = taglist[i]  # label is the tag text
            tagbutton = RemovableButton(parent=self)
            tagbutton.setText(label)
            tagbutton.setFixedWidth(int(picwidth / 3 - 6.66))
            if len(label) > 10:
                # if the str is too long, show a tooltip
                tagbutton.setToolTip(taglist[i])
            self.gridlayout.addWidget(tagbutton, (i + 3) // 3, (i + 3) % 3, Qt.AlignCenter)

    # newtab is used to show new tab when one tag is clicked

    def newtab(self, tag):
        # this case will open a new search in the main tab
        self.mainwindow.titlebar.searchbar.setText(tag)
        self.mainwindow.actionmade()

    def addtag(self):
        tagstr = gettagbybirthday(self.birthday)
        taglist = tagstr.split()
        newinputstr = self.newinput.text().lower()
        newinputlist = newinputstr.split()
        for tag in newinputlist:
            expandlist = expandstr(tag).split()[1:]
            for item in expandlist:
                if item not in newinputlist:
                    newinputlist.append(item)
            if tag not in taglist:
                tagstr += ' {}'.format(tag)
        updatebybirthday(self.birthday, tag=tagstr)
        self.showtags(self.birthday)
        self.dbcon.commit()

        self.mainwindow.triggermodify(self.birthday, 'tag')
        # update alltag in the completer
        self.mainwindow.titlebar.searchbar.completer.alltags = refreshalltags(
            self.mainwindow.titlebar.searchbar.completer.alltags, tagstr.split())
        self.newinput.setText('')

    def removetag(self, tag):
        # remove the count of the total wbirthdayget
        self.length -= 1
        # this case will delete the current tag
        oldtag = gettagbybirthday(self.birthday)
        newtag = oldtag.replace(' {}'.format(tag), '')
        updatebybirthday(self.birthday, tag=newtag)
        self.dbcon.commit()
        self.showtags(self.birthday)
        self.dbcon.commit()
        self.mainwindow.triggermodify(self.birthday, 'tag')

    def clear(self):
        # remove everything in this scroll
        widget = QWidget(self)
        self.setWidget(widget)


class RemovableButton(QWidget):
    def __init__(self, parent=None):
        super(RemovableButton, self).__init__(parent)
        self.parent = parent
        self.closebutton = QPushButton(self)
        self.closebutton.setFixedSize(15, 15)
        self.closebutton.setStyleSheet(removebuton)
        self.linkbutton = QPushButton(self)
        # remove background and make the word blue and underline
        self.linkbutton.setStyleSheet('''
        QPushButton{background-color: rgba(0, 0, 0, 0); color: blue; text-decoration: none; text-align: left; }
        QPushButton:hover{text-decoration: underline;}
        QPushButton:pressed{text-decoration: none;}''')

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.closebutton)
        hlayout.addWidget(self.linkbutton)
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hlayout)

        # signals
        self.linkbutton.clicked.connect(lambda: self.parent.newtab(self.linkbutton.text()))
        self.closebutton.clicked.connect(lambda: self.parent.removetag(self.linkbutton.text()))

    def setText(self, text):
        self.linkbutton.setText(text)
        # hide close button in certain situation
        if text == '#deleted' or text == '#like' or text == '#later':
            self.closebutton.hide()


class ButtonLink(QWidget):
    def __init__(self, parent=None):
        super(ButtonLink, self).__init__(parent)
        self.mainwindow = parent
        linkbutton = QPushButton(self)
        linkbutton.setFixedSize(15, 15)
        linkbutton.setStyleSheet(smallopenstyle)
        self.linkline = QLineEdit(self)
        self.linkline.setFont(QFont('Arial', 8))
        self.linkline.setStyleSheet(searchbarstyle)
        hly = QHBoxLayout(self)
        hly.setSpacing(1)
        hly.addWidget(linkbutton)
        hly.addWidget(self.linkline)
        hly.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(15)
        self.setLayout(hly)

        linkbutton.clicked.connect(self.openlink)
        self.linkline.textEdited.connect(self.updatelink)

    def openlink(self):
        if self.linkline.text() != '':
            os.system("start {}".format(self.linkline.text()))

    def updatelink(self):
        itembirthday = self.mainwindow.piclabel.birthday
        updatebybirthday(birthday=itembirthday, link=self.linkline.text())
        # update in table and images
        self.mainwindow.triggermodify(itembirthday, 'link')

class Grabber(QWidget):
    def __init__(self, mainwin=None):
        super(Grabber, self).__init__()
        self.mainwindow = mainwin
        self.dirty = True
        self.setWindowTitle('Grab a new thumbnail')
        self.resize(picwidth, picheight)
        # ensure that the widget always stays on top, no matter what
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        layout.setContentsMargins(3, 0, 2, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # create a "placeholder" widget for the screen grab geometry
        self.grabWidget = QWidget()
        layout.addWidget(self.grabWidget)
        self.grabButton = QPushButton('grab')
        layout.addWidget(self.grabButton)

        self.grabButton.clicked.connect(self.updatePixmap)

    def updateMask(self):
        # create mask
        frameRect = self.frameGeometry()

        # get the grabWidget geometry and remap it to global coordinates
        grabGeometry = self.grabWidget.geometry()
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))

        # get the actual margins between the grabWidget and the window margins
        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        # reset the geometries to get "0-point" rectangles for the mask
        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(0, 0))

        # create the base mask region, adjusted to the margins between the
        # grabWidget and the window as computed above
        region = QRegion(frameRect.adjusted(left, top, right, bottom))
        # "subtract" the grabWidget rectangle to get a mask that only contains
        # the window titlebar, margins and panel
        region -= QRegion(grabGeometry)
        self.setMask(region)

    def updatePixmap(self):
        left = self.pos().x()
        top = self.pos().y()+30
        width = self.size().width()
        height = self.size().height()-21
        width = min(width, int(height * picwidth / picheight))
        height = min(height, int(width * picheight / picwidth))

        region = {'left': left, 'top': top, 'width': width, 'height': height}

        with mss.mss() as sct:
            im = sct.grab(region)
            rawbytes = mss.tools.to_png(im.rgb, im.size)
            rawpixmap = byte2pixmap(rawbytes)
            pixmap_final = resizepixmap(rawpixmap, picwidth, picheight, 'top')
            try:
                itembirthday = self.mainwindow.piclabel.birthday
                # update database
                updatebybirthday(birthday=itembirthday, pixmap=pixmap2byte(pixmap_final))
                # update detailarea
                self.mainwindow.piclabel.setPixmap(pixmap_final)
                # update figures in maintab
                self.mainwindow.triggermodify(itembirthday, 'pixmap')
            except:
                pass

        self.close()

    def resizeEvent(self, event):
        super(Grabber, self).resizeEvent(event)
        # the first resizeEvent is called *before* any first-time showEvent and
        # paintEvent, there's no need to update the mask until then; see below
        if not self.dirty:
            self.updateMask()

    def paintEvent(self, event):
        super(Grabber, self).paintEvent(event)
        # on Linux the frameGeometry is actually updated "sometime" after show()
        # is called; on Windows and MacOS it *should* happen as soon as the first
        # non-spontaneous showEvent is called (programmatically called: showEvent
        # is also called whenever a window is restored after it has been
        # minimized); we can assume that all that has already happened as soon as
        # the first paintEvent is called; before then the window is flagged as
        # "dirty", meaning that there's no need to update its mask yet.
        # Once paintEvent has been called the first time, the geometries should
        # have been already updated, we can mark the geometries "clean" and then
        # actually apply the mask.
        if self.dirty:
            self.updateMask()
            self.dirty = False
