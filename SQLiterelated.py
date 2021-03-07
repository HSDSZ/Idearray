from PyQt5.QtCore import QByteArray
from PyQt5.QtSql import QSqlQuery
from datetime import datetime
authorpage = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x18\x00\x00\x00\x9e\x08\x06\x00\x00\x00\xe9\x10\x15\xfd\x00\x00\x00\x01sRGB\x01\xd9\xc9,\x7f\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95+\x0e\x1b\x00\x00\x12\x84IDATx^\xed\xdd\t`Se\x82\x07\xf0\x7f\xce\x1e\xd0\x0bh\x01\x91\xd3\x16\xb9t\x05E\xc6T\xc7u\x14\xa1E\xe4pe\x9det\x1c\x07Z\x16\x97\xb6\n\x08:\xacx\xcc0\x8b \x9b\xea\x08RA\xee\x9d\x01\xe4\x10\xa5EYEG\xa9\xa2#8\n\xad\xb4\xf1@\x199\x8aP\xa0-m\xd2\xe4\xcdK\xfa%Mh\x9b\xa6\xc7W\x92\xf2\xff\xe9\x83\xbc\xef}\xc9\xfbr\xbc\x7f\xbe\xf7\xbe\xf7\x82FQ\x81\x88H\x02\xad\xf8\x9b\x88\xa8\xd51`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914!\x170\x8a\xa2\xe0\xbd\xf7\xde\xc5;\xef\xec\xc6\x7fL\x7f\x10Q7\xf4\xc3UK\x1fF\x87\xc1W\x8a\x1aD\x14,4\xea\x06\xab\x88\xdb!!cf&^\xdd\xb4\xde\x154\x9a\x1b\x13\x91p\xdb0T\x195\xb8\xb0h\x0bN[N\x8aZD\x14\x0cB.`bW\xfd\'\xca\xf4\x80]\xed{i\xb5Zh\xed\n\x12\nO\xe1\xc2\xfa=8}\xa4D\xd4"\xa2`\x102\xbbH\xd1W]\x81A\x0b\x7f\x83Jg\x8b5\n:|\xf45:\x9f\xb7C\xcd\x1a\x94\xbd\xf39f\xcd\x98\xe9\xaaGD\xc1#d\x02\xc6\xe8p\xc0z\xbc\x14UaZ\xc4]P\xe7\xafODi\xa4\x16\xd1\xe5j\x07\xac\xe4\x1c\x9e\x985W\xd4$\xa2`\x112\x01S\xa1T#\xaaO\x0fDT)\xd0\x18\x0c\x88\xfb\xa6\x14\x8e\xc7\xd6C;\x7f3\xce~}\\\xd4"\xa2`\x122\xc7`6nX\x8f\xa5\xebV\xe1\xab\xa2B\xb5\xd1z\xac|9\x07cF\x8d\x16K\x89(\x18\x85\xd4A\xde\xad[\xb7b\xe2\xc4\x89b\x8e\x88\x82]\xc8\xec"\xcd\x993\x1b\x193\x1e\x16sD\x14\nB\xa6\x07\xd3\xbd[\x02:u\xea\x84C\x05_\x89\x12"\nv!\xd3\x83\twT3\\\x88BL\x9b\x04\xcc5=\xfb`\xd7\xae]b\xaey\x14\xa3C\xdc"\xa2P!e\x17\xa9\xa7y*\xf46\x07Nv\x0bCD\x15pj\xcaR\xb1\xa4\xe9\x8a\x0b\x0b0:%\x19\x19\x0f\xcfC\xe6l\x9eLG\x14J\xa4\xf4`t\xe1FXc\xc3\x11]\xe6@\x98\xbde\xf95i\xe2x\xf4\xe8hhv\xb8TVVb\xcc\xc8Qb\x8e\x88\xda\x92\x94\x80\xb1\xeb4\xb0\x19\xb4\xa8\x0e\xd7A\xd1hDi\xf3$F}\x8f\xc5s"\xc5\\\xd3\xdc\x956\x19?\xff\xd5x\xec\xdc\xfd\x96(!\xa2\xb6$u\x14i\xce\x82\xa7\xb1c\xfbk(\xfc\xe4KQ\xd24\xeb\xd6\xbe\x8a=k\xa7\xe1\xc3\xaf\xa2Pt\xf4\'Q\xda\xb0.\xb7_\x8f\xe8\xe4DT\xf6\xeb\x8a\xd3\xbajt\xfa\xb0\x18?.\xdf-\x96\x12Q[\x93>L}\xea\xc4qt\xe9\xdaM\xcc5\xcd\xb8\xbboF\xf5\x91b\x1c<a\xc3\x91\xe3\xa7Ei\xc3\xba\xad\x98\x81\xaaH\x05\xa5\x06\x05\xc6\x0b\x0e\xe8\xd7}\x80\xf2\xdd\x07\xc5R"jk\xd2G\x91\x9c\xe1\xb2\xf4\x91\xbe\xf8\xc3C\xd1H\xbe\xf1:Q\xea\xdf\x9e\xdd\xdbqS\x9fH\xcc\x1c\xf9\x03v\xfe\xfdD\xa3\xe1b\xb1X`\xb8\xae7\x1c\xb0\xa3s\xd1\x19t?i\x83Q}j\xfa\n\x8e<\x11]Jm2L\xfd\xf2_\xcaQr2\x12\xa5\xdf\xfdC\x94\xf8\xf7\xe4\x13\xcfb\xe6\x03]\xd09\xb6\xf1\xdd"\xa7\x95kV\xa3\xdb\x80\xab\x10\xf9\xe39|\xfd\xf1>T\x85\xeb\xa0\xab\xac\x86\xedl\x99\xa8AD\x97B\x9b\x9e\xc9;\xa0W<F$\x96C\x13?\x1a\xab7n\x15\xa5\xbe\xe6f\xfd\x0eW\x1b^\xc6s\xdb;c\xc3\xa6u\x186t\x84X\xd2\xb0\x11#F`\xdf\xbe}\xf8\xa2\xf0K<\xb3\xf2O(\xd8\xf79\n>\xd8\'\x96\x12\xd1\xa5\xd2&\x01S\\\\\x8cYY\x8f \xec\xdc\xc7\xe8\x93`\xc3\xa9\x0bvt\xb9&\r\x0b\xff\xe7yh\xbcF\x99\x9cM\xe9\xdd\xa1#:\xc5\xd9\xb1.\xf7o\xb8\xe6_\x86\x88%\r{\xf3\xcd7\xb1\xf8\xe9\x87\xa1\x18{\xe0\xfd\xbd\xf9\xae\xb2/\n\x0e\xe1\xdaA\x83]\xb7\xa9\x96%;\x1d\x8b\n\xd4\x1b\x83\xc6cvf\n\x12k\x8a]\xfc-\xa3\xc6\xb5\xc6\xeb\xe7y\x0c\x0c\xc2\xec\xe5\x99\xed\xe3=p\x06LKm\xdc\xb1M\xb9PU)\xe6|\x1d8p@I\x88\x8fUbc"\x95\x82CE\xae2\xab\xd5\xa6\xa4\x8f3(\xe6\x19W*C{wV\xe6fe([6\xbf\xa6\x0c\xbc\xa2\xabrxC/e\xe9\xb2lW\xbd\xc6\xf4\xebjP\x16L\x1b\xa0\xbc\xfaR\x8e(\t2\xc5\xc5Jnn\xaekRo\x06\xa69\xf7\tPn\x1a\x9c_&\nLf\xe5\xe2\x87\xf6\xb7\x8c\x1a\xd7\x1a\xaf\x9f\xe71\x90\xa6\xe4\x8a\xb2P\xd7\xe2c0\xfa\xe1}\xf0\xdb3\xbb\x11\xb59\x03\x11\x7f\xfe/tX7],\x01v\xef\xde\x8d~\xfd\xfa\xe1\xc4\xc938SZ\x8e\x81\x83\x92\\\xe5\x06\x83\x1e/o\xb7"\xf3\x85\x1f\xb0\xff\xbbS\xb8-e\x0c6\xae_\x89\xfb\xef\xac\x84\xc6z\x01\xdfn\x99\x8b%\x7f\\\xe2\xaa{\xb1\xa1}\xe3\xb0v^\x0f\xf4\xea\x1c\x83\xaf\x8f[\xf1\xf8\xb2B\xfcf\xfaT\xb14\xc8\x14/Bjj\xaakZT,\xca\x1a\xd3\x9c\xfb\x10\x05\xa9\x16\x07L\xbf\x9b\xafG\x95\x0e\x888|\x02\x11eU\x80\xbdZ,\x01F\x8e\x1c\x89\xe8\xe8h1\xd7\xb0;\xef\xbc\x13\x1b\xb7\xe7\xe2\xf1U\xa5\x18\xf5\xb8\x11\xf7\xdc\x17\x8b%\xe6\xe7\xb1b\xc5\nQ\x03x\xf7\xed\xb7p]\xf7\x18\xfcrd9\xcc\x9bc\xf1\xfdOg\xc5\x12"\nV-\x0e\x98\xd4\xce\x03\xb0"\xf2\x16\\\xff\xf19d\x9c\xbc\x12\xebcZvZ\xfe7\xc7\x8e\xe2\xb9\x97J\xb0\xcblG\xc1\x1b\xff\x8d\xf2\xf22L\x9f\x92\x86\x84S\xbf\x82Vo\xc7c9V\xec?|H\xd4&\xa2`\xd6\xe2\x801\xcf\xfb\x03\x1e\x98p\x1f\xf6\xbc\xfd.\x9e\xfa\xdd|L\x98p\x8fX\xd2|\x07\x8fu\x81\xc3~\x16S\xc7+H\xea\xd3\x13e\xdf\xbc\x86\t\xd3\xb5\xf8\xec\xfb\xf3\xa2\x06\x11\x85\x8269\x0f\xa6\xa9\xfe\xb4\xeaed=\x0b\x9c\xa9\xb0\xe3\x9d\x17\xa3p\xc3\x10\x07\x8aKO\xf8\x8c8\x11Q\xf0\x0b\xca\x80\x199z\x1c\xde\xfc\xac\x04Y\xab:c\xf2#e\xd8\xf5e\xe3\xc3\xd5\x97#K^6\xd2\x93\x93\x91\xac\x06\xaf3|\x93\xd5\xdb\xe9\xd9y\xb0\x88\xe52X,y\xc8NW\xd7\x99\\\xb3N\x8d\xc6y\xbb\xf9\xeb\xb5\xe4\xa5#=\xdd9e#O\x94\xd5\xe1|\x9e\x8d\xd4\xf1<N\x03\xedhn\xbb\x9dC\xc7>\x8f\xeby\x1c\xe7\x94\x8e\xbc&=i\x8b\xab\x9d\xce\xfb\xd6\xb4\xc1\xf9\x9e\xa5#\xbbi\x0f\x12Z\xc4hR\xd0\xfab]o\xe5\xee\xa1\x11b.\xc4\xe4\xa6\x89aG(i\x81\x8e;\x06t\x9f\\%\xcd\xe4\x1e\xd2\xaco2)\xe6z\xc6J[6L]\xac\x98\xfd\xae\xd39\x99\xd467q\x906\x80\xe7[;|\xdbP\x1d\xaf\xb6\xd5\xa9\xd0\xb2v\xfb\xbe.\xea\xeb~\xd1\xfd\xdc\xafs\xa3\xaf_\xb1\xff\xf7\xcc\xa4\xb6\xbb\xf6yr\x98\xba\xcdL\x9es\x12w\xdc\x1a%\xe6H\xfd:G\xba&\x159\xaes\nMH3\xe7\xbaNdtM\xea\'\xd4\xe4\xaa\x93\x8f\xac$\xf5\xdb\xd5u\xbb58\xd7\x99\x84\xac\x9a\xf3\x18a2\xa5\xc1\x9c+\xd6Y\x9c\x8b\\s\xedzsR\x93\x90\xde\x94\x15\xa7\x8c\x87\xba\xd1\xba\x1c,\xaa\xef\x9b<\x0f\xdbs\xc4MU\xce\xf6\xfa\x1e\xbc\x18\x05\xa2mi\xe3Sjn\xb8\xb4n\xbbw\xa6\xab\xaf\xbb\xfa\xb7)-\ri\xae)\xd0\x9e\xb5\xda\x8e$\xf7{\xe6\xbc\xbf\x19\xb9\x9e\xf7\xcc\x0c5x\x90\x9f\x93\x8aT\xaf\xe7\xd9n\x88\xa0\tZ\xa3\xef\xb8]\xe9\xdf#^\xcc\x85\x18\xafog\xf5\xc3\xad\xa8\x1f\xca\xc6\'\x93\xc9s\x9f\xfa\xbe\xadk\xbf\xe5\xea\xef\xa5(\xc5fE\xfd\xbc\xd6\xac\xf3\xa2\n\xfe\xbee\x03Z\xa6N\r\xf6P\x9c\xdf\xd0\xa2NS\xbf\x81\xfd\xad[]\xe8Yw\xe3u|\xd7\xdb\x1a\xed\xf6~\x8c\x06_sU\xcb^?\xb5o\xe4\xb3\x9e\xf6\xd3\x83\t\xfa\x80qz\xe2\xd1,\xa5_\xb7\xeeb.\x84\\\xbcq4q\xaa\xdb\xdbo8<\xbc5\xf4a\x0fh#\xb8x\x99\xd7:\xeb\xee~\xf8*6\xfb\x0f\xc7\x86\xd4\xde\xaf\xee\x06\xec^f2\x9bE\x10\xd4\xadSo\xdb[\xa9\xdd\xde\x1b~s^\xf3\xc0\xdb\xd1\xfc\x80\x0efA\xbf\x8b\xe44w\xfe|\xc4\x85\x03\xc7\x8f\xfd(JB\x91I\xed\xa2\x070\x89\xda\xf5*.P;\xf3N&L\x1a\xd3\xf0\x95*I\x83\xc4\xa3\xe4o\xc2\xce\x16\x1e?\xb4\xec\xdc$\xd6\xa9~\xec}v?\xeaJ\xcc\x9c\xe7\xd9\xdd\xa9\x7fW\xa6~\x89c&yvU\n|\xce^\xb6`\xe7&\xe7\xda\x9d\xcf7\x13\xe3]\x0f\x9e\x8fM>O\xca\x82"\xf1\x93?\xa6Ic<\xd7\xef\xb4~\xbb\xfd\xbf\xe6\r\xf2\xbcg\x8d\xb5#E<\xbf\xf6Ej\xc0\xdc\xfe\x8b\x7f\xc5\x9bol\x13s\xcd\x17\x1e\x11\x01\x87C\x83\xb8\xb8N\xa2$\xf4\xa4\xe5\xee\xc5\xde\xbd\x01L\xeaWaC\xf2<\x07#\xf2\x91\xf5k\xf7HF\xdd\xe9\xd7\xee\x83\x0e\xad\xa0\xd8}pC\xdd\x04\x1b\xd9NUIpg\x1b\x0e\x16\xf9\x1d\x9d\xf1\x918\x06\x93\xc4\xfd|6p\xcbN\xb8\xf2\x05C\xd0_\xdd\xb6\xdd\xc1\x99\xef\x9dB\x9e:\xbe\x01\xd0\xfa\xed\xaeiCSY\xdc\xe9\x17P;\xda\x1f\xa9\x01S\xf8m\x11&=\xf5(z\xbc8\x15=\x16?\x88+\x9e\xf87$L\xfe9\xc2\x076\xed\x17\xeet:\x03\xceWV!,\\\xed\xc6P\x8d\xfc|\xf5\xff\x06&Q%t$bLm\xc2x\x0eN{z!i\xe3\xd5\xefw\xaf\x9e\x8eW\x1dO\x0f\xc14\t\xcd\xe9`\x04\xcc4H\x8d\xa1\xa6\xab\r\xba\xcb\x93\xd4\x80)S\xf3 \xe1\xc6A8\x16o@I\xf7\x0e85\xb8+\xce\x8e\xb9\x16=f\xfe;\xfe7\xbb\xfe\x8b\x19\xeb\x939u\n\xb4\x0e\xbb\x98#\xe7\xb7\xb597\x17\xb9\x8dN\xf3\xe4nt\xad\xa8v7\xe9 \xdc\x83I\xee\x8d\xd3\xb3k\xe1\xe9\xe9\xe4\xc0\xdd\xd1q\xf7\xea\xbcw\x8f(xH\r\x18}\x99\x1dG\xf2?G\x84\r\x88\xb5\x02\x8ee\xb90\x9e\xaf\xc6\x0f\xe1V<\xb5c\x95\xa8\xe5\xdf\xc0nq\x08;\xbd\r\xd5\xc60Qr\xf9\xf2\x1c[qJJAJJ\xe3SK7\xba\xdau\xd6n\xf8\r\xab\x1d.\xc6\x90\xfeM[wb\x7fu\'\xc4\xc9}\x8c\xc5=<\xed\xbdk\x91\x88\xfebd\xb8fH\xbb\xf6\xf8\xcb\x90\x8b\xf6_\xda\xac\xdd\x01\x0b\xa4\x1d\xed\x8f\xd4\x80\x99v\xffoa\xb8P\x8d*\x9d\x06%F\x07\xae\xb8?\x15qJ\x18\xf4v\r\x12\xc6\xdd,j\xf97\xb8g%&\x8f\xed\x88\xc1\x83y6o\xa2{\xebR7B\xdf\x83\xa1\xf2x\xaf\xd3\xf7\xe0j=,E\xeafT\xc3$~\x9a#p\xb5\x079]\xc7X\xf2\xb6\xbb\xce9q\xef\x1e\xb9\xa5\x88J\xf9\x9bv\xc2\xe29\xfeR\xf7\xf8F\xdb\xb5\xdb?w{\x1b\x7f\xcf|\xcf\xf7i/\xa4\x06\xcc\x82\x05\x0b`-:\x81.e\n\xa2\xab\x80\x1fc48\x17^\x8d\x0b\xab\xdfBY\x8c\x11?[:K\xd4l\xd8\xdc\xe9\x11\xd0\xea\xaa1e\xca\x14Qr\x19\xf3:)-\xe7\xf7\xd9\x81\x1fDm\t\xafu\xe6g-\xaa=\xf6Q\x8f\xbcEY\xeaf\xe4\x94\x86y\x99M\xef\x07x6\xc6\x9c\xedH\x17[[\x9d\x91\x17w{\x9c#d\x17\x1d\xa3\xf1\xd1\x86\xed\xf6+i\x90\xd8\xf5\xf3\xff\x9eY\xb2\x7f_\x13\xa8\xed\x8c\xd4\x80q\xd3\xe6\xbc\x03l\xf8\x10\xd1{\x8a\xa0\x7f\xbf\x00Q]\xba\xe0\xe43\x1b0\xf0\xd0\x19Q\xa3a\xe1\x0e\x1b\x8cJ\x05\xee\x9et\x9f(i\xba\x13\'N\x88[\xa1.\x05\xb3\xcd\xe2\xe3\x9a\x9f\x85\xa4\xe4\xecz\xaf\x85q_\xa3\x94\xdd*\t\x94\x82\xe5\x9e\x91\xad\x1c\xa4\xd6{\xed\x8c\x05y\xe9\xc9\x9e3QM\xe6\xd9u7\xf8@xB!\x0795\xdd\x97zF^\xdc#>\xf9\xc8\x12\xa3e\xf5\x0f\xff\xb6a\xbb\xfdI\xcc\xc4\xbc\xda\xa4\xab\xe7=S\xdb\x90\x9d\x8c\xa4V\x1c\xf9\x0b*\xe2|\x98Kf\xda\xb44%!\xa1\x8b\xb2x\xf1bQ\xe2\xeb\xf3W\xa2\x94C\xab;\x89\xb9\xa6\xb3Z\xadJ\xd4\xd8aJ\x87\xfbG(\xfa>\x9d\x94n\x03\xfb\x8a%m \x80\xebl\xeah\xf4>\x17\x9f\xf5\xe9\x9cL\x8a\xc9T3y\x97\x05tB\x9a\xe0o\x99\x93\xf7\xc9h\xee\xc7\xafY\xa7w\x99\xff\x93\xd1\x02\xe1\xf3\xdc\x02jK\xc3g\xd7:\xb5\xb4\xdd\x8d\xbd.n\xfe\xeb\xd5s\x1d\xd2\xc5\xef\x97\xfaf\xd7>w\x9eh\xd7j\x96-[\xae\xf60J\x90\x91\x91\x81\xf1\xb7\xc4c\xe2X\xdf\xdf\x931\xea\xd4W\xdcn\x13sM\xa3\xbf2\x06\xf1\x1b\xb2\xa0L\xbc\x11\x95\xa97 \xf6\xe9\xc9\xa8xj\x1cz\xbd\x9a\x81\xbeK\xa6\xa0\xb4\xf4\x9c\xa8\x19J\x12\x91\xb2\\A\xb1\xe7:\x1a\xa7\xda!j\x17u\xebI\xcb]\x83\xd6\xec\xed\'f\xee\xf5\\7S\xc3\xbdN1+\xae\xf3\xd9\xdb\xc2\x95z\x1f\xc8nhd\xa8v\xc4I\xd5\xc8\xf0t[\xb5\xdb?\xb57\xb5\xb7\x18\xe6\xdaF\xa8\xcdp\xbf_\xe2z\xb2\xe5\xad\xdew\n\nm\xfa\xcf\x964\xe6\x8a\xe8Xl\\\xdc\x07\xb1\xc3_\xc55C\x87\xb9\xca\x0e\xae\x8d\xc1\xd9R#\x923J\\\xf3\xde\n\x0e\x16b\xc7\x1b[\xb1~\xd9\x93\x18t\x95\x01\xb11\x1dq\xe4\x98\x16GOF\xe0\xd0\xb7G\xd0\xdf<\r\'c\xb4\xa8\xd4+Pv\xedG\xf5G\x168\x14\x07b\xe6\xdd\x07E\r\xae\xf2\x85[\xa1?U\x8e\xca\x92\x10\xfe\xf7\x93,\x16X\x9c\x17\xcd\xa97\x93\x92\x92\xd4-*Q\xd2(\x887u\x9d\x16\xe7\xc5z\xeaMu\x9dIm\xb2\xce\xd6\x10\x0c\xed\xaem\x83\xf3\xfdJT\xdb\xd0\x9e\x05U\xc0\xb8\xed~\xae3\xfat\x0f\xc3yk\x05\xce\x95t\xc0\xcc\x85\xa7\xd0\xfb\xea\x04\x0c\xeco\xc3\xa9\x12\x1b\xbe?\xd3\x03\xc3\x7f\x91\x82g\x16,\x14\xf7\xf0\xaf\xffh\x13l\xbf\x1c\x81\xe3av\xd8\xed\xea\xa4\xf6\xdb\xf4\xea\x1f\xca\xcc\xb5\xe8h\xd3\xe0\x81\x07\x1e\xc4\xf9\xf3\xe7\xb1r\xe5Jq\x0f"j\rA\x190\xb7\xdet\r\xee\x19\xf6\x03n\xbd^\x03\x9dR\rcx4\xee\x9e}\x0eS\xb2\x9e\xc1\xac\xc7\x1e\x11\xb5\x9a&\xe9\xba\x01\xb0t\xb4!\xb6\x7fo\xe8:F\xe0\xf4\x87\x7f\x87c\xffQ\xb1\x94\x88d\xb8\xe4\xc7`\xea\xb3dI\x0e\xd6l\xae@\xc9O\x1a \xc2\x88=\xfb\xcb\xf1\xc6\xfb\xfb\x9b\x1d.N\x9f\xfd\xf5\x13\x8c\xeat5\xcaw\x1d\x00\xde\xfe\x02\xf7^\xed\xb5?LDR\x04e\x0f\xe6\xea^\xf1X6K\x8b\xf8\xa8\n\x8c{\xc2\x80\xf7>\xfe\x14\xbdz_%\x96\x12Q\xa8\x08\xca\x1e\x8c\xc6aCTx\x0540B\xe7\x08\xca&\x12Q\x00\x82j\xeb\xbdPY\x81\tw\xdf\x8b-\xf3\xab\x10\xa5\xd7"\x12\n\x9e^\xb4\x88\xbd\x17\xa2\x10\x154\xbbH\x07\x0b\xf7#\xe7\xd1;\x90q\xaf\r\xb6\xb0\xce\x98\xfb\xc21\xbc\xff\xb9\x15\xa5UA\xb7\x07GD\x01\xba\xa4=\x98\xd4[\x93\xb1vN\x1c\x8a\xd6\xc5\xc3\xf8i\n\xf6\x16*\xf8\xabu\x11\x06N\xfe\x0e\xaf\xef\xabb\xb8\x10\x85\xb8K\xd2\x83),,\xc4S\x0f\xde\x84ySm\xd0\xebt\xf8\xf4p8\x9e^\xa3\xc1\xd7\xc7\xda\xcb5CD\xe4\xd4\xe6\x01\xd3?^\x87\'\xa7v\xc0\xf0~j\xf7I\x1f\x8e\xe9\x0b\xce\xe3\x85\xd7\x0e`\xe0\xb5\x03D\r"j/\xa4\x06Lee%\xb6m{\x1d]\xff\x91\x86\x9e\xdd\xf4\x80\xb5\x1a0\xeaq\xe0\xab0\xf4\x1d\xbb\x1d\xc3G\xdc(j\x12Q{$%`\x8a,\xc58v\xf4$\x0el\x98\x80[n\x88@G\xddY\xb5\xd4\x01}T$F\xcf4`\xf3\x8e\x1d\xb8n\xd8\xd0\x9a\xcaD\xd4n\xb5Z\xc0\x1c<\xfc%\xa6\xdf\xfb\x00"\xab\xbf\xc4K\x8fFBq\x9e\xbfb\xd0\x00\xba\x0e(J\xc8\xc6\xcd\xc9\xb7#:*V\xd4&\xa2\xcbA\xab\x04\xcc\xbdc\xc7`\xda\xa8O\xd1+\xca\x00\xc5z\xdeU\xa6\x84U#e\xc6\x05\x0c\x1e>\x1ao\xfc\xbf\xbf\xdf\x13#\xa2\xf6\xaa\xd9\xc3\xd4\x9b\xd6\xfc\x1fn\xea\x19\x87\xc2\xf5]\xf1\xec=\x9f\xe0Jc\x15lV\x074a\x06L}\xa5/\xb6X\x1e\xc57g\x15\x86\x0b\xd1e\xac\xc9=\x98\xd7\xb7n\xc4\x1f3&c\xf5\xfcph\xb5:\xd8\x15\x8d\xfa\xb7\x1e\xe7\xca\xf5x\xe8E#\x16/\xc9\xc1\xa8\xbbF\x8b\xdaDt9kR\xc0\x98\x86\x0e\xc1+\x99\xc7a\xb0Y\xe1\xd0i\xa08t\xa8\xd6\xd9\xf0\xde^;f\xac\xa8\x10\xb5\x88\x88j\x04\xbc\x8b4\xa4\xab\x1ekf\xfc\x00\x83\xf3\xe7+\xb5j\xafE\x8d%\xad\xc3\x8a\xb7>\xd2\xe3\x83\x9fn\x13\xb5\x88\x88j\x05\x140\xb3\'v\xc2\x96\x851p8j:;v(\xea\x1d5\xa8\x0e\xd3\xe3\xb0\xf5.l\xda\xb6\xd3UND\xe4\xcd\xef.\xd2\xea\xd5\xab\x91pt6\xfat\xab\x84N\xfd\xcf\xa1v[tjmg\xc0(\xd0c\xd9\x0e\r^|\xfd\'Q\x9b\x88\xc8W\x83=\x98G\xa6=\x8c\r\xcf\xcfDL\x07\x07J\xce\xe8QZ\xa9\x87\xc1\xa8EX8\xa0\xb39p\xect\x05v\x1d\xd0\x89\xdaDDu\xf9\xed\xc1\x1c\xd8\xff7<4v\x04\xacV=b"4\xe8\xd7\xd3\x8e\x91\xc9\x9d\xf0\xb3\x01v\xac\xdaV\x86Sq\x93\xb0b\xedZQ\x9b\x88\xc8W\xab\x9chGDT\x9ff\x9fhGD\xd4\x18\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\r\x03\x86\x88\xa4a\xc0\x10\x914\x0c\x18"\x92\x86\x01CD\xd20`\x88H\x1a\x06\x0c\x11I\xc3\x80!"i\x180D$\t\xf0OWI\xb8\x82F9\x9c\x9e\x00\x00\x00\x00IEND\xaeB`\x82'

def createtable():
    # create a table named 'alldata' if there is no such table inside this database
    # deletedata table is used to save the deleted stuff
    query = QSqlQuery()
    query.exec('CREATE TABLE IF NOT EXISTS alldata(birthday INT, modtime INT, title TEXT, link TEXT, comment TEXT, tag TEXT, pixmap BLOB)')
    query.exec('CREATE TABLE IF NOT EXISTS deleteddata(birthday INT, modtime INT, title TEXT, link TEXT, comment TEXT, tag TEXT, pixmap BLOB)')
    query.exec('CREATE TABLE IF NOT EXISTS hierarchy(tag TEXT, children TEXT)')

    # insert author data if not exist
    if gettitlebybirthday(10000) != 'author of this sofware':
        query.prepare("INSERT INTO alldata (birthday, modtime, title, link, comment, tag, pixmap)"
                      "VALUES (:birthday, :modtime, :title, :link, :comment, :tag, :pixmap)")
        query.bindValue(":birthday", 10000)
        query.bindValue(":modtime", 10000)
        query.bindValue(":title", 'author of this sofware')
        query.bindValue(":link", 'https://space.bilibili.com/11925424?from=search&seid=8254168425775436573')
        query.bindValue(":comment", '')
        query.bindValue(":tag", '#author')
        query.bindValue(":pixmap", QByteArray(authorpage))
        query.exec()

def dbsize():
    query = QSqlQuery()
    query.exec("SELECT max(rowid) from alldata")
    query.next()
    rawsize = query.value(0)
    # when there is no data, rawsize is None. then replace it with 0
    return rawsize if rawsize != '' else 0

def getalltags():
    query = QSqlQuery()
    # read all tag column
    query.exec("SELECT tag FROM alldata ORDER BY link")
    # save tags into a list
    data = ['#like','#deleted','#later','#settings']
    while query.next():
        data += query.value(0).split()
    # remove the repeated tags
    return list(set(data))

def getallbybirthday(birthday):
    query = QSqlQuery()
    query.exec('SELECT modtime, title, link, comment, tag, pixmap FROM alldata WHERE birthday = {}'.format(birthday))
    query.next()
    if query.value(0) != None:
        return query.value(0),query.value(1),query.value(2),query.value(3),query.value(4),query.value(5)
    else:
        query.exec('SELECT modtime, title, link, comment, tag, pixmap FROM deleteddata WHERE birthday = {}'.format(birthday))
        query.next()
        return query.value(0),query.value(1),query.value(2),query.value(3),query.value(4),query.value(5)

def getallexceptpixbybirthday(birthday):
    query = QSqlQuery()
    query.exec('SELECT title, link, tag, comment FROM alldata WHERE birthday = {}'.format(birthday))
    query.next()
    if query.value(0) != None:
        return query.value(0),query.value(1),query.value(2),query.value(3)
    else:
        query.exec('SELECT title, link, tag, comment FROM deleteddata WHERE birthday = {}'.format(birthday))
        query.next()
        return query.value(0),query.value(1),query.value(2),query.value(3)

def operation_getbytag(tag):
     # decide which database we use
    dbtablename = 'deleteddata' if '#deleted' in tag else 'alldata'
    # split the searched text
    taglist = tag.split()
    # create an operation which search all tags inputs.
    operation = "SELECT birthday, title, link, comment, tag, pixmap FROM {}".format(dbtablename)
    for i in range(len(taglist)):
        if i == 0:
            operation += " WHERE tag LIKE '%{}%'".format(taglist[i])
        else:
            operation += " AND tag LIKE '%{}%'".format(taglist[i])
    return operation

def operation_getbytag2(tag = ''):
     # decide which database we use
    dbtablename = 'deleteddata' if '#deleted' in tag else 'alldata'

    # create an operation which search all tags inputs.
    head = "SELECT birthday, title, link, comment, tag, pixmap FROM {} WHERE (tag LIKE '%".format(dbtablename)

    # remove extra space
    tag = tag.replace(' #or ',"%')OR(tagLIKE'%")
    tag = tag.replace(' ', '% AND tag LIKE %')
    tag = tag.replace(')OR(', ') OR (')
    tag = tag.replace("tagLIKE'%", "tag LIKE '%")

    foot = "%')"
    return head+tag+foot

def operation_getbytag3(tag = ''):
     # decide which database we use
    dbtablename = 'deleteddata' if '#deleted' in tag else 'alldata'

    # create an operation which search all tags inputs.
    head = "SELECT birthday, title, link, comment, tag, pixmap FROM {} WHERE (tag LIKE '%".format(dbtablename)

    # remove extra space
    tag = tag.replace(' or ',"%')OR(tagLIKE'%")
    tag = tag.replace(' ', "%' AND tag LIKE '%")
    tag = tag.replace(')OR(', ') OR (')
    tag = tag.replace("tagLIKE'%", "tag LIKE '%")

    foot = "%') ORDER BY birthday"
    return head+tag+foot

def getlinkbybirthday(birthday):
    query = QSqlQuery()
    query.exec('SELECT link FROM alldata WHERE birthday = {}'.format(birthday))
    query.next()
    if query.value(0) != None:
        return query.value(0)
    else:
        query.exec('SELECT link FROM deleteddata WHERE birthday = {}'.format(birthday))
        query.next()
        return query.value(0)

def gettitlebybirthday(birthday):
    query = QSqlQuery()
    query.exec('SELECT title FROM alldata WHERE birthday = {}'.format(birthday))
    query.next()
    if query.value(0) != None:
        return query.value(0)
    else:
        query.exec('SELECT title FROM deleteddata WHERE birthday = {}'.format(birthday))
        query.next()
        return query.value(0)

def getpixmapbybirthday(birthday):
    query = QSqlQuery()
    query.exec('SELECT pixmap FROM alldata WHERE birthday = {}'.format(birthday))
    query.next()
    if query.value(0) != None:
        return query.value(0)
    else:
        query.exec('SELECT pixmap FROM deleteddata WHERE birthday = {}'.format(birthday))
        query.next()
        if query.value(0) != None:
            return query.value(0)
        else:
            return authorpage

def getcommentbybirthday(birthday):
    query = QSqlQuery()
    query.exec('SELECT comment FROM alldata WHERE birthday = {}'.format(birthday))
    query.next()
    if query.value(0) != None:
        return query.value(0)
    else:
        query.exec('SELECT comment FROM deleteddata WHERE birthday = {}'.format(birthday))
        query.next()
        return query.value(0)

def gettagbybirthday(birthday):
    query = QSqlQuery()
    query.exec('SELECT tag FROM alldata WHERE birthday = {}'.format(birthday))
    query.next()
    # print(query.value(0))
    if query.value(0) != None:
        return query.value(0)
    else:
        query.exec('SELECT tag FROM deleteddata WHERE birthday = {}'.format(birthday))
        query.next()
        return query.value(0)

def updatebybirthday(birthday, link = '', comment = '3.141592653', tag = '', pixmap = b'\x00', title = ''):
    # decide which database
    oldtag = gettagbybirthday(birthday)

    dbtablename = 'deleteddata' if '#deleted' in oldtag else 'alldata'
    now = str(datetime.now())
    modtime = int(now.split(' ')[0].replace('-','')+now.split(' ')[1].split('.')[0].replace(':',''))

    updatewhat = (link != '')*1+(comment != '3.141592653')*10+(tag != '')*100+(pixmap != b'\x00')*1000+(title != '')*10000
    query = QSqlQuery()
    if updatewhat == 0:
        # updatewhat == 0, means link comment and tag are all emtpy
        pass
    elif updatewhat == 1:
        # update link only
        query.prepare("UPDATE {} SET link=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(link)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 10:
        query.prepare("UPDATE {} SET comment=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(comment)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 11:
        query.prepare("UPDATE {} SET link =?, comment=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(link)
        query.addBindValue(comment)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 100:
        query.prepare("UPDATE {} SET tag =?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(tag)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 101:
        query.prepare("UPDATE {} SET link =?, tag=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(link)
        query.addBindValue(tag)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 110:
        query.prepare("UPDATE {} SET comment =?, tag=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(comment)
        query.addBindValue(tag)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 111:
        query.prepare("UPDATE {} SET link =?, comment =?, tag=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(link)
        query.addBindValue(comment)
        query.addBindValue(tag)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 1000:
        query.prepare("UPDATE {} SET pixmap=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(QByteArray(pixmap))
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 10000:
        query.prepare("UPDATE {} SET title=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(title)
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    elif updatewhat == 11000:
        query.prepare("UPDATE {} SET title=?, pixmap=?, modtime=? WHERE birthday=?".format(dbtablename))
        query.addBindValue(title)
        query.addBindValue(QByteArray(pixmap))
        query.addBindValue(modtime)
        query.addBindValue(birthday)
        query.exec()

    else:
        pass

def deletebybirthday(birthday):
    if birthday == 10000:
        pass
    else:
        # remove one row from alldata table to deleteddata table
        modtime, title, link, comment, tag, pixmap = getallbybirthday(birthday)
        newtag = tag + ' #deleted'
        # do delete from alldata table
        operation = 'DELETE FROM alldata WHERE birthday={}'.format(birthday)
        query = QSqlQuery()
        query.exec(operation)
        # add it into deleteddata table4
        query.prepare("INSERT INTO deleteddata (birthday, modtime, title, link, comment, tag, pixmap)"
                      "VALUES (:birthday, :modtime, :title, :link, :comment, :newtag, :pixmap)")
        query.bindValue(":birthday", birthday)
        query.bindValue(":modtime", modtime)
        query.bindValue(":title", title)
        query.bindValue(":link", link)
        query.bindValue(":comment", comment)
        query.bindValue(":newtag", newtag)
        query.bindValue(":pixmap", QByteArray(pixmap))
        query.exec()

def recoverbybirthday(birthday):
    if birthday == 10000:
        pass
    else:
        # remove one row from alldata table to deleteddata table
        modtime, title, link, comment, tag, pixmap = getallbybirthday(birthday)
        # check if it is a deleted data
        newtag = tag.replace(' #deleted', '')
        #  recover data into alldata from deleted table
        operation = 'DELETE FROM deleteddata WHERE birthday={}'.format(birthday)
        query = QSqlQuery()
        query.exec(operation)
        # add it into alldata table
        query.prepare("INSERT INTO alldata (birthday, modtime, title, link, comment, tag, pixmap)"
                      "VALUES (:birthday, :modtime, :title, :link, :comment, :newtag, :pixmap)")
        query.bindValue(":birthday", birthday)
        query.bindValue(":modtime", modtime)
        query.bindValue(":title", title)
        query.bindValue(":link", link)
        query.bindValue(":comment", comment)
        query.bindValue(":newtag", newtag)
        query.bindValue(":pixmap", QByteArray(pixmap))
        query.exec()

def adddata(birthday, title, link, comment, tag, pixmap):
    query = QSqlQuery()
    modtime = birthday
    query.prepare("INSERT INTO alldata (birthday, modtime, title, link, comment, tag, pixmap)"
                  "VALUES (:birthday, :modtime, :title, :link, :comment, :tag, :pixmap)")
    query.bindValue(":birthday", birthday)
    query.bindValue(":modtime", modtime)
    query.bindValue(":title", title)
    query.bindValue(":link", link)
    query.bindValue(":comment", comment)
    query.bindValue(":tag", tag)
    query.bindValue(":pixmap", QByteArray(pixmap))
    query.exec()

def adddatawithoutpix(birthday, title, link, comment, tag):
    query = QSqlQuery()
    modtime = birthday
    query.prepare("INSERT INTO alldata (birthday, modtime, title, link, comment, tag)"
                  "VALUES (:birthday, :modtime, :title, :link, :comment, :tag)")
    query.bindValue(":birthday", birthday)
    query.bindValue(":modtime", modtime)
    query.bindValue(":title", title)
    query.bindValue(":link", link)
    query.bindValue(":comment", comment)
    query.bindValue(":tag", tag)
    query.exec()

def refreshalltags(currentalltags, taglist):
    for item in taglist:
        if item not in currentalltags:
            currentalltags += [item]

    return currentalltags

# below for hierarchy database

# def getallhierarchy(cursor):
#     operation = "SELECT tag, children FROM hierarchy"
#     cursor.execute(operation)
#     data = cursor.fetchall()
#     return data

def alltaginhierarchy():
    query = QSqlQuery()
    # read all tag column
    query.exec("SELECT tag FROM hierarchy ORDER BY tag")
    # save tags into a list
    data = []
    while query.next():
        data += query.value(0).split()
    # remove the repeated tags
    return list(set(data))


def addhierarchy(tag,children):
    query = QSqlQuery()
    query.prepare("INSERT INTO hierarchy (tag, children)"
                  "VALUES (:tag, :children)")
    query.bindValue(":tag", tag)
    query.bindValue(":children", children)
    query.exec()


def deletehierarchy(tag):
    # first delete tag
    query = QSqlQuery()
    query.exec("DELETE FROM hierarchy WHERE tag='{}'".format(tag))


def removechild(tag,child):
    query = QSqlQuery()
    query.exec("SELECT children FROM hierarchy WHERE tag LIKE '{tag}'".format(tag=tag))
    query.next()
    children = query.value(0)
    newchildrenlist = children.replace(child, '').split()
    newchildren = ' '.join(newchildrenlist)
    updatechilderen(tag, newchildren)

def addchild(tag,child):
    query = QSqlQuery()
    query.exec("SELECT children FROM hierarchy WHERE tag LIKE '{tag}'".format(tag=tag))
    query.next()
    children = query.value(0)
    if child not in children.split():
        newchildren = children+' '+child
        updatechilderen(tag, newchildren)


def removeparent(tag,parent):
    removechild(parent, tag)

def addparent(tag,parent):
    query = QSqlQuery()
    query.exec("SELECT children FROM hierarchy WHERE tag LIKE '{}'".format(parent))
    query.next()
    result = query.value(0)
    if result == None:
        # this parent not exists
        addhierarchy(parent.lower(), tag)
    else:
        # this parent exist
        addchild(parent.lower(), tag)

def searchchildren(tag):
    query = QSqlQuery()
    # first search the wanted tag
    query.exec("SELECT children FROM hierarchy WHERE tag LIKE '{}'".format(tag))
    query.next()
    result = query.value(0)
    if result != None:
        return True, result
    else:
        addhierarchy(tag.lower(),'')
        return False, ''

def searchparent(tag):
    query = QSqlQuery()
    query.exec("SELECT tag FROM hierarchy WHERE children LIKE '% {tag} %' OR children LIKE '{tag}' OR children LIKE '{tag} %' OR children LIKE '% {tag}'".format(tag=tag))
    parent = ''
    while query.next():
        parent += ' {}'.format(query.value(0))

    return parent[1:]

def updatechilderen(tag,children):
    query = QSqlQuery()
    query.exec("UPDATE hierarchy SET children='{}' WHERE tag='{}'".format(children,tag))

def expandstr(tag):
    query = QSqlQuery()
    # first search the wanted tag
    query.exec("SELECT children FROM hierarchy WHERE tag LIKE '{}'".format(tag))
    query.next()
    result = query.value(0)
    if result != None:
        sumlist = result.split()
        for item in sumlist:
            tag += ' {}'.format(item)
            # this children might contain new children
            query.exec("SELECT children FROM hierarchy WHERE tag LIKE '{}'".format(item))
            query.next()
            result = query.value(0)
            if result != None:
                newlist = result.split()
                for newitem in newlist:
                    if newitem not in sumlist and newitem != tag:
                        sumlist.append(newitem)

    return tag

if __name__ == "__main__":
    from PyQt5.QtSql import QSqlDatabase, QSqlQuery
    dbcon = QSqlDatabase.addDatabase("QSQLITE")
    dbcon.setDatabaseName('./idearray.db')
    dbcon.open()
    query = QSqlQuery()
    query.exec("SELECT tag FROM alldata ORDER BY link")
    while query.next():
        print(query.value(0))
