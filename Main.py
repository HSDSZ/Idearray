from QTrelated import *
from SQLiterelated import *
from Webrelated import *
from StyleSheetSum import *
from Settings import *
import os
import fitz
from PyQt5.QtWidgets import QWidget, QMainWindow, QCompleter, QVBoxLayout, QLineEdit, QTabWidget, QScrollArea,QGridLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit, QTextBrowser, QMenu, QLayout, QFileDialog, QSizePolicy, QSizeGrip,QListWidget,QCheckBox,QTableWidget,QTableWidgetItem,QAbstractItemView
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt, QStringListModel, pyqtSignal, QRect, QSize, QPoint,QUrl,QThread
from PyQt5.QtGui import QFont, QCursor,QCloseEvent,QImage,QIcon,QIntValidator
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from images import *

class Mywindow(QMainWindow):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setWindowIcon(QIcon(':HSDSZ.ico'))
        self.birthdaylistsum = []
        self.initUI()
        # self.dbcon = QSqlDatabase.addDatabase("QSQLITE")

        # import configuration
        startupDBpath, startupwidth, startupheight,self.startuplook = readconfig()
        self.resize(startupwidth,startupheight)
        # connect to database
        self.dbpath = startupDBpath
        self.dbcon = QSqlDatabase.addDatabase("QSQLITE")
        self.dbcon.setDatabaseName(self.dbpath)
        self.dbcon.open()
        createtable()
        self.dbcon.commit()
        self.settingwin.page1.le2.setText(startupDBpath)
        self.settingwin.page1.le.setText(startupDBpath)
        self.settingwin.page1.widthle.setText(str(startupwidth))
        self.settingwin.page1.check1.setChecked(self.startuplook)
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
        self.showhidebutton.clicked.connect(self.showhidedetails)

    def initUI(self):
        self.setMinimumHeight(600)
        self.setWindowTitle("idearray")

        # create a previewwindow and setting window
        self.previewwindow = QWebEngineView()
        self.settingwin = SettingWindow()

        # titlebar and maintab
        self.titlebar = TitleBar(self)
        self.maintab = MainTab(self)
        self.maintab.setMinimumWidth(picwidth + 30)
        # self.maintab.setStyleSheet('background-color: rgb(0,0,0,100)')

        # showhide button between tab and comment tag area
        self.showhidebutton = QPushButton(self)
        self.showhidebutton.setFixedSize(10, 50)
        self.showhidebutton.setContentsMargins(0, 0, 0, 0)
        self.showhidebutton.setStyleSheet(pointleft)

        # right tag and comment area
        self.piclabel = PixmapArea(self)
        self.tagarea = TagArea(parent=self)
        self.tagarea.setFixedWidth(picwidth)
        self.commentarea = CommentArea(parent=self)
        self.commentarea.setFixedSize(picwidth,100)
        self.commentarea.setPlaceholderText('Here presents your comment')
        self.commentarea.setStyleSheet('border: none')
        self.linkline = ButtonLink(self)

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
        hlayout.addWidget(self.showhidebutton)
        hlayout.addWidget(self.toolarea)
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setSpacing(0)

        # set the layout of the control
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.titlebar)
        vlayout.addLayout(hlayout)
        # gap between vlayout and the window boder
        vlayout.setContentsMargins(5, 0, 5, 5)
        vlayout.setSpacing(1)
        # display the layout
        frame = QWidget()
        frame.setLayout(vlayout)
        self.setCentralWidget(frame)
        self.setMinimumWidth(picwidth*2 + 80)
        self.showhidebutton.setStyleSheet(pointleft)
        self.maintab.show()
        self.toolarea.hide()
        self.titlebar.mode = 'view'

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

    def showhidedetails(self):
        # depending on the max or not, action is different
        if 'view' in self.titlebar.mode:
            self.titlebar.swithcmodeto(self.titlebar.mode.replace('view','both'))
        elif 'both' in self.titlebar.mode:
            self.titlebar.swithcmodeto(self.titlebar.mode.replace('both','view'))
        else:
            pass

    def triggermodify(self, birthday, source='title', extrude=[-1,'']):
        for i in range(len(self.birthdaylistsum)):
            birthdaylist = self.birthdaylistsum[i]
            if birthday in birthdaylist:
                # get the index of the birthday in the birthdaylist
                index = birthdaylist.index(birthday)
                # get the tabpage
                tabpage = self.maintab.widget(i)
                #update tables
                if not (extrude == [i, 'table']):
                    # refresh table
                    tablepage = tabpage.tablepage
                    # update tables
                    if source == 'title':
                        newtitle = gettitlebybirthday(birthday)
                        tablepage.item(index,1).setText(newtitle)
                    elif source == 'link':
                        newlink = getlinkbybirthday(birthday)
                        tablepage.item(index,2).setText(newlink)
                    elif source == 'comment':
                        newcomment = getcommentbybirthday(birthday)
                        tablepage.item(index,4).setText(newcomment)
                    elif source == 'tag':
                        newtag = gettagbybirthday(birthday)
                        tablepage.item(index,3).setText(newtag)

                # update images
                if source == 'title':
                    # if title is changed, also refresh the image page
                    holder = tabpage.imagepage.widget()
                    # get the specific image widget
                    widget = holder.flayout.itemAt(index).widget()
                    newtitle = gettitlebybirthday(birthday)
                    widget.title.setText(newtitle)


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
        self.dbpath = QFileDialog.getSaveFileName(self,'Create a database','.','(*.db)')[0]
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
            tabpage = TabPage(parent = self, imagepage = imagepage, tablepage = tablepage)
            tabpage.gap.setText(fulltext)
            self.maintab.addTab(tabpage, pagetitle)
            self.maintab.setCurrentIndex(self.maintab.count()-1)
            if self.startuplook:
                imagepage.show()
                tablepage.hide()
            else:
                imagepage.hide()
                tablepage.show()

            # fetch the searched result from DB and put them into image and tablepage
            operation = operation_getbytag3(fulltext)
            operation = "SELECT birthday, title, link, comment, tag, pixmap FROM alldata WHERE (tag LIKE '%youtube%') ORDER BY birthday"
            print(operation)

            query = QSqlQuery()
            query.exec(operation)
            birthdaylist = []
            i = 0
            while query.next():
                # get the birthday, title, url, comment, tag
                birthday = query.value(0)
                birthdaylist.append(birthday)
                title = query.value(1)
                url = query.value(2)
                urltype = geturltype(url)# the first tag is the type
                comment = query.value(3)
                tag = query.value(4)
                pixmap = query.value(5) if query.value(5) != '' else authorpage
                # create a widget to be added
                singleimageitem = ImageWidget(self, holder.flayout,birthday,url,urltype)
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
                singletableitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                tablepage.setItem(i, 0, singletableitem)
                singletableitem = QTableWidgetItem(title)
                tablepage.setItem(i, 1, singletableitem)
                singletableitem = QTableWidgetItem(url)
                singletableitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                tablepage.setItem(i, 2, singletableitem)
                singletableitem = QTableWidgetItem(tag)
                singletableitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                tablepage.setItem(i, 3, singletableitem)
                singletableitem = QTableWidgetItem(comment)
                tablepage.setItem(i, 4, singletableitem)

                QApplication.processEvents()
                i += 1
            tablepage.loadfinished = True
            self.birthdaylistsum.append(birthdaylist)

    # this slot function response to a custom dropped event. That event emit dragtext
    def handledropped(self, dragtext):
        # show mainwindow right detail area
        currentmode = self.titlebar.mode
        if currentmode == 'update':
            pass
        else:
            self.titlebar.swithcmodeto(currentmode.replace('view', 'both'))

        # get the birthday, url, urltype, these shared content. set url
        birthday = now()
        urltype = geturltype(dragtext)
        url = refineurl(dragtext, urltype)
        self.linkline.linkline.setText(url)
        self.piclabel.birthday = birthday
        self.tagarea.birthday = birthday
        self.commentarea.birthday = birthday


        # set title
        if urltype == 'pdf':
            document = fitz.open(url)
            urltitle = geturltitle(url,urltype,document)
        else:
            urltitle = geturltitle(url,urltype)
        urltitle = geturltitle(url, urltype)
        self.piclabel.title.setText(urltitle)

        # set tags and update alltag in the searchbar completer
        tagstr, taglist = titletotags(urltype, urltitle)
        self.tagarea.showtagsbylist(taglist)
        for item in taglist:
            if item not in self.titlebar.searchbar.completer.alltags:
                self.titlebar.searchbar.completer.alltags += [item]

        # set comment
        self.commentarea.setText('')
        # process them and add them into database
        QApplication.processEvents()
        adddatawithoutpix(birthday, urltitle, url, '', tagstr)
        self.dbcon.commit()

        # set pixmap to qlabel and save this new pixmap to database
        if urltype == 'web':
            self.piclabel.setPixmap(QPixmap(':loading.png'))
            self.tempengine = Webengine(self.dbcon,self.piclabel)
            self.tempengine.setZoomFactor(0.3)
            self.tempengine.show()
            self.tempengine.birthday = birthday
            self.tempengine.load(QUrl(url))
        elif urltype == 'pdf':
            # screenshot the first page
            page1 = document[0] # first page
            pix = page1.getPixmap(alpha = False)
            # convert into qpix and resize
            qimage=QImage(pix.samples,pix.width, pix.height,pix.stride,QImage.Format_RGB888)
            rawpixmap = QPixmap.fromImage(qimage)
            qpixmap = resizepixmap(rawpixmap,picwidth,picheight, area = 'top')
            bytedata = pixmap2byte(qpixmap)
            # save into db
            self.piclabel.setPixmap(qpixmap)
            updatebybirthday(birthday=birthday, title=urltitle, pixmap=bytedata)
            self.dbcon.commit()
        elif urltype == 'image':
            pixmap = QPixmap(url)
            pixmap = resizepixmap(pixmap,picwidth,picheight)
            self.piclabel.setPixmap(pixmap)
            # insert data into the db base
            bytedata = pixmap2byte(pixmap)
            updatebybirthday(birthday=birthday, pixmap=bytedata)
            self.dbcon.commit()
        elif urltype == 'youtube' or urltype == 'bilibili':
            pixmap = youtubilibilithumb(url,urltype, picwidth, picheight)
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

        item = self.taglist.findItems(search_text,Qt.MatchExactly)[0]
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

###############Below are widgets for tab and its pages###############
class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)
        self.oldfocusindex = 0
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

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

    def resizeEvent(self, QResizeEvent):
        scrollwidth = self.size().width()
        remainwidth = scrollwidth % picwidth
        counts = scrollwidth // picwidth
        if remainwidth < 20:
            spacing = int((remainwidth + picwidth) / counts)
        else:
            spacing = int(remainwidth / counts)

        self.flayout.setSpacing(spacing)

        # if self.size().width() > 1500:
        #     self.flayout.setSpacing(35)
        # else:
        #     self.flayout.setSpacing(10)

class ImageWidget(QLabel):
    def __init__(self, parent=None, glayout=None, birthday=0, url ='', urltype='unknown'):
        super(ImageWidget, self).__init__(parent)
        # some variable
        self.url = url
        self.urltype = urltype
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
        self.previewbutton = PreviewButton(self, self.urltype)
        self.previewbutton.setFixedSize(40, 30)
        self.previewbutton.move(int(picwidth / 2)-20, int(picheight / 2)-15)
        self.previewbutton.hide()
        self.previewbutton.setToolTip('Preview')

        # some toolbar buttons
        self.urlbutton = QPushButton(self)
        self.urlbutton.setStyleSheet(openstyle)
        self.urlbutton.setFixedSize(25, 25)
        self.urlbutton.setToolTip('open')

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
        vbx.addWidget(self.urlbutton)
        vbx.addWidget(self.likebutton)
        vbx.addWidget(self.laterbutton)
        vbx.addWidget(self.deletebutton)
        vbx.addWidget(self.downloadbutton)
        self.bar = QWidget(self)
        self.bar.setStyleSheet('background-color: None')
        self.bar.setLayout(vbx)
        self.bar.hide()

        # signal
        # self.title.textChanged.connect(self.titleeditted)
        self.urlbutton.clicked.connect(self.openurl)
        self.likebutton.clicked.connect(self.changelike)
        self.laterbutton.clicked.connect(self.changelater)
        self.previewbutton.clicked.connect(self.showpreview)
        self.deletebutton.clicked.connect(self.deleterecover)
        self.downloadbutton.clicked.connect(self.download)

    # slot function
    def openurl(self):
        urltype = geturltype(self.url)
        if urltype == 'web' or urltype == 'youtube' or urltype == 'bilibili':
            os.system("start {}".format(self.url))
        else:
            os.startfile(self.url)

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
        self.folderpath = QFileDialog.getExistingDirectory(None, 'Select a folder:', '/')

        if self.folderpath != '':
            self.work = BkgrndThread(self, url=self.url, path=self.folderpath)
            self.work.start()
            # downloadvideo(self.url,self.folderpath)

    def showpreview(self):
        self.previewwindow = WebPreview2()
        self.previewwindow.preview(self.url)
        self.previewwindow.show()
        # a popup window to show the preview of the url

    def titleeditted(self):
        focused_widget = QApplication.focusWidget()
        newtitle = self.title.toPlainText()
        if isinstance(focused_widget, QTextEdit) and self.title.iseditmode and newtitle != '':
            updatebybirthday(self.birthday, title=self.title.toPlainText())
            self.parent.piclabel.title.setText(self.title.toPlainText())

            # maintab index
            excludeindex = self.parent.maintab.currentIndex()
            self.parent.triggermodify(self.birthday, 'title', extrude = [excludeindex, 'image'])

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
            self.parent.linkline.linkline.setText(self.url)

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

        if self.urltype == 'youtube' or self.urltype == 'bilibili':
            self.downloadbutton.show()
        else:
            self.downloadbutton.hide()

        title = gettitlebybirthday(self.birthday)
        if title != self.title.toPlainText():
            self.title.setText(title)

        if istypeexist(self.urltype):
            self.previewbutton.show()

    def leaveEvent(self, *args, **kwargs):
        self.bar.hide()
        self.previewbutton.hide()

class PreviewButton(QPushButton):
    def __init__(self,parent = None, urltype = 'unknown'):
        super(PreviewButton, self).__init__(parent)
        self.parent = parent
        try:
            self.setStyleSheet(previewicon(urltype))
        except:
            pass

    def enterEvent(self, *args, **kwargs):
        self.setCursor(QCursor(Qt.PointingHandCursor))
    def leaveEvent(self, *args, **kwargs):
        self.setCursor(QCursor(Qt.ArrowCursor))

class WebPreview(QWidget):
    def __init__(self, parent = None):
        super(WebPreview, self).__init__(parent)
        self.webengine = QWebEngineView()
        self.webengine.page().settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.webengine.page().settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.webengine.resize(1200,900)

        button1 = QPushButton()
        button1.setFixedSize(20,20)
        gap = QLabel()
        hlyout = QHBoxLayout()
        hlyout.addWidget(button1)
        hlyout.addWidget(gap)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.webengine)
        vlayout.addLayout(hlyout)
        self.setLayout(vlayout)

        button1.clicked.connect(self.zoom)

    def zoom(self):
        pass

    def preview(self,url):
        self.webengine.load(QUrl(url))

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.webengine.close()
        self.close()

class WebPreview2(QWebEngineView):
    def __init__(self, parent = None):
        super(WebPreview2, self).__init__(parent)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.resize(1000,900)

    def preview(self,url):
        urltype = geturltype(url)
        if urltype == 'pdf':
            self.load(QUrl.fromUserInput('{}?file={}'.format(PDFJS, url)))
        else:
            self.load(QUrl(url))

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
        self.setHorizontalHeaderLabels(['birthday','title', 'url', 'tag', 'comment'])
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.verticalHeader().setFixedWidth(20)
        self.setColumnWidth(0, 105)
        self.setColumnWidth(1, 350)
        self.setColumnWidth(2, 208)
        self.setColumnWidth(3, 400)
        self.setColumnWidth(4, 800)

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
        self.cellChanged.connect(self.changemade)
        self.customContextMenuRequested.connect(self.generateMenu)

    def updaterightarea(self,currentRow,currentColumn,previousRow, previousColumn):
        if currentRow != previousRow:
            # if we swap row, then we trigger right area
            birthday = int(self.item(currentRow,0).text())
            if birthday != self.parent.tagarea.birthday:
                # show all the tags of this widget
                self.parent.tagarea.showtags(birthday)
                # show comment into the tagarea
                self.parent.commentarea.showcomment(birthday)
                # show the pic annd title in the piclabel
                self.parent.piclabel.showpixandtitle(birthday)
                # set the link
                url = getlinkbybirthday(birthday)
                self.parent.linkline.linkline.setText(url)

    def changemade(self,row,column):
        if self.loadfinished and self.iseditmode and column != 3:
            # maintab index
            excludeindex = self.parent.maintab.currentIndex()
            birthday = int(self.item(row,0).text())
            newtext = self.item(row,column).text()
            if column == 1:
                #update title
                updatebybirthday(birthday,title= newtext)
                self.parent.piclabel.title.setText(newtext)
                self.parent.triggermodify(birthday, 'title', extrude = [excludeindex, 'table'])
            elif column == 2:
                # update url
                updatebybirthday(birthday,link= newtext)
                self.parent.linkline.linkline.setText(newtext)
                self.parent.triggermodify(birthday, 'link', extrude = [excludeindex, 'table'])
            elif column == 4:
                # update comment
                updatebybirthday(birthday,comment= newtext)
                self.parent.commentarea.showcomment(birthday)
                self.parent.triggermodify(birthday, 'comment', extrude = [excludeindex, 'table'])
            else:
                pass

    def generateMenu(self, pos):
        row = self.currentRow()
        if row != -1:
            birthday = int(self.item(row,0).text())
            url = self.item(row,2).text()
            urltype = geturltype(url)
            self.action5.setEnabled(istypeexist(urltype))
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
                if urltype == 'web' or urltype == 'youtube' or urltype == 'bilibili':
                    os.system("start {}".format(url))
                else:
                    os.startfile(url)

            elif self.action == self.action5:
                self.previewwindow = WebPreview2()
                self.previewwindow.preview(url)
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

################# Below are widgets for the right tagarea and commentarea ############

class TextEdit(QTextEdit):
    def __init__(self, parent = None):
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
        self.setFixedSize(picwidth, picheight + 60)

        self.title.textChanged.connect(self.titleeditted)

    def showpixandtitle(self,birthday):
        self.birthday = birthday
        pix = getpixmapbybirthday(birthday)
        self.setPixmap(byte2pixmap(pix))
        title = gettitlebybirthday(birthday)
        self.title.setText(title)

    def titleeditted(self):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QTextEdit) and self.title.iseditmode:
            updatebybirthday(self.birthday,title= self.title.toPlainText())
            self.mainwindow.triggermodify(self.birthday, 'title')

    def updatepixmap(self,bytedata):
        updatebybirthday(birthday=self.birthday, pixmap=bytedata)


class CommentArea(QTextEdit):
    def __init__(self, parent):
        super(CommentArea, self).__init__(parent)
        self.mainwindow = parent
        self.textChanged.connect(self.textmodded)
        self.dbcon = None

    def showcomment(self, birthday, comment = '3.141592653'):
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
        self.newinput.setFixedWidth(picwidth-20)
        self.newinput.returnPressed.connect(self.addtag)
        self.gridlayout.addWidget(self.newinput, 0, 0, 1, 3)

    def showtags(self, birthday):
        # clear the layout, keep the newinput lineedit
        for i in range(self.gridlayout.count()-1):
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
            tagbutton.setFixedWidth(int(picwidth/3-6.66))
            if len(label) > 10:
                # if the str is too long, show a tooltip
                tagbutton.setToolTip(taglist[i])
            self.gridlayout.addWidget(tagbutton, (i + 3) // 3, (i + 3) % 3, Qt.AlignCenter)

    def showtagsbylist(self, taglist):
        # clear the layout, keep the newinput lineedit
        for i in range(self.gridlayout.count()-1):
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
            tagbutton.setFixedWidth(int(picwidth/3-6.66))
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
            newinputlist += expandlist
            if tag not in taglist:
                tagstr += ' {}'.format(tag)
        updatebybirthday(self.birthday, tag=tagstr)
        self.showtags(self.birthday)
        self.dbcon.commit()

        self.mainwindow.triggermodify(self.birthday, 'tag')
        # update alltag in the completer
        self.mainwindow.titlebar.searchbar.completer.alltags = refreshalltags(self.mainwindow.titlebar.searchbar.completer.alltags, tagstr.split())
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
        self.urlbutton = QPushButton(self)
        # remove background and make the word blue and underline
        self.urlbutton.setStyleSheet('''
        QPushButton{background-color: rgba(0, 0, 0, 0); color: blue; text-decoration: none; text-align: left; }
        QPushButton:hover{text-decoration: underline;}
        QPushButton:pressed{text-decoration: none;}''')

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.closebutton)
        hlayout.addWidget(self.urlbutton)
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hlayout)

        # signals
        self.urlbutton.clicked.connect(lambda: self.parent.newtab(self.urlbutton.text()))
        self.closebutton.clicked.connect(lambda: self.parent.removetag(self.urlbutton.text()))

    def setText(self, text):
        self.urlbutton.setText(text)
        # hide close button in certain situation
        if text == '#deleted' or text == '#like' or text == '#later':
            self.closebutton.hide()

class ButtonLink(QWidget):
    def __init__(self, parent):
        super(ButtonLink, self).__init__(parent)
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

    def openlink(self):
        if self.linkline.text() != '':
            os.system("start {}".format(self.linkline.text()))

################Below are widgets for titlebar################

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
        self.setPlaceholderText(" Search tags or drag url/file here")
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
        # hasUrls means drag in a file or url
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
        self.mode = 'view'
        self.previousmode = 'view'
        self.m_drag = False

        # create a searchbar
        self.searchbar = CustomLineEdit(parent=self)
        self.searchbar.setStyleSheet(searchbarstyle)
        self.searchbar.setMaximumWidth(600)

        # custom menu and button
        # menulist = ["Set hierarchy", {"Empty": ['Empty', "Empty"]}]
        menulist = ["Tag hierarchy setting"]
        filemenu = QMenu(self)
        create_menu(menulist, filemenu)


        # gap is  for icon and double click use
        self.icon = CustomGap(parent=self)
        self.icon.setFixedWidth(50)
        self.icon.setStyleSheet(hsdsz)

        # design button to hold the menu
        filebutton = QPushButton()
        filebutton.setFixedWidth(60)
        filebutton.setMenu(filemenu)
        filebutton.setText('Setting')
        filebutton.setStyleSheet("QPushButton { border: none}")

        self.gap = CustomGap(parent=self)

        # create a some quick tool button
        self.pinbutton = NoMoveButton()
        self.pinbutton.setFixedSize(27, 27)
        self.pinned = False
        self.pinbutton.setStyleSheet(unpinned)
        self.miniwinbutton = NoMoveButton()
        self.miniwinbutton.setFixedSize(27,27)
        self.miniwinbutton.setStyleSheet(nonmini)
        minbutton = QPushButton()
        minbutton.setFixedSize(27, 27)
        minbutton.setStyleSheet(minimize)
        self.maxbutton = NoMoveButton()
        self.maxbutton.setFixedSize(27, 27)
        self.maxbutton.setStyleSheet(originmode)
        closebutton = NoMoveButton()
        closebutton.setFixedSize(27, 27)
        closebutton.setStyleSheet(closeicon)
        # arrange these in a horizontal way
        hbx = QHBoxLayout()
        hbx.addWidget(self.icon)
        # hbx.addWidget(filebutton)
        hbx.addWidget(self.gap)
        hbx.addWidget(self.searchbar)
        hbx.addWidget(self.pinbutton)
        hbx.addWidget(self.miniwinbutton)
        hbx.addWidget(minbutton)
        hbx.addWidget(self.maxbutton)
        hbx.addWidget(closebutton)
        hbx.setContentsMargins(0, 0, 0, 0)
        hbx.setSpacing(0)
        self.setLayout(hbx)

        # signals
        self.pinbutton.clicked.connect(self.pin)
        self.miniwinbutton.clicked.connect(self.miniwin)
        minbutton.clicked.connect(self.min)
        self.maxbutton.clicked.connect(self.max)
        closebutton.clicked.connect(self.shutdown)
        # signals of menu
        filemenu.triggered.connect(self.actionClicked)

    def swithcmodeto(self,modeto = 'view'):
        self.previousmode = self.mode
        if modeto == 'maxview':
            self.mode = 'maxview'
            self.sizebeforemax = [self.mainwindow.size().width(), self.mainwindow.size().height()]
            self.mainwindow.showhidebutton.show()
            self.maxbutton.show()
            self.mainwindow.setMinimumWidth(picwidth + 80)
            self.mainwindow.showhidebutton.setStyleSheet(pointleft)
            self.mainwindow.maintab.show()
            self.mainwindow.toolarea.hide()
            self.mainwindow.showMaximized()

            # set icons style
            self.maxbutton.setStyleSheet(maxmode)
            self.miniwinbutton.setStyleSheet(nonmini)

        elif modeto == 'maxboth':
            self.sizebeforemax = [self.mainwindow.size().width(), self.mainwindow.size().height()]
            self.mode = 'maxboth'
            self.mainwindow.showhidebutton.show()
            self.maxbutton.show()
            self.mainwindow.setMinimumWidth(picwidth * 2 + 80)
            self.mainwindow.showhidebutton.setStyleSheet(pointright)
            self.mainwindow.maintab.show()
            self.mainwindow.toolarea.show()
            self.mainwindow.showMaximized()

            # set icons style
            self.maxbutton.setStyleSheet(maxmode)
            self.miniwinbutton.setStyleSheet(nonmini)

        elif modeto == 'view':
            self.mode = 'view'
            self.mainwindow.showhidebutton.show()
            self.maxbutton.show()
            self.mainwindow.setMinimumWidth(picwidth * 2 + 80)
            self.mainwindow.showhidebutton.setStyleSheet(pointleft)
            self.mainwindow.maintab.show()
            self.mainwindow.toolarea.hide()
            self.mainwindow.showNormal()

            # set icons style
            self.maxbutton.setStyleSheet(originmode)
            self.miniwinbutton.setStyleSheet(nonmini)

        elif modeto == 'both':
            self.mode = 'both'
            self.mainwindow.showhidebutton.show()
            self.maxbutton.show()
            self.mainwindow.setMinimumWidth(picwidth * 2 + 80)
            self.mainwindow.showhidebutton.setStyleSheet(pointright)
            self.mainwindow.maintab.show()
            self.mainwindow.toolarea.show()
            self.mainwindow.showNormal()

            # set icon style
            self.maxbutton.setStyleSheet(originmode)
            self.miniwinbutton.setStyleSheet(nonmini)

        elif modeto == 'update':
            self.sizebeforemini = [self.mainwindow.size().width(),self.mainwindow.size().height()]
            self.mode = 'update'
            self.mainwindow.showhidebutton.hide()
            self.maxbutton.hide()
            self.mainwindow.setMinimumWidth(picwidth + 10)
            self.mainwindow.toolarea.show()
            self.mainwindow.maintab.hide()
            self.mainwindow.showNormal()
            self.mainwindow.resize(picwidth + 10, 600)

            # set icon style
            self.miniwinbutton.setStyleSheet(mini)

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
        if self.mode == 'update':
            # if the current mode is update mode. then return back to its previous
            self.swithcmodeto(self.previousmode)
            self.mainwindow.resize(self.sizebeforemini[0], self.sizebeforemini[1])

        else:
            # as long as self.mode is not updatemode. change them to updatemode
            self.swithcmodeto('update')

    def max(self):
        # if this icon is max, then make the mainwindow original mode
        if self.mode == 'view' or self.mode == 'both':
            self.swithcmodeto('max{}'.format(self.mode))

        elif self.mode == 'maxview' or self.mode == 'maxboth':
            self.swithcmodeto(self.mode.split('max')[1])

            if self.sizebeforemax[0] == (picwidth + 10):
                self.mainwindow.resize(1300, 800)
            else:
                self.mainwindow.resize(self.sizebeforemax[0],self.sizebeforemax[1])

        else:
            pass

    def min(self):
        self.mainwindow.showMinimized()

    def actionClicked(self, action):
        pass
        print(action.text())

    # overwrite functions
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.start_x = QMouseEvent.x()
            self.start_y = QMouseEvent.y()
            self.m_drag = True

    def mouseMoveEvent(self, QMouseEvent):
        if 'max' in self.mode and self.m_drag == True:
            # after moving, if the current icon is max style, change it into originnal
            self.mainwindow.showNormal()
            self.maxbutton.setStyleSheet(originmode)
            self.mode = self.mode.split('max')[1]
            if self.sizebeforemax[0] == (picwidth + 10):
                self.mainwindow.resize(1300, 800)
            else:
                self.mainwindow.resize(self.sizebeforemax[0],self.sizebeforemax[1])


        # change cursor to hand
        # if QMouseEvent.button() == Qt.LeftButton:
        if self.m_drag:
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            dis_x = QMouseEvent.x() - self.start_x
            dis_y = QMouseEvent.y() - self.start_y
            self.mainwindow.move(self.mainwindow.x()+dis_x, self.mainwindow.y()+dis_y)

    def mouseReleaseEvent(self, QMouseEvent):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.m_drag = False

class NoMoveButton(QPushButton):
    def __init__(self, parent = None):
        super(NoMoveButton, self).__init__(parent)

    def mouseMoveEvent(self, QMouseEvent):
        pass

###################BG THread ####################
class BkgrndThread(QThread):
    def __init__(self, parent=None, url='', path=''):
        super(BkgrndThread, self).__init__(parent)
        self.url = url
        self.folderpath = path

    def run(self):
        downloadvideo(self.url,self.folderpath)
        self.quit()

class BkgrnTitle(QThread):
    def __init__(self, parent = None, url='',urltype='youtube',birthday=0):
        super(BkgrnTitle, self).__init__(parent)
        self.parent = parent
        self.url = url
        self.urltype = urltype
        self.birthday = birthday

    def run(self):
        pixmap = youtubilibilithumb(self.url,self.urltype, picwidth, picheight)
        self.parent.piclabel.setPixmap(pixmap)
        # insert data into the db base
        bytedata = pixmap2byte(pixmap)


if __name__ == "__main__":
    picwidth, picheight = [320, 180]
    PDFJS = 'file:///./pdfjs/web/viewer.html'
    buildwindow(Mywindow)
