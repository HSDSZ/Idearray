from settings import *
from tabcontent import *
from titlebar import *
from detailsarea import *
import fitz
from PyQt5.QtWidgets import QMainWindow,QSizeGrip,QListWidget,QCheckBox,QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtGui import QImage,QIcon,QIntValidator
import mss

class Mywindow(QMainWindow):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.move(50, 50)
        self.setWindowIcon(QIcon(':HSDSZ.ico'))
        self.birthdaylistsum = []
        self.initUI()
        # self.dbcon = QSqlDatabase.addDatabase("QSQLITE")

        # import configuration

        # self.resize(startupwidth,startupheight)
        # connect to database
        self.dbpath = startupDBpath
        self.dbcon = QSqlDatabase.addDatabase("QSQLITE")
        self.dbcon.setDatabaseName(self.dbpath)
        self.dbcon.open()
        createtable()
        self.dbcon.commit()

        # hidden windows
        self.tempengine = Webengine(self.dbcon, self.piclabel)  #used to screenshot web
        self.grabwin = Grabber(self)
        self.settingwin = SettingWindow()

        self.settingwin.page1.le2.setText(startupDBpath)
        self.settingwin.page1.le.setText(startupDBpath)
        self.settingwin.page1.widthle.setText(str(startupwidth))
        self.settingwin.page1.check1.setChecked(startuplook)
        self.settingwin.page1.heightle.setText(str(startupheight))
        self.settingwin.page2.taglist.addItems(alltaginhierarchy())
        # singals
        self.settingwin.page1.bt.clicked.connect(self.chooseDB)
        self.settingwin.page1.bt2.clicked.connect(self.newDB)

        # update all children widget with the DB connection
        self.titlebar.searchbar.completer.alltags = getalltags()
        self.commentarea.dbcon = self.dbcon
        self.tagarea.dbcon = self.dbcon

        # signal
        self.titlebar.searchbar.returnPressed.connect(self.actionmade)
        self.titlebar.searchbar.dropped.connect(self.handledropped)
        self.piclabel.capturebutton.clicked.connect(self.grabwin.show)

    def initUI(self):
        self.setWindowTitle("idearray")

        # titlebar and maintab
        self.titlebar = TitleBar(self)
        self.maintab = MainTab(self)
        self.maintab.setMinimumWidth(picwidth + 30)
        # self.maintab.setStyleSheet('background-color: rgb(0,0,0,100)')

        # right tag and comment area
        self.piclabel = PixmapArea(self)
        self.tagarea = TagArea(parent=self)
        self.tagarea.setFixedWidth(picwidth)
        self.commentarea = CommentArea(parent=self)
        self.commentarea.setFixedSize(picwidth, 100)
        self.commentarea.setPlaceholderText('Here presents your comment')
        self.commentarea.setStyleSheet('border: none')
        self.linkline = ButtonLink(parent=self)

        # set the hlayout to place tag and comment area
        v2layout = QVBoxLayout()
        v2layout.addWidget(self.piclabel)
        v2layout.addWidget(self.tagarea)
        v2layout.addWidget(self.commentarea)
        v2layout.addWidget(self.linkline)
        v2layout.setContentsMargins(0, 0, 0, 0)

        self.toolarea = QWidget(self)
        self.toolarea.setLayout(v2layout)
        self.toolarea.setFixedWidth(picwidth)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.maintab)
        hlayout.addWidget(self.toolarea)
        hlayout.setSpacing(0)
        self.belowwidget = QWidget(self)
        self.belowwidget.setLayout(hlayout)

        # set the layout of the control
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.titlebar)
        vlayout.addWidget(self.belowwidget)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        # display the layout
        frame = QWidget()
        frame.setLayout(vlayout)
        self.setCentralWidget(frame)
        self.setMinimumWidth(picwidth + 10)

        self.titlebar.mode = 'bar'
        self.belowwidget.hide()
        self.toolarea.hide()
        self.resize(100, 10)
        self.titlebar.maxbutton.setStyleSheet(originmode)

        # add grip to resize
        self._gripSize = 5
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge),
            SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge),
            SideGrip(self, Qt.BottomEdge),
        ]
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.cornerGrips = [QSizeGrip(self) for i in range(4)]

    def triggermodify(self, birthday, source='title'):
        for i in range(len(self.birthdaylistsum)):
            birthdaylist = self.birthdaylistsum[i]
            if birthday in birthdaylist:
                # get the index of the birthday in the birthdaylist
                index = birthdaylist.index(birthday)
                # get the table and image widget
                tabpage = self.maintab.widget(i)
                # get table
                tablepage = tabpage.tablepage
                # get flayout holder
                holder = tabpage.imagepage.widget()
                # get the specific image widget
                widget = holder.flayout.itemAt(index).widget()

                # update tables
                if source == 'title':
                    newtitle = gettitlebybirthday(birthday)
                    tablepage.item(index,0).setText(newtitle)
                    widget.title.setText(newtitle)
                elif source == 'link':
                    newlink = getlinkbybirthday(birthday)
                    tablepage.item(index,1).setText(newlink)
                    widget.link = newlink
                elif source == 'pixmap':
                    newpixmap = getpixmapbybirthday(birthday)
                    widget.setPixmap(byte2pixmap(newpixmap))
                elif source == 'comment':
                    newcomment = getcommentbybirthday(birthday)
                    tablepage.item(index,3).setText(newcomment)
                elif source == 'tag':
                    newtag = gettagbybirthday(birthday)
                    tablepage.item(index, 2).setText(newtag)
                else:
                    pass


    # slot functions
    def chooseDB(self):
        oldpath = self.dbpath
        self.settingwin.hide()
        self.dbpath = QFileDialog.getOpenFileName(self,'Open a database','.','(*.db)')[0]
        self.settingwin.show()
        if self.dbpath != '' and oldpath != self.dbpath:
            self.settingwin.page1.le2.setText(self.dbpath)
            self.dbcon.setDatabaseName(self.dbpath)
            self.dbcon.open()
            self.maintab.clear()
            # new db selected, reset everything
            self.maintab.clear()
            self.piclabel.clear()
            self.piclabel.title.clear()
            self.tagarea.showtagsbylist([])
            self.linkline.linkline.clear()
            self.birthdaylistsum = []

    def newDB(self):
        oldpath = self.dbpath
        self.settingwin.hide()
        self.dbpath = QFileDialog.getSaveFileName(self, 'Create a database', '.', '(*.db)')[0]
        self.settingwin.show()
        if self.dbpath != '' and oldpath != self.dbpath:
            self.settingwin.page1.le2.setText(self.dbpath)
            self.dbcon.setDatabaseName(self.dbpath)
            self.dbcon.open()
            # create table
            createtable()
            self.dbcon.commit()
            # new db selected, reset everything
            self.maintab.clear()
            self.piclabel.clear()
            self.piclabel.title.clear()
            self.tagarea.showtagsbylist([])
            self.linkline.linkline.clear()
            self.birthdaylistsum = []

    def actionmade(self):
        # get the page title from the searchbar. only show the first 5 letters
        fulltext = self.titlebar.searchbar.text()

        if fulltext == '#setting' or fulltext == '#settings':
            # if you input a #settings, you pop up a setting window
            self.settingwin.show()
        elif fulltext == '':
            pass
        else:
            if self.titlebar.mode == 'bar':
                self.titlebar.swithcmodeto('normal')
            # if you input other than #setting, you do add tab
            # pagetitle is the words appear on the tab
            pagetitle = fulltext if len(fulltext) <= 5 else fulltext[0:5] + "..."
            # clear the searchbar afterwards
            # self.titlebar.searchbar.setText('')
            # create a blank page to show the image viewport
            imagepage = QScrollArea()
            imagepage.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            imagepage.setWidgetResizable(True)
            imagepage.setStyleSheet('border:None')
            # create flowlayout and put this flowlayout into the imagepage
            holder = FLayoutHolder()
            imagepage.setWidget(holder)
            # create a blank table to show the
            tablepage = Table(self)

            # emerge them into a tab page and insert into tab
            tabpage = TabPage(parent=self, imagepage=imagepage, tablepage=tablepage)
            tabpage.gap.setText(fulltext)
            self.maintab.addTab(tabpage, pagetitle)
            self.maintab.setCurrentIndex(self.maintab.count()-1)
            if self.settingwin.page1.check1.checkState() == 2:
                imagepage.show()
                tablepage.hide()
            else:
                imagepage.hide()
                tablepage.show()

            # fetch the searched result from DB and put them into image and tablepage
            operation = operation_getbytag3(fulltext)
            query = QSqlQuery()
            query.exec(operation)
            birthdaylist = []
            i = 0
            while query.next():
                # get the birthday, title, link, comment, tag
                birthday = query.value(0)
                birthdaylist.append(birthday)
                title = query.value(1)
                link = query.value(2)
                comment = query.value(3)
                tag = query.value(4)
                # linktype = getlinktype(link)# the first tag is the type
                linktype = tag.split(' ')[0]
                pixmap = query.value(5) if query.value(5) != '' else authorpage
                # create a widget to be added
                singleimageitem = ImageWidget(self, holder.flayout, birthday, link, linktype)
                singleimageitem.title.setText(title)
                singleimageitem.index = i
                singleimageitem.dbcon = self.dbcon
                # singleimageitem.birthday = birthday
                singleimageitem.comment = comment
                singleimageitem.setPixmap(byte2pixmap(pixmap))
                # singleimageitem.setPixmap(pixmap)
                # insert into flayout
                holder.flayout.addWidget(singleimageitem)
                # this processevent is used to show image one by one

                tablepage.insertRow(i)
                singletableitem = QTableWidgetItem(str(birthday))
                singletableitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                singletableitem.setTextAlignment(Qt.AlignRight)
                tablepage.setItem(i, 4, singletableitem)
                singletableitem = QTableWidgetItem(title)
                singletableitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                tablepage.setItem(i, 0, singletableitem)
                singletableitem = QTableWidgetItem(link)
                singletableitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                tablepage.setItem(i, 1, singletableitem)
                singletableitem = QTableWidgetItem(tag)
                singletableitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                tablepage.setItem(i, 2, singletableitem)
                singletableitem = QTableWidgetItem(comment)
                singletableitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                tablepage.setItem(i, 3, singletableitem)

                QApplication.processEvents()
                i += 1
            tablepage.loadfinished = True
            self.birthdaylistsum.append(birthdaylist)

    # this slot function response to a custom dropped event. That event emit dragtext
    def handledropped(self, dragtext):
        # show mainwindow right detail area
        currentmode = self.titlebar.mode
        if currentmode == 'bar':
            self.titlebar.swithcmodeto('detail')

        # get the birthday, link, linktype, these shared content. set link
        birthday = now()
        linktype, doi, pdflink = getlinktype(dragtext)
        link = refinelink(dragtext, linktype)
        self.linkline.linkline.setText(link)
        self.piclabel.birthday = birthday
        self.tagarea.birthday = birthday
        self.commentarea.birthday = birthday

        # set title
        if linktype == 'pdf':
            document = fitz.open(link)
            linktitle = getlinktitle(link,linktype,document)
        else:
            linktitle = getlinktitle(link,linktype)
        self.piclabel.title.setText(linktitle)

        # set tags and update alltag in the searchbar completer
        if linktype == 'paper':
            tagstr, taglist = titletotags('paper {}'.format(doi), linktitle)
        else:
            tagstr, taglist = titletotags(linktype, linktitle)

        self.tagarea.showtagsbylist(taglist)
        for item in taglist:
            if item not in self.titlebar.searchbar.completer.alltags:
                self.titlebar.searchbar.completer.alltags += [item]

        # set comment
        self.commentarea.setText('')
        # process them and add them into database
        QApplication.processEvents()

        # add data into db
        if linktype == 'paper':
            adddatawithoutpix(birthday, linktitle, pdflink, '', tagstr)
        else:
            adddatawithoutpix(birthday, linktitle, link, '', tagstr)

        self.dbcon.commit()

        # set pixmap to qlabel and save this new pixmap to database
        if linktype == 'web' or linktype == 'paper':
            self.piclabel.setPixmap(QPixmap(':loading.png'))
            self.tempengine.setZoomFactor(0.3)
            self.tempengine.show()
            self.tempengine.birthday = birthday
            self.tempengine.load(QUrl(link))
        elif linktype == 'pdf':
            # screenshot the first page
            page1 = document[0]# first page
            pix = page1.getPixmap(alpha = False)
            # convert into qpix and resize
            qimage=QImage(pix.samples,pix.width, pix.height,pix.stride,QImage.Format_RGB888)
            rawpixmap = QPixmap.fromImage(qimage)
            qpixmap = resizepixmap(rawpixmap,picwidth,picheight, area = 'top')
            bytedata = pixmap2byte(qpixmap)
            # save into db
            self.piclabel.setPixmap(qpixmap)
            updatebybirthday(birthday=birthday, title=linktitle, pixmap=bytedata)
            self.dbcon.commit()
        elif linktype == 'image':
            pixmap = QPixmap(link)
            pixmap = resizepixmap(pixmap,picwidth,picheight)
            self.piclabel.setPixmap(pixmap)
            # insert data into the db base
            bytedata = pixmap2byte(pixmap)
            updatebybirthday(birthday=birthday, pixmap=bytedata)
            self.dbcon.commit()
        elif istypeolvid(linktype):
            pixmap = videothumb(link, linktype, picwidth, picheight)
            self.piclabel.setPixmap(pixmap)
            # insert data into the db base
            bytedata = pixmap2byte(pixmap)
            updatebybirthday(birthday=birthday, pixmap=bytedata)
            self.dbcon.commit()
        else:
            # different file type
            pixmap = QPixmap(':filethumb.png')
            self.piclabel.setPixmap(pixmap)
            updatebybirthday(birthday=birthday, pixmap=pixmap2byte(pixmap))
            self.dbcon.commit()

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(
            QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(
            QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(
            QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.updateGrips()

#################Below are widgets for the mainwindow################
class SideGrip(QWidget):
    def __init__(self, parent, edge):
        QWidget.__init__(self, parent)
        if edge == Qt.LeftEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == Qt.TopEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == Qt.RightEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None

class Webengine(QWebEngineView):
    def __init__(self, dbcon, piclabel):
        super(Webengine, self).__init__()
        self.loadcount = 0
        self.dbcon = dbcon
        self.qlabel = piclabel
        self.setFixedSize(picwidth, picheight)
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        self.page().settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.page().settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.loadFinished.connect(self.loadtopiclabel)

    def loadtopiclabel(self):
        # take a screenshot of the web
        pixmap = self.grab()
        self.qlabel.setPixmap(pixmap)
        # qlabel to bytedata
        bytedata = pixmap2byte(pixmap)
        updatebybirthday(birthday=self.birthday, pixmap=bytedata)
        self.dbcon.commit()
        self.close()

class SettingWindow(QWidget):
    def __init__(self,parent = None):
        super(SettingWindow, self).__init__(parent)

        self.setWindowFlags(Qt.WindowCloseButtonHint| Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        # self.setFixedSize(700,500)
        self.setWindowTitle('Settings (Auto save)')
        self.setWindowIcon(QIcon(':HSDSZ.ico'))

        # set tab
        self.tab = QTabWidget(self)
        self.tab.tabBar().hide()
        # page 1
        self.page1 = BasicSetPage(self)
        self.tab.addTab(self.page1, 'basic')
        # page 2
        self.page2 = HierachyPage(self)
        self.tab.addTab(self.page2, 'Hierachy')

        #Set list
        settinglist = QListWidget(self)
        settinglist.addItems(['Basic','Hierachy'])
        settinglist.setFixedWidth(70)
        settinglist.setStyleSheet('''QListWidget
                                    {border-width: 1px;
                                     border-color: rgba(100,100,100,80);
                                     border-style: outset;}''')
        settinglist.currentRowChanged.connect(self.tabswitched)
        # layout them
        hlyout = QHBoxLayout()
        hlyout.setContentsMargins(2,2,2,2)
        hlyout.setSpacing(2)
        hlyout.addWidget(settinglist)
        hlyout.addWidget(self.tab)
        self.setLayout(hlyout)

    def tabswitched(self, currentRow):
        self.tab.setCurrentIndex(currentRow)

class BasicSetPage(QWidget):
    def __init__(self, parent = None):
        super(BasicSetPage, self).__init__(parent)
        self.parent = parent
        # page 1
        self.bt = QPushButton('Choose database')
        self.bt2 = QPushButton('New database')
        gap_row1 = QLabel()
        gap_row1.setFixedWidth(300)
        hlyout_row1 = QHBoxLayout()
        hlyout_row1.setContentsMargins(0,0,0,0)
        hlyout_row1.addWidget(self.bt)
        hlyout_row1.addWidget(self.bt2)
        hlyout_row1.addWidget(gap_row1)

        lb2 = QLabel('Current database')
        self.le2 = QLineEdit()
        self.le2.setEnabled(False)
        hlyout_row2 = QHBoxLayout()
        hlyout_row2.addWidget(lb2)
        hlyout_row2.addWidget(self.le2)
        hlyout_row2.setContentsMargins(0,0,0,0)

        self.bt3 = QPushButton('Set startup database')
        self.bt3.setFixedWidth(180)
        gap_row3 = QLabel()
        hlyout_row3 = QHBoxLayout()
        hlyout_row3.addWidget(self.bt3)
        hlyout_row3.addWidget(gap_row3)
        hlyout_row3.setContentsMargins(0,0,0,0)

        lb = QLabel('Startup database')
        self.le = QLineEdit()
        self.le.setEnabled(False)
        hlyout_row4 = QHBoxLayout()
        hlyout_row4.addWidget(lb)
        hlyout_row4.addWidget(self.le)
        hlyout_row4.setContentsMargins(0,0,0,0)

        lb3 = QLabel('Startup window size.')

        lb4 = QLabel(' width:')
        self.widthle = QLineEdit()
        self.widthle.setValidator(QIntValidator())
        lb5 = QLabel('height')
        self.heightle = QLineEdit()
        self.heightle.setValidator(QIntValidator())
        hlyout_row5 = QHBoxLayout()
        hlyout_row5.addWidget(lb4)
        hlyout_row5.addWidget(self.widthle)
        hlyout_row5.addWidget(lb5)
        hlyout_row5.addWidget(self.heightle)
        hlyout_row5.setContentsMargins(0,0,0,0)

        lb6 = QLabel('Startup look')
        self.check1 = QCheckBox('Image version')
        self.check1.setChecked(True)
        self.check2 = QCheckBox('Table version')
        hlyout_row_checkbox = QHBoxLayout()
        hlyout_row_checkbox.addWidget(self.check1)
        hlyout_row_checkbox.addWidget(self.check2)

        vlyout = QVBoxLayout()
        vlyout.setSpacing(5)
        vlyout.addLayout(hlyout_row1)
        vlyout.addLayout(hlyout_row2)
        rowgap = QLabel()
        rowgap.setFixedHeight(20)
        vlyout.addWidget(rowgap)
        vlyout.addLayout(hlyout_row3)
        vlyout.addLayout(hlyout_row4)
        vlyout.addWidget(rowgap)
        vlyout.addWidget(lb3)
        vlyout.addLayout(hlyout_row5)
        vlyout.addWidget(rowgap)
        vlyout.addWidget(lb6)
        vlyout.addLayout(hlyout_row_checkbox)
        gap = QLabel()
        gap.setFixedHeight(200)
        vlyout.addWidget(gap)
        hlyout_row_reset = QHBoxLayout()
        reset = QPushButton('Reset')
        gap_row6 = QLabel()
        gap_row6.setFixedWidth(200)
        hlyout_row_reset.addWidget(reset)
        hlyout_row_reset.addWidget(gap_row6)
        vlyout.addLayout(hlyout_row_reset)

        self.setLayout(vlyout)

        self.bt3.clicked.connect(self.startupDB)
        self.widthle.textEdited.connect(self.updatewidth)
        self.heightle.textEdited.connect(self.updateheight)
        reset.clicked.connect(self.settingreset)
        self.check1.stateChanged.connect(self.check1clicked)
        self.check2.stateChanged.connect(self.check2clicked)

    def startupDB(self):
        startupDBpath = QFileDialog.getOpenFileName(self,'Startup database','.','(*.db)')[0]
        if startupDBpath != '':
            self.le.setText(startupDBpath)
            updateconfig('startupDB',startupDBpath)

    def updatewidth(self,a0):
        updateconfig('startupwidth',int(a0))

    def updateheight(self,a0):
        updateconfig('startupheight',int(a0))

    def settingreset(self):
        defaultconfig()
        self.widthle.setText(str(defaultdict['startupwidth']))
        self.heightle.setText(str(defaultdict['startupheight']))
        self.le.setText(defaultdict['startupDB'])
        self.check1.setChecked(True)

    def check1clicked(self):
        check1state = self.check1.checkState()
        self.check2.setChecked(not check1state)
        updateconfig('startuplook',check1state == 2)

    def check2clicked(self):
        self.check1.setChecked(not self.check2.checkState())
        updateconfig('startuplook',self.check1.checkState() == 2)

class HierachyPage(QWidget):
    def __init__(self, parent = None):
        super(HierachyPage, self).__init__(parent)
        label0 = QLabel('Tag')
        label0.setFixedWidth(60)
        deletebutton = QPushButton()
        deletebutton.setStyleSheet(deletehierarchy)
        deletebutton.setFixedSize(15,15)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText('Search or enter to create new')
        # self.searchbar.returnPressed.connect(self.searchbarenter)

        self.demon = QLabel()

        self.taglist = QListWidget()
        self.taglist.setSortingEnabled(True)
        # self.list.itemClicked.connect(self.showchildrenparent)
        label1 = QLabel('Childen tags')
        label1.setWordWrap(True)
        self.childentext = QLineEdit()
        label2 = QLabel('Parent Tags')
        label2.setWordWrap(True)
        self.parenttext = QLineEdit()

        # layout
        hlyout0 = QHBoxLayout()
        hlyout0.addWidget(label0)
        hlyout0.addWidget(self.searchbar)
        hlyout0.addWidget(deletebutton)
        vlyout0 = QVBoxLayout()
        vlyout0.addLayout(hlyout0)
        vlyout0.addWidget(self.taglist)

        hlayout1 = QHBoxLayout()
        hlayout1.addLayout(vlyout0)
        hlayout1.addWidget(self.demon)


        vlyout1 = QVBoxLayout()
        vlyout1.addLayout(hlayout1)
        vlyout1.addWidget(label1)
        vlyout1.addWidget(self.childentext)
        vlyout1.addWidget(label2)
        vlyout1.addWidget(self.parenttext)
        # hlyout1.setSpacing(10)
        self.setLayout(vlyout1)

        self.taglist.itemClicked.connect(self.showchildrenparent)
        self.searchbar.returnPressed.connect(self.search)
        deletebutton.clicked.connect(self.deleteitem)
        self.childentext.editingFinished.connect(self.modifychildren)
        self.parenttext.editingFinished.connect(self.modifyparent)

    def showchildrenparent(self,item):

        itemtext = item.text()
        children = searchchildren(itemtext)[1]
        self.childentext.setText(children)
        parents = searchparent(itemtext)
        self.parenttext.setText(parents)

    def search(self):
        # get the text from searchbar
        search_text = self.searchbar.text()
        # search the children, if not exist, then create one
        isexist, children = searchchildren(search_text)
        if not isexist:
            self.taglist.addItem(search_text.lower())
        self.childentext.setText(children)
        # search parents
        parents = searchparent(search_text)
        self.parenttext.setText(parents)

        item = self.taglist.findItems(search_text, Qt.MatchExactly)[0]
        self.taglist.setCurrentItem(item)

    def deleteitem(self):
        row = self.taglist.currentRow()
        if row != -1:
            text = self.taglist.currentItem().text()
            query = QSqlQuery()
            query.exec("DELETE FROM hierarchy WHERE tag='{}'".format(text))
            self.taglist.takeItem(row)

    def modifychildren(self):
        if self.taglist.currentRow() != -1:
            parenttag = self.taglist.currentItem().text()
            children = self.childentext.text()
            newchildrenlist = children.split()
            newchildren = ' '.join(newchildrenlist)
            updatechilderen(parenttag,newchildren)

    def modifyparent(self):
        tag = self.taglist.currentItem().text()
        oldtext = searchparent(tag)
        oldlist = oldtext.split()

        newlist = self.parenttext.text().split()

        toremoveset = set(oldlist).difference(set(newlist))
        toremovelist = list(toremoveset)
        toaddset = set(newlist).difference(set(oldlist))
        toaddlist = list(toaddset)

        for parent in toremovelist:
            removeparent(tag,parent)
            self.taglist.clear()
            self.taglist.addItems(alltaginhierarchy())
        for parent in toaddlist:
            addparent(tag,parent)
            self.taglist.clear()
            self.taglist.addItems(alltaginhierarchy())




if __name__ == "__main__":
    # picwidth, picheight = [320, 180]
    # PDFJS = 'file:///./pdfjs/web/viewer.html'

    buildwindow(Mywindow)
