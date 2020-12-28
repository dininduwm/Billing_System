import json

# save data to the conf file
def saveConf(data):
    with open('settings/conf.json', 'w') as file:
        file.write(json.dumps(data))

# get data from the file
def loadConf():
    with open('settings/conf.json', 'r') as file:
        return(json.loads(file.read()))

