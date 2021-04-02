from webrelated import *
from stylesheetsum import *
from SQLiterelated import *
from constants import *
from PyQt5.QtWidgets import QApplication,QMenu, QHBoxLayout, QTextEdit, QLayout,QWidget,QLabel,QPushButton,QVBoxLayout, QTabWidget, QTextBrowser, QFileDialog, QSizePolicy,QTableWidget,QAbstractItemView
from PyQt5.QtCore import Qt,QRect, QSize, QPoint,QThread,QUrl
from PyQt5.QtGui import QCloseEvent, QCursor, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

###############Below are widgets for tab and its pages###############
class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super(FlowLayout, self).__init__(parent)
        self.oldfocusindex = 0
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(15)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    # slot function
    def highlight(self, newfocusindex):
        # clear the previous focus
        self.itemAt(self.oldfocusindex).widget().setStyleSheet(defaultpic)
        # focus on the new widget
        self.itemAt(newfocusindex).widget().setStyleSheet(highligtpic)
        # update the oldfocusindex
        self.oldfocusindex = newfocusindex

    # overwrite function
    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton,
                                                                Qt.Horizontal)
            # dynamic change Y spacing
            # spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton,
                                                                # Qt.Vertical)
            # fix the Y spacing
            spaceY = 30
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

class FLayoutHolder(QWidget):
    def __init__(self, parent = None):
        super(FLayoutHolder, self).__init__(parent)
        self.flayout = FlowLayout(self)
        self.setLayout(self.flayout)
        self.setContentsMargins(10, 10, 0, 0)

class ImageWidget(QLabel):
    def __init__(self, parent=None, glayout=None, birthday=0, link ='', linktype='unknown'):
        super(ImageWidget, self).__init__(parent)
        # some variable
        self.link = link
        self.linktype = linktype
        self.birthday = birthday  # birthday in the database
        self.index = -1  # index in the gridlayout
        self.dbcon = None
        # some object.
        self.glayout = glayout
        self.parent = parent
        self.setToolTip('birthday: {}'.format(self.birthday))

        # setup the layout
        self.setFixedSize(picwidth, picheight + 50)
        self.setAlignment(Qt.AlignTop)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet(defaultpic)

        # below are creating a textbrowser, set transparent/no boarder, set arial and 10 size
        self.title = QTextBrowser(self)
        self.title.setStyleSheet("QTextBrowser { background-color: rgba(0, 0, 0, 0); border: none}")
        self.title.setFont(QFont('Arial', 14))
        self.title.setFixedHeight(50)
        self.title.setFixedWidth(picwidth)
        self.title.move(0, picheight)

        # preview icon
        # if linktype == 'paper':
        #     self.previewbutton = PreviewButton(self, 'pdf')
        # else:
        self.previewbutton = PreviewButton(self, self.linktype)
        self.previewbutton.setFixedSize(40, 30)
        self.previewbutton.move(int(picwidth / 2)-20, int(picheight / 2)-15)
        self.previewbutton.hide()
        self.previewbutton.setToolTip('Preview')

        # some toolbar buttons
        self.linkbutton = QPushButton(self)
        self.linkbutton.setStyleSheet(openstyle)
        self.linkbutton.setFixedSize(25, 25)
        self.linkbutton.setToolTip('open')

        self.likebutton = QPushButton(self)
        self.likebutton.setFixedSize(25, 25)
        self.likebutton.setToolTip('like most')

        self.laterbutton = QPushButton(self)
        self.laterbutton.setFixedSize(25, 25)
        self.laterbutton.setToolTip('watch later')

        self.deletebutton = QPushButton(self)
        self.deletebutton.setFixedSize(25, 25)
        self.deletebutton.setToolTip('delete')

        self.downloadbutton = QPushButton(self)
        self.downloadbutton.setStyleSheet(downloadstyle)
        self.downloadbutton.setFixedSize(25,25)
        self.downloadbutton.setToolTip('download video')

        vbx = QVBoxLayout(self)
        vbx.addWidget(self.linkbutton)
        vbx.addWidget(self.likebutton)
        vbx.addWidget(self.laterbutton)
        vbx.addWidget(self.deletebutton)
        vbx.addWidget(self.downloadbutton)
        self.bar = QWidget(self)
        self.bar.setStyleSheet('background-color: None')
        self.bar.setLayout(vbx)
        self.bar.hide()

        # signal
        self.linkbutton.clicked.connect(self.openlink)
        self.likebutton.clicked.connect(self.changelike)
        self.laterbutton.clicked.connect(self.changelater)
        self.previewbutton.clicked.connect(self.showpreview)
        self.deletebutton.clicked.connect(self.deleterecover)
        self.downloadbutton.clicked.connect(self.download)

    # slot function
    def openlink(self):
        if istypeolvid(self.linktype) or self.linktype == 'web':
            os.system("start {}".format(self.link))
        else:
            os.startfile(self.link)

    def changelike(self):
        # check if #like tag is in. If in means like it
        orignaltag = gettagbybirthday(self.birthday)
        if '#like' not in orignaltag:
            # there is no #like tag, then add it
            newtag = orignaltag + ' #like'
            self.likebutton.setStyleSheet(likestyle)
        else:
            # there is #like tage, then deleted its
            newtag = orignaltag.replace(' #like', '')
            self.likebutton.setStyleSheet(unlikestyle)
        updatebybirthday(birthday=self.birthday, tag=newtag)
        self.dbcon.commit()
        self.parent.triggermodify(self.birthday, 'tag')
        # check if we need to update #like in the tagarea
        if self.parent.tagarea.birthday == self.birthday:
            self.parent.tagarea.showtags(self.birthday)

    def changelater(self):
        # check if #like tag is in. If in means like it
        orignaltag = gettagbybirthday(self.birthday)
        if '#later' not in orignaltag:
            # there is no #like tag, then add it
            newtag = orignaltag + ' #later'
            self.laterbutton.setStyleSheet(laterstyle)
        else:
            # there is #later tage, then deleted its
            newtag = orignaltag.replace(' #later', '')
            self.laterbutton.setStyleSheet(unlaterstyle)
        updatebybirthday(birthday=self.birthday, tag=newtag)
        self.dbcon.commit()
        self.parent.triggermodify(self.birthday, 'tag')
        # check if we need to update #later in the tagarea
        if self.parent.tagarea.birthday == self.birthday:
            self.parent.tagarea.showtags(self.birthday)

    def deleterecover(self):
        orignaltag = gettagbybirthday(self.birthday)
        if '#deleted' not in orignaltag:
            self.deletebutton.setStyleSheet(recoverstyle)
            deletebybirthday(self.birthday)
        else:

            self.deletebutton.setStyleSheet(todeletestyle)
            recoverbybirthday(self.birthday)
        self.dbcon.commit()
        self.parent.triggermodify(self.birthday, 'tag')
        # check if we need to update #deleted in the tagarea
        if self.parent.tagarea.birthday == self.birthday:
            self.parent.tagarea.showtags(self.birthday)

    def download(self):
        if istypeolvid(self.linktype):
            folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '/')
            if folder != '':
                self.work = BkgrndThread(self, link=self.link, path=folder)
                self.work.start()
            return
        elif self.linktype == 'paper':
            try:
                document = requests.get(self.link, headers=headers).content
                filename = savabletitle(self.title.toPlainText())
                filepath = QFileDialog.getSaveFileName(self, 'Save paper', '{}.pdf'.format(filename), 'PDF (*.pdf)')[0]
                if filepath != '':
                    with open(filepath, 'wb') as f:
                        f.write(document)
            except:
                pass

    def showpreview(self):
        self.previewwindow = WebPreview()
        self.previewwindow.preview(self.link, self.linktype)
        self.previewwindow.show()
        # a popup window to show the preview of the link

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            # when left mouse clicked do the following
            # focus on this widget
            self.glayout.highlight(self.index)
            # show all the tags of this widget
            self.parent.tagarea.showtags(self.birthday)
            # show comment into the tagarea
            self.parent.commentarea.showcomment(self.birthday)
            # show the pic in the piclabel
            self.parent.piclabel.showpixandtitle(self.birthday)
            # set the link
            self.parent.linkline.linkline.setText(self.link)
            self.parent.toolarea.show()

    # overwrite function
    def enterEvent(self, *args, **kwargs):
        # mouse enter, then show toolbar
        self.bar.show()
        # since toolbar is shown, check if it is a liked video
        tag = gettagbybirthday(self.birthday)
        if '#like' in tag:
            self.likebutton.setStyleSheet(likestyle)
        else:
            self.likebutton.setStyleSheet(unlikestyle)
        # then check if it is a later video
        if '#later' in tag:
            self.laterbutton.setStyleSheet(laterstyle)
        else:
            self.laterbutton.setStyleSheet(unlaterstyle)
        # then check if it is a deleted video
        if '#deleted' in tag:
            self.deletebutton.setStyleSheet(recoverstyle)
        else:
            self.deletebutton.setStyleSheet(todeletestyle)


        title = gettitlebybirthday(self.birthday)
        if title != self.title.toPlainText():
            self.title.setText(title)

        if istypeexist(self.linktype):
            self.previewbutton.show()

    def leaveEvent(self, *args, **kwargs):
        self.bar.hide()
        self.previewbutton.hide()

class PreviewButton(QPushButton):
    def __init__(self, parent=None, linktype = 'unknown'):
        super(PreviewButton, self).__init__(parent)
        self.parent = parent
        try:
            self.setStyleSheet(previewicon(linktype))
        except:
            pass

    def enterEvent(self, *args, **kwargs):
        self.setCursor(QCursor(Qt.PointingHandCursor))
    def leaveEvent(self, *args, **kwargs):
        self.setCursor(QCursor(Qt.ArrowCursor))

class WebPreview(QWebEngineView):
    def __init__(self, parent=None):
        super(WebPreview, self).__init__(parent)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.resize(1000, 900)

    def preview(self, link, linktype):
        if linktype == 'pdf' or linktype == 'paper':
            self.load(QUrl.fromUserInput('{}?file={}'.format(PDFJS, link)))
        else:
            self.load(QUrl(link))

class Table(QTableWidget):
    def __init__(self, parent = None):
        super(Table, self).__init__(parent)

        self.parent = parent
        self.iseditmode = False
        self.loadfinished = False
        self.setStyleSheet('border:None')
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['title', 'link', 'tag', 'comment','birthday'])
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.verticalHeader().setFixedWidth(20)

        self.setColumnWidth(0, 350)
        self.setColumnWidth(1, 208)
        self.setColumnWidth(2, 400)
        self.setColumnWidth(3, 800)
        self.setColumnWidth(4, 105)

        # create a menu
        self.menu = QMenu(self)
        self.action1 = self.menu.addAction(u'like')
        self.action1.setCheckable(True)
        self.action2 = self.menu.addAction(u'watch later')
        self.action2.setCheckable(True)
        self.action3 = self.menu.addAction(u'delete')
        self.action3.setCheckable(True)
        self.action4 = self.menu.addAction(u'open')
        self.action5 = self.menu.addAction(u'preview')
        # preview window
        self.currentCellChanged.connect(self.updaterightarea)
        self.customContextMenuRequested.connect(self.generateMenu)

    def updaterightarea(self,currentRow,currentColumn,previousRow, previousColumn):
        if currentRow != previousRow:
            # if we swap row, then we trigger right area
            birthday = int(self.item(currentRow,4).text())
            if birthday != self.parent.tagarea.birthday:
                # show all the tags of this widget
                self.parent.tagarea.showtags(birthday)
                # show comment into the tagarea
                self.parent.commentarea.showcomment(birthday)
                # show the pic annd title in the piclabel
                self.parent.piclabel.showpixandtitle(birthday)
                # set the link
                link = getlinkbybirthday(birthday)
                self.parent.linkline.linkline.setText(link)


    def generateMenu(self, pos):
        row = self.currentRow()
        if row != -1:
            birthday = int(self.item(row,4).text())
            link = self.item(row,1).text()
            linktype = self.item(row, 2).text().split(' ')[0]# linktype is the first tag
            self.action5.setEnabled(istypeexist(linktype))
            orignaltag = gettagbybirthday(birthday)
            isliked = '#like' in orignaltag
            islater = '#later' in orignaltag
            isdeleted = '#deleted' in orignaltag
            self.action1.setChecked(isliked)
            self.action2.setChecked(islater)
            self.action3.setChecked(isdeleted)
            self.action = self.menu.exec(self.mapToGlobal(pos))
            if self.action == self.action1:
                if isliked:
                    # there is #like tage, then deleted its
                    newtag = orignaltag.replace(' #like', '')
                    # self.item(row,3).setText(orignaltag.replace(' #like', ''))
                else:
                    # there is no #like tag, then add it
                    newtag = orignaltag + ' #like'
                    # self.item(row,3).setText(orignaltag + ' #like')
                updatebybirthday(birthday=birthday, tag=newtag)
                # update the interface anywhere contain this tag
                self.parent.triggermodify(birthday, 'tag')
                # check if we need to update #like in the tagarea
                if self.parent.tagarea.birthday == birthday:
                    self.parent.tagarea.showtags(birthday)

            elif self.action == self.action2:
                if islater:
                    # there is #later tage, then deleted its
                    newtag = orignaltag.replace(' #later', '')
                else:
                    # there is no #later tag, then add it
                    newtag = orignaltag + ' #later'
                updatebybirthday(birthday=birthday, tag=newtag)
                 # update the interface anywhere contain this tag
                self.parent.triggermodify(birthday, 'tag')
                # check if we need to update #later in the tagarea
                if self.parent.tagarea.birthday == birthday:
                    self.parent.tagarea.showtags(birthday)

            elif self.action == self.action3:
                if isdeleted:
                    recoverbybirthday(birthday)
                else:
                    deletebybirthday(birthday)
                # update the interface anywhere contain this tag
                self.parent.triggermodify(birthday, 'tag')
                # check if we need to update #deleted in the tagarea
                if self.parent.tagarea.birthday == birthday:
                    self.parent.tagarea.showtags(birthday)

            elif self.action == self.action4:
                if linktype == 'web' or linktype == 'youtube' or linktype == 'bilibili':
                    os.system("start {}".format(link))
                else:
                    os.startfile(link)

            elif self.action == self.action5:
                self.previewwindow = WebPreview()
                self.previewwindow.preview(link,linktype)
                self.previewwindow.show()

    def enterEvent(self, *args, **kwargs):
        self.iseditmode = True

    def leaveEvent(self, *args, **kwargs):
        focused_widget = QApplication.focusWidget()
        self.iseditmode = isinstance(focused_widget, QTableWidget)

class TabPage(QWidget):
    def __init__(self, parent, imagepage, tablepage):
        super(TabPage, self).__init__(parent)
        self.imagepage = imagepage
        self.tablepage = tablepage
        # self.tablepage.hide()
        # self.imagepage.hide()

        button1 = QPushButton(self)
        button1.setFixedSize(20,20)
        button1.setStyleSheet(imageversion)
        button2 = QPushButton(self)
        button2.setFixedSize(20,20)
        button2.setStyleSheet(tableversion)
        self.gap = QLabel(self)
        self.gap.setStyleSheet('background-color: #F0F0F0;')

        hlyout = QHBoxLayout()
        hlyout.setContentsMargins(0,0,0,0)
        hlyout.addWidget(self.gap)
        hlyout.addWidget(button1)
        hlyout.addWidget(button2)
        hlyout.setSpacing(0)
        hlyout2 = QHBoxLayout()
        hlyout2.setContentsMargins(0, 0, 0, 0)
        hlyout2.addWidget(imagepage)
        hlyout2.addWidget(tablepage)
        vlyout = QVBoxLayout()
        vlyout.setSpacing(0)
        vlyout.setContentsMargins(0, 0, 0, 0)
        vlyout.addLayout(hlyout)
        vlyout.addLayout(hlyout2)
        self.setLayout(vlyout)

        # signals
        button1.clicked.connect(self.hidetable)
        button2.clicked.connect(self.hideimage)

        # highlight image and auto highlight the same data in table

    def hidetable(self):
        self.imagepage.show()
        self.tablepage.hide()

    def hideimage(self):
        self.imagepage.hide()
        self.tablepage.show()

class MainTab(QTabWidget):
    def __init__(self, parent=None):
        super(MainTab, self).__init__(parent)
        self.mainwindow = parent
        self.setTabsClosable(True)
        # close page once the close button is clicked. and deleted the unwanted list in birthdaylistsum
        self.tabCloseRequested.connect(self.updatelist)

    def updatelist(self, index):
        self.removeTab(index)
        del self.mainwindow.birthdaylistsum[index]


class BkgrndThread(QThread):
    def __init__(self, parent=None, link='', path=''):
        super(BkgrndThread, self).__init__(parent)
        self.link = link
        self.folderpath = path

    def run(self):
        downloadvideo(self.link, self.folderpath)
        self.quit()
