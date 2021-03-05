### This file is used to simplify the use of PyQt5 or Pyside ###
import os
from PyQt5.QtGui import QPixmap
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from SQLiterelated import expandstr
import json
import requests
import urllib3

def bilithumburl(bvid):
    # url = 'https://api.bilibili.com/x/web-interface/view?aid='+avid
    url = 'https://api.bilibili.com/x/web-interface/view?bvid={}'.format(bvid)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
                'Referer': 'https://www.bilibili.com'}

    urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    content = json.loads(response.text)

    statue_code = content.get('code')
    if statue_code == 0:
        return content.get('data').get('pic')
    else:
        return ''

# this function return a Qpixmap of video web which has thumbnail
def youtubilibilithumb(url,urltype, width, height):
    if urltype == 'youtube':
        # get youtube thumbnail
        id = url.split('=')[1].split('&')[0]
        thumbnail_url = "http://img.youtube.com/vi/{}/0.jpg".format(id)
        loadedpix = urltopixmap(thumbnail_url)
        return resizepixmap(loadedpix, width, height)

    elif urltype == 'bilibili':
        # get bilibili thumbnail
        bvid = url.split('video/')[1].split('?')[0]
        # v = video.get_video_info(bvid=bvid)
        # get the image
        # thumbnail_url = v.get('pic')
        thumbnail_url = bilithumburl(bvid)
        loadedpix = urltopixmap(thumbnail_url)
        return resizepixmap(loadedpix, width, height)

    else:
        pixmap = QPixmap('./pics/unknownthumb.png')
        return pixmap.scaled(width,height)

def urltopixmap(url):
    data = urlopen(url).read()
    # load this data into a QPixmap
    qpixmap = QPixmap()
    qpixmap.loadFromData(data)
    return qpixmap

def resizepixmap(qpixmap,width, height, area = 'middle'):

    rawwdith = qpixmap.size().width()
    rawheight = qpixmap.size().height()

    if area == 'top':
        # cut the unwanted bottom
        qpixmap = qpixmap.copy(0,0,rawwdith, rawwdith/16*9)
    elif area == 'middle':
        # cut the unwanted top and bottom black strip
        qpixmap = qpixmap.copy(0, int(0.5 * (rawheight - rawwdith / 16 * 9)), rawwdith, int(rawwdith / 16 * 9))
    else:
        # directly scale
        pass
    # scale the qpixamp to a wanted size
    qpixmap = qpixmap.scaled(width, height)
    return qpixmap

def refineurl(url, urltype):
    if (urltype == 'web') or (urltype == 'youtube') or (urltype == 'bilibili'):
        if 'http' not in url:
            newurl = 'http://www.' + url
            return newurl
        else:
            return url
    elif urltype == 'unknown':
        newurl = url
        return newurl
    else:
        newurl = url.split('file:///')[1]
        return newurl

def geturltitle(url, urltype, document = None):
    if urltype == 'youtube' or urltype == 'web' or urltype == 'bilibili':
        try:
            source_code = requests.get(url)
            soup = BeautifulSoup(source_code.content,'html.parser')
            rawtitle = soup.title.text
        except:
            rawtitle = 'unknown'
        # remove some usless str. bilibli and youtube title has some useless suffix
        title = rawtitle.split('_哔哩哔哩 (')[0].split(' - YouTube')[0]
        return title

    elif urltype == 'pdf':
        try:
            toc = document.get_toc()
            rawtitle = document.get_toc()[0][1]
            newtitle = rawtitle.replace('', ' ')
            if newtitle == 'Title':
                return os.path.basename(url).split('.')[0]
            else:
                return newtitle
        except:
            newtitle = os.path.basename(url).split('.')[0]
        return newtitle

    elif urltype == 'unknown':
        return 'unknown'

    else:
        title = os.path.basename(url).split('.')[0]
        return title

def titletotags(urltype, rawtitle):
    # tidy up this title
    tidytitle = tidyup(rawtitle)
    # put the urltype at the begining of the tags
    tagstr = '{} {}'.format(urltype, tidytitle)
    # expand the tags
    tagstr = expandstr(tagstr)
    # remove repeated str
    words = tagstr.split()
    tagstr = " ".join(sorted(set(words), key=words.index))
    # generate the final taglist
    taglist = tagstr.split()
    return tagstr, taglist

def geturltype(url):
    if 'youtube.com/watch' in url:
        return 'youtube'
    elif 'bilibili.com/video' in url:
        return 'bilibili'
    elif 'http' in url:
        return 'web'
    elif ':' in url:
        extension = url.split('.')[-1]
        if extension == 'jpg' or extension == 'png' or extension == 'jpeg':
            return 'image'
        else:
            return extension
    else:
        return 'unknown'

def istypeexist(urltype):
    if urltype == 'youtube':
        return True
    elif urltype == 'bilibili':
        return True
    elif urltype == 'web':
        return True
    elif urltype == 'pdf':
        return True
    elif urltype == 'image':
        return True
    elif urltype == 'txt':
        return True
    else:
        return False

def tidyup(title=''):
    # lowercase first
    title = title.lower()
    # remove the following str
    title = title.replace('[', '')
    title = title.replace('【', '')
    title = title.replace('】', '')
    title = title.replace(']', '')
    title = title.replace('{', '')
    title = title.replace('}', '')
    title = title.replace('(', '')
    title = title.replace('（', '')
    title = title.replace(')', '')
    title = title.replace('）', '')
    title = title.replace('!', '')
    title = title.replace('+', '')
    title = title.replace(':', '')


    # replace the following str with space
    title = title.replace('|', ' ')
    title = title.replace('「', ' ')
    title = title.replace('」', ' ')
    title = title.replace('/', ' ')
    title = title.replace(' - ', ' ')
    title = title.replace('-', ' ')
    title = title.replace('_', ' ')
    title = title.replace('&', ' ')
    title = title.replace(' a ', ' ')
    title = title.replace(' with ', ' ')
    title = title.replace(' to ', ' ')
    title = title.replace(' in ', ' ')
    title = title.replace(' on ', ' ')
    title = title.replace(' at ', ' ')
    title = title.replace(' an ', ' ')
    title = title.replace(' and ', ' ')
    title = title.replace(' the ', ' ')
    title = title.replace('    ', ' ')
    title = title.replace('   ', ' ')
    title = title.replace('  ', ' ')
    title = title.replace(' ', ' ')

    # if the final str of the title is an empty space, remove it
    return title[:-1] if title[-1] == ' ' else title


def now():
    now = str(datetime.now())
    birthday = int(now.split(' ')[0].replace('-','')+now.split(' ')[1].split('.')[0].replace(':',''))
    return birthday

if __name__ == '__main__':
    import fitz
    url = './T.pdf'
    document = fitz.open(url)
    urltitle = geturltitle(url,'pdf',document)
    print(urltitle)
