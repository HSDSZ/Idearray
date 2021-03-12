import json

def defaultconfig():
    with open('./idearray_config.json','w',encoding='utf-8') as json_file:
        json.dump(defaultdict,json_file,ensure_ascii=False)

def readconfig():
    try:
        json_file = open('./idearray_config.json','r', encoding='utf-8')
    except:
        defaultconfig()
        json_file = open('./idearray_config.json','r',encoding='utf-8')

    data = json.load(json_file)
    json_file.close()


    startupDB = data['startupDB']
    startupwidth = data['startupwidth']
    startupheight = data['startupheight']
    preferredlook = data['startuplook']
    return startupDB, startupwidth, startupheight,preferredlook


def updateconfig(key, value):
    try:
        with open('./idearray_config.json', 'r', encoding='utf-8') as json_file:
            dictionary = json.load(json_file)
    except:
        dictionary = defaultdict

    dictionary[key] = value  # or whatever

    with open('./idearray_config.json','w',encoding='utf-8') as json_file:
        json.dump(dictionary,json_file,ensure_ascii=False)


defaultdict ={
        'startupDB':'./idearray.db',
        'startupwidth':1400,
        'startupheight':900,
        'startuplook':True,
            }

if __name__ == '__main__':
    a = readconfig()
    print(a)
