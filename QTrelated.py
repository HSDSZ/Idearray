import sys
from PyQt5.QtWidgets import QApplication,QMenu
from PyQt5.QtCore import QBuffer,QByteArray,QIODevice
from PyQt5.QtGui import QPixmap
# this function generate the window of a given QMainwindow class
def buildwindow(WindowClass):
    # system operation
    app = QApplication(sys.argv)
    # instance your window
    window = WindowClass()
    # show your window
    window.show()
    # run your window in system
    sys.exit(app.exec_())

def create_menu(d, menu):
    if isinstance(d, list):
        for e in d:
            create_menu(e, menu)
    elif isinstance(d, dict):
        for k, v in d.items():
            sub_menu = QMenu(k, menu)
            menu.addMenu(sub_menu)
            create_menu(v, sub_menu)
    else:
        action = menu.addAction(d)
        action.setIconVisibleInMenu(False)


def pixmap2byte(qpixmap):
    # create byt array
    ba = QByteArray()
    buff = QBuffer(ba)
    buff.open(QIODevice.WriteOnly)
    ok = qpixmap.save(buff, 'png')
    assert ok
    pixmap_bytes = ba.data()
    return  pixmap_bytes

def byte2pixmap(byte):
    ba = QByteArray(byte)
    pixmap = QPixmap()
    ok = pixmap.loadFromData(ba, "png")
    assert ok
    return pixmap

def file2byte(path):
    with open(path, "rb") as image:
        f = image.read()
        return f

