import os
import re

def function_04(value,rule,excep):
    excep.append(' ')
    temp = value.strip().split(' ')
    value = ''
    for i in temp:
        value += i.strip() + ' '
    res = ''
    for i in value:
        if(rule == 'alnum'):
            if(i.isupper() or i.islower() or i.isdigit() or (i in excep)):
                res += i
        elif(rule == 'num'):
            if(i.isdigit() or (i in excep)):
                res += i
        elif(rule == 'alpha'):
            if(i.isupper() or i.islower() or (i in excep)):
                res += i
    return res.strip()

def function_01(text,ptrn,indx):
    length_text = len(text)
    length_ptrn = len(ptrn)
    for i in range(indx,length_text-length_ptrn):
        match = 0
        for j in range(0,length_ptrn):
            if(ptrn[j] == text[i+j]):
                match += 1
        if(match >= (7*length_ptrn/10)):
            return i
    return -1
    # not found
    
def function_02(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_1.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','output','part_1.txt'),'w')
    a_field = readFile.readline()[:-1]
    b_field = readFile.readline()[:-1]
    a_ite = function_01(text,a_field,0)
    # assume i get a valid index
    result = []
    while b_field:
        b_ite = function_01(text,b_field,a_ite+len(a_field))
        if(b_ite == -1):
            b_ite = a_ite + len(a_field) + 10
        # value lies between [a_ite + len(a_field) ... b_ite] 
        value = text[a_ite + len(a_field) : b_ite]
        
        if(a_field == 'Name'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Visit #'):
            value = function_04(value,'num',[])
            result.append(value)
        elif(a_field == 'MR #'):
            value = function_04(value,'num',[])
            result.append(value)
        elif(a_field == 'BirthDate'):
            value = function_04(value,'num',['/'])
            result.append(value)
        elif(a_field == 'Age'):
            value = function_04(value,'num',[])
            result.append(value)
        elif(a_field == 'Gender'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'SSN'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'MaritalStatus'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Patient Type'):
            value = function_04(value,'alpha',['(',')'])
            result.append(value)
        elif(a_field == 'Visit Type'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Visit Status'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Admitting MD'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Admit Date/Time'):
            value = function_04(value,'num',[',','/'])
            result.append(value)
        elif(a_field == 'Location'):
            value = function_04(value,'alpha',['-'])
            result.append(value)
        elif(a_field == 'Service'):
            value = function_04(value,'alpha',['-'])
            result.append(value)
        elif(a_field == 'Attending Physician'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Admit Source'):
            value = function_04(value,'alpha',['.'])
            result.append(value)
        elif(a_field == 'Admit Type'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Admitting DX'):
            value = function_04(value,'alpha',[',','/'])
            result.append(value)
        elif(a_field == 'Patient Address/Phone'):
            value = function_04(value,'alnum',['-','/'])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    i = 0
    file = open(output , 'w')
    fld = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_1.txt'),'r')
    key = fld.readline()[:-1]
    while key != 'Insurance PRIMAR':
        file.write(key + ' : ' + result[i] + '\n')
        i += 1
        key = fld.readline()[:-1]
    file.close()
    fld.close()

def function_03(fileLocation):
    result = ''
    fileInputHandler = open(fileLocation , 'r')
    line = fileInputHandler.readline()
    while(line):
        result += (line[:-1]) + ' '
        line = fileInputHandler.readline()
    fileInputHandler.close()
    return result

def function_05(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_2.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','output','part_2.txt'),'w')
    a_field = readFile.readline()[:-1]
    b_field = readFile.readline()[:-1]
    a_ite = function_01(text,a_field,0)
    # assume i get a valid index
    result = []
    while b_field:
        b_ite = function_01(text,b_field,a_ite+len(a_field))
        if(b_ite == -1):
            b_ite = a_ite + len(a_field) + 10
        # value lies between [a_ite + len(a_field) ... b_ite] 
        value = text[a_ite + len(a_field) : b_ite]
        if(a_field == 'PlanName'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Phone Number'):
            value = function_04(value,'num',['-'])
            result.append(value)
        elif(a_field == 'Subscriber Name'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Subscriber SSN'):
            value = function_04(value,'alnum',[',','-','[',']','(',')'])
            result.append(value)
        elif(a_field == 'Group Name'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Relation to Patient'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Group #'):
            value = function_04(value,'alnum',['-','/'])
            result.append(value)
        elif(a_field == 'Policy #'):
            value = function_04(value,'alnum',['-','/'])
            result.append(value)
        elif(a_field == 'Cert #'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Effective Dt'):
            value = function_04(value,'num',['/','-'])
            result.append(value)
        elif(a_field == 'Insurance Addr'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'City'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'State'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Zip'):
            value = function_04(value,'num',[])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    i = 0
    file = open(output , 'a')
    fld = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_2.txt'),'r')
    key = fld.readline()[:-1]
    while key != 'SECONDAR':
        file.write('Primary ' + key + ' : ' + result[i] + '\n')
        i += 1
        key = fld.readline()[:-1]
    file.close()
    fld.close()
    
def function_06(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_3.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','output','part_3.txt'),'w')
    a_field = readFile.readline()[:-1]
    b_field = readFile.readline()[:-1]
    a_ite = function_01(text,a_field,0)
    # assume i get a valid index
    result = []
    while b_field:
        b_ite = function_01(text,b_field,a_ite+len(a_field))
        if(b_ite == -1):
            b_ite = a_ite + len(a_field) + 10
        # value lies between [a_ite + len(a_field) ... b_ite] 
        value = text[a_ite + len(a_field) : b_ite]
        if(a_field == 'PlanName'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Phone Number'):
            value = function_04(value,'num',['-'])
            result.append(value)
        elif(a_field == 'Subscriber Name'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Subscriber SSN'):
            value = function_04(value,'alnum',[',','-','[',']','(',')'])
            result.append(value)
        elif(a_field == 'Group Name'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Relation to Patient'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Group #'):
            value = function_04(value,'alnum',['-','/'])
            result.append(value)
        elif(a_field == 'Policy #'):
            value = function_04(value,'alnum',['-','/'])
            result.append(value)
        elif(a_field == 'Cert #'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Effective Dt'):
            value = function_04(value,'num',['/','-'])
            result.append(value)
        elif(a_field == 'Insurance Addr'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'City'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'State'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Zip'):
            value = function_04(value,'num',[])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    i = 0
    file = open(output , 'a')
    fld = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_3.txt'),'r')
    key = fld.readline()[:-1]
    while key != 'Designated Representativ':
        file.write('Secondary ' + key + ' : ' + result[i] + '\n')
        i += 1
        key = fld.readline()[:-1]
    file.close()
    fld.close()

def function_07(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_4.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','output','part_4.txt'),'w')
    a_field = readFile.readline()[:-1]
    b_field = readFile.readline()[:-1]
    a_ite = function_01(text,a_field,0)
    # assume i get a valid index
    result = []
    while b_field:
        b_ite = function_01(text,b_field,a_ite+len(a_field))
        if(b_ite == -1):
            b_ite = a_ite + len(a_field) + 10
        # value lies between [a_ite + len(a_field) ... b_ite] 
        value = text[a_ite + len(a_field) : b_ite]
        if(a_field == 'Name'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Relationship'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Address'):
            value = function_04(value,'alnum',[',','/'])
            result.append(value)
        elif(a_field == 'Home'):
            value = function_04(value,'num',['-'])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    i = 0
    file = open(output , 'a')
    fld = open(os.path.join(os.getcwd(),'HospitalForms','RWJUH','part_4.txt'),'r')
    key = fld.readline()[:-1]
    while key != 'CONFIDENTIAL PATIENT INFORMATIO':
        file.write('Designated Representative ' + key + ' : ' + result[i] + '\n')
        i += 1
        key = fld.readline()[:-1]
    file.close()
    fld.close()

def function_11(location):
    linux = False
    for i in location:
        if(i == '/'):
            linux = True
            break
    arr = []
    if(linux):
        arr = location.split('/')
        arr[-2] = 'output'
        res = '/'
        for i in arr:
            res = os.path.join(res,i)
        return res
    arr = location.split('\\')
    arr[-2] = 'output'
    res = arr[0]+'\\'
    for i in range(1,len(arr)):
        res = os.path.join(res,arr[i])
    return res

def function_rwjuh(location):
    output = function_11(location)
    ocroutput = function_03(location)
    p = function_01(ocroutput,'Demographics',0)
    q = function_01(ocroutput,'Insurance PRIMARY',0)
    function_02(ocroutput[p:q+20], output)
    r = function_01(ocroutput,'SECONDARY',0)
    function_05(ocroutput[q:r+10],output)
    s = function_01(ocroutput,'Designated Representative',0)
    function_06(ocroutput[r:s+26],output)
    function_07(ocroutput[s:],output)
