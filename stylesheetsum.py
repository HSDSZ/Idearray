from images import *
# titlebar stylsheet
maxmode = ''' 
            QPushButton
            {background-image : url(:max.png);
            border-radius: 5px;
            border-width: 1px;
            border-color: rgba(244,244,244,0);
            background-color: rgba(244,244,244,0);
            border-style: outset;}
            QPushButton:hover
            {background-image : url(:max hover.png);
            background-color: white;}
            QPushButton:pressed
            {background-color: gray;}
            '''
originmode = ''' 
            QPushButton
            {background-image : url(:origin.png);
            border-radius: 5px;
            border-width: 1px;
            border-color: rgba(244,244,244,0);
            background-color: rgba(244,244,244,0);
            border-style: outset;}
            QPushButton:hover
            {background-image : url(:origin hover.png);
            background-color: white;}
            QPushButton:pressed
            {background-color: gray;}
            '''
hsdsz = ''' 
     QLabel
     {background-image : url(:head.png);}
     '''
down = ''' 
     QPushButton
     {background-image : url(:down.png);
     border-radius: 5px;
     border-width: 1px;
     border-color: rgba(244,244,244,0);
     background-color: rgba(244,244,244,0);
     border-style: outset;}
     QPushButton:hover
     {background-image : url(:down hover.png);
     background-color: white;}
     QPushButton:pressed
     {background-color: gray;}
     '''
up = ''' 
     QPushButton
     {background-image : url(:up.png);
     border-radius: 5px;
     border-width: 1px;
     border-color: rgba(244,244,244,0);
     background-color: rgba(244,244,244,0);
     border-style: outset;}
     QPushButton:hover
     {background-image : url(:up hover.png);
     background-color: white;}
     QPushButton:pressed
     {background-color: gray;}
     '''
minimize = ''' 
     QPushButton
     {background-image : url(:min.png);
     border-radius: 5px;
     border-width: 1px;
     border-color: rgba(244,244,244,0);
     background-color: rgba(244,244,244,0);
     border-style: outset;}
     QPushButton:hover
     {background-image : url(:min hover.png);
     background-color: white;}
     QPushButton:pressed
     {background-color: gray;}
     '''
closeicon = ''' 
     QPushButton
     {background-image : url(:close.png);
     border-radius: 5px;
     border-width: 1px;
     border-color: rgba(244,244,244,0);
     background-color: rgba(244,244,244,0);
     border-style: outset;}
     QPushButton:hover
     {background-image : url(:close hover.png);
     background-color: white;}
     QPushButton:pressed
     {background-color: gray;}
     '''
unpinned = ''' 
         QPushButton
         {background-image : url(:unpin.png);
         border-radius: 5px;
         border-width: 1px;
         border-color: rgba(244,244,244,0);
         background-color: rgba(244,244,244,0);
         border-style: outset;}
         QPushButton:hover
         {background-image : url(:unpin hover.png);
         background-color: white;}
         QPushButton:pressed
         {background-color: gray;}
         '''
pinned = ''' 
         QPushButton
         {background-image : url(:pin.png);
         border-radius: 5px;
         border-width: 1px;
         border-color: rgba(244,244,244,0);
         background-color: rgba(244,244,244,0);
         border-style: outset;}
         QPushButton:hover
         {background-image : url(:pin hover.png);
         background-color: white;}
         QPushButton:pressed
         {background-color: gray;}
         '''

# style of the showhidedetail button
pointright = ''' 
             QPushButton
             {background-image : url(:pointright.png);
             border-width: 0px;
             border-style: outset;}
             QPushButton:hover
             {background-image : url(:pointright hover.png);}
             '''
pointleft = ''' 
             QPushButton
             {background-image : url(:pointleft.png);
             border-width: 0px;
             border-style: outset;}
             QPushButton:hover
             {background-image : url(:pointleft hover.png);}
             '''

# style of the image and table version switch
imageversion = ''' 
                 QPushButton
                 {background-image : url(:image version.png);
                 border-width: 0px;
                 border-color: #F0F0F0;
                 background-color: #F0F0F0;
                 border-style: outset;}
                 QPushButton:hover
                 {background-image : url(:image version hover.png);
                 background-color: #F0F0F0;}
                 QPushButton:pressed
                 {background-image : url(:image version.png);
                 background-color: #F0F0F0;}
                 '''

tableversion = ''' 
                 QPushButton
                 {background-image : url(:table version.png);
                 border-width: 0px;
                 border-color: #F0F0F0;
                 background-color: #F0F0F0;
                 border-style: outset;}
                 QPushButton:hover
                 {background-image : url(:table version hover.png);
                 background-color: #F0F0F0;}
                 QPushButton:pressed
                 {background-image : url(:table version.png);
                 background-color: #F0F0F0;}
                 '''


# style of removable button
removebuton = ''' 
            QPushButton
            {background-image : url(:remove.png);
            border-radius: 5px;
            border-width: 1px;
            border-color: rgba(244,244,244,0);
            background-color: rgba(244,244,244,0);
            border-style: outset;}
            QPushButton:hover
            {background-color: white;}
            QPushButton:pressed
            {background-color: gray;}
            '''

# style of lineedit
searchbarstyle = "border-radius: 9px; border-width: 1px; border-color: rgb(100,100,100,80);border-style: outset;"
searchbarstyle2 = "border-radius: 5px; border-width: 1px; border-color: rgb(100,100,100,80);border-style: outset;"


# style of openlinkbutton in the detial area
smallopenstyle = ''' 
            QPushButton
            {background-image : url(:smallopen.png);
            border-radius: 5px;
            border-width: 1px;
            border-color: rgba(244,244,244,0);
            background-color: rgba(244,244,244,0);
            border-style: outset;}
            QPushButton:hover
            {background-color: white;}
            QPushButton:pressed
            {background-color: gray;}
            '''

# style of each image widget
defaultpic = '''QLabel
                {border-width : 0px;
                border-radius: 5px;
                border-color: rgba(100,100,100,80);
                border-style: outset;
                background-color : None
                }
                QLabel:hover
                {border-width : 1px;
                border-radius: 5px;
                border-color: rgba(100,100,100,50);
                border-style: outset;
                background-color : rgba(201,247,255,100)}'''

highligtpic = '''QLabel
                {border-width : 1px;
                border-radius: 5px;
                border-color: rgba(100,100,100,80);
                border-style: outset;
                background-color: LightSkyBlue}'''


# delete/open/like/later button sytle
todeletestyle = ''' 
             QPushButton
             {background-image : url(:delete.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-style: outset;}
             '''

recoverstyle = ''' 
             QPushButton
             {background-image : url(:recover.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-style: outset;}
             '''

likestyle = ''' 
             QPushButton
             {background-image : url(:like.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-width: 1px;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-width: 1px;
             border-style: outset;}
             '''

unlikestyle = ''' 
             QPushButton
             {background-image : url(:unlike.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-width: 1px;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-width: 1px;
             border-style: outset;}
             '''

laterstyle = ''' 
             QPushButton
             {background-image : url(:later.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-width: 1px;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-width: 1px;
             border-style: outset;}
             '''

unlaterstyle = ''' 
             QPushButton
             {background-image : url(:unlater.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-width: 1px;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-width: 1px;
             border-style: outset;}
             '''

openstyle = ''' 
             QPushButton
             {background-image : url(:open.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-style: outset;}
             '''

downloadstyle = ''' 
             QPushButton
             {background-image : url(:download.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: gray;
             border-style: outset;}
             QPushButton:hover
             {border-color: white;
             border-style: outset;}
             QPushButton:pressed
             {border-color: gray;
             border-style: outset;}
             '''

def previewicon(urltype):
    previewicon = ''' 
                 QPushButton
                 {{background-color: None;
                 background-image : url(:{type}icon.png);}}
                 QPushButton:hover
                 {{background-color: None;
                 background-image : url(:{type}icon hover.png);}}
                 '''.format(type=urltype)
    return previewicon

# styles in pop up window
addhierarchy = ''' 
             QPushButton
             {background-image : url(:addhierarchy.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: rgba(0,0,0,0);
             border-style: outset;}
             QPushButton:hover
             {border-color: gray;
             border-width: 1px;
             border-style: outset;}
             QPushButton:pressed
             {border-color: white;
             border-width: 1px;
             border-style: outset;}
             '''

deletehierarchy = ''' 
             QPushButton
             {background-image : url(:deletehierarchy.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: rgba(0,0,0,0);
             border-style: outset;}
             QPushButton:hover
             {border-color: gray;
             border-width: 1px;
             border-style: outset;}
             QPushButton:pressed
             {border-color: white;
             border-width: 1px;
             border-style: outset;}
             '''
deletehierarchy = ''' 
             QPushButton
             {background-image : url(:deletehierarchy.png);
             border-radius: 5px;
             border-width: 1px;
             border-color: rgba(0,0,0,0);
             border-style: outset;}
             QPushButton:hover
             {border-color: gray;
             border-width: 1px;
             border-style: outset;}
             '''
