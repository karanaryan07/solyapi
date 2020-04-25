def getJson(path,username,hospital):
    fileHandler = open(path , 'r')
    json = {}
    json['Doctor_ID'] = username
    json['Hospital_ID'] = hospital
    line = fileHandler.readline()[:-1]
    while line:
        arr = line.split(':')
        value = arr[-1]
        key = ''
        for i in range(len(arr)-1):
            key += arr[i] + ' '
        json[key.strip(' ')] = value.strip(' ')
        line = fileHandler.readline()[:-1]
    return json
