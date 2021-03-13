import os
from PyQt5.QtGui import QPixmap
from datetime import datetime
from SQLiterelated import expandstr
import json
import requests
from constants import *
from you_get import common
def bili_thumb_link(bvid):
    # link = 'https://api.bilibili.com/x/web-interface/view?aid='+avid
    link = 'https://api.bilibili.com/x/web-interface/view?bvid={}'.format(bvid)

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    #             'Referer': 'https://www.bilibili.com'}

    # linklib3.disable_warnings()
    response = requests.get(link, headers=headers, verify=False)
    content = json.loads(response.text)

    statue_code = content.get('code')
    if statue_code == 0:
        return content.get('data').get('pic')
    else:
        return ''

def qqv_thumb_link_old(link):
    if 'page' in link:
        vid = link.split('page/')[1].split('.html')[0]
        thumblink = 'http://puui.qpic.cn/qqvideo_ori/0/{}_360_204/0'.format(vid)
        return thumblink
    elif 'cover' in link:
        # individual video
        link_tail = link.split('cover/')[1]
        if '/' in link_tail:
            vid = link_tail.split('/')[1].split('.html')[0]
        else:
            fulltext = requests.get(link,headers=headers).text
            vid = fulltext.split('var LIST_INFO = {"vid":["')[1].split('"')[0]
        thumblink = 'http://puui.qpic.cn/qqvideo_ori/0/{}_360_204/0'.format(vid)
        return thumblink
    else:
        return ''

def qqv_thumb_link(link):
    if 'page' in link:
        vid = link.split('page/')[1].split('.html')[0]
        thumblink = 'https://vpic.video.qq.com/15746141/{}.png'.format(vid)
        return thumblink
    elif 'cover' in link:
        # individual video
        link_tail = link.split('cover/')[1]
        if '/' in link_tail:
            vid = link_tail.split('/')[1].split('.html')[0]
        else:
            fulltext = requests.get(link,headers=headers).text
            vid = fulltext.split('var LIST_INFO = {"vid":["')[1].split('"')[0]
        thumblink = 'https://vpic.video.qq.com/15746141/{}.png'.format(vid)
        return thumblink
    else:
        return ''

def iqiyi_thumb_link(link):
    # first the the vid
    fulltext = requests.get(link,headers=headers).text
    tvid = fulltext.split('tvid=')[1].split('&aid')[0]

    # get image from api
    api_link = 'http://pcw-api.iqiyi.com/video/video/playervideoinfo?tvid={}'.format(tvid)
    fulltext = requests.get(api_link,headers=headers).text
    content = json.loads(fulltext)
    return content.get('data').get('vpic')


# this function return a Qpixmap of video web which has thumbnail
def videothumb(link,linktype, width, height):
    if linktype == 'youtube':
        # get youtube thumbnail
        id = link.split('=')[1].split('&')[0]
        thumbnail_link = "http://img.youtube.com/vi/{}/0.jpg".format(id)
        rawpixmap = linktopixmap(thumbnail_link)
        return resizepixmap(rawpixmap, width, height)

    elif linktype == 'bilibili':
        # get bilibili thumbnail
        bvid = link.split('video/')[1].split('?')[0]
        thumbnail_link = bili_thumb_link(bvid)
        rawpixmap = linktopixmap(thumbnail_link)
        return resizepixmap(rawpixmap, width, height)

    elif linktype == 'iqiyi':
        thumbnail_link = iqiyi_thumb_link(link)
        rawpixmap = linktopixmap(thumbnail_link)
        return resizepixmap(rawpixmap, width, height)

    elif linktype == 'tencent':
        thumbnail_link = qqv_thumb_link(link)
        rawpixmap = linktopixmap(thumbnail_link)
        return resizepixmap(rawpixmap, width, height)

    else:
        pixmap = QPixmap('./pics/unknownthumb.png')
        return pixmap.scaled(width,height)


def linktopixmap(link):
    data = requests.get(link,headers=headers).content
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

def refinelink(link, linktype):
    if (linktype == 'web') or (linktype == 'youtube') or (linktype == 'bilibili') or (linktype == 'tencent') or (linktype == 'iqiyi'):
        if 'http' not in link:
            newlink = 'http://www.' + link
            return newlink
        else:
            return link
    elif linktype == 'unknown':
        newlink = link
        return newlink
    else:
        newlink = link.split('file:///')[1]
        return newlink

def getlinktitle(link, linktype, document = None):
    if linktype == 'youtube' or linktype == 'web' or linktype == 'tencent' or linktype == 'iqiyi':
        try:
            r = requests.get(link,headers=headers)
            r.encoding = 'utf-8'
            fulltext = r.text
            rawtitle = fulltext.split('<title>')[1].split('</title>')[0]
        except:
            rawtitle = 'unknown'
        # remove some usless str. youtube title has some useless suffix
        title = rawtitle.split(' - YouTube')[0]
        title = title.replace('â€“',' ')
        return title
    
    elif linktype == 'bilibili':
        try:
            fulltext = requests.get(link,headers=headers).text
            title = fulltext.split('<title data-vue-meta="true">')[1].split('_哔哩哔哩 (')[0]
        except:
            title = 'unknown'
        return title

    elif linktype == 'pdf':
        try:
            toc = document.get_toc()
            rawtitle = document.get_toc()[0][1]
            newtitle = rawtitle.replace('', ' ')
            if newtitle == 'Title':
                return os.path.basename(link).split('.')[0]
            else:
                return newtitle
        except:
            newtitle = os.path.basename(link).split('.')[0]
        return newtitle

    elif linktype == 'unknown':
        return 'unknown'

    else:
        title = os.path.basename(link).split('.')[0]
        return title

def titletotags(linktype, rawtitle):
    # tidy up this title
    tidytitle = tidyup(rawtitle)
    # put the linktype at the begining of the tags
    tagstr = '{} {}'.format(linktype, tidytitle)
    # expand the tags
    tagstr = expandstr(tagstr)
    # remove repeated str
    words = tagstr.split()
    tagstr = " ".join(sorted(set(words), key=words.index))
    # generate the final taglist
    taglist = tagstr.split()
    return tagstr, taglist

def getlinktype(link):
    if 'youtube.com/watch' in link:
        return 'youtube'
    elif 'bilibili.com/video' in link:
        return 'bilibili'
    elif 'v.qq.com' in link:
        return 'tencent'
    elif 'iqiyi.com/v' in link:
        return 'iqiyi'
    elif 'http' in link:
        return 'web'
    elif ':' in link:
        extension = link.split('.')[-1]
        if extension == 'jpg' or extension == 'png' or extension == 'jpeg':
            return 'image'
        else:
            return extension
    else:
        return 'unknown'

def istypeexist(linktype):
    if linktype == 'youtube':
        return True
    elif linktype == 'bilibili':
        return True
    elif linktype == 'web':
        return True
    elif linktype == 'pdf':
        return True
    elif linktype == 'image':
        return True
    elif linktype == 'txt':
        return True
    elif linktype == 'tencent':
        return True    
    elif linktype == 'iqiyi':
        return True
    else:
        return False

def istypeolvid(linktype):
    if linktype == 'youtube' or linktype == 'bilibili' or linktype == 'tencent' or linktype == 'iqiyi':
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

def downloadvideo(link,path='./'):
    # try:
    #     common.any_download(link=link,output_dir=path,merge=True)
    #     # os.system('you-get -o {} {}'.format(path, link))
    # except:
    #     pass
    common.any_download(url=link,output_dir=path,merge=True)
