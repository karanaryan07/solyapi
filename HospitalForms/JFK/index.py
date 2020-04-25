import os
import re
import cv2
import numpy as np
from PIL import Image 
import pytesseract as pt 
import os 
import pytesseract as pt 
from itertools import chain

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
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_1.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','output','part_1.txt'),'w')
    a_field = readFile.readline()[:-1]
    b_field = readFile.readline()[:-1]
    a_ite = function_01(text,a_field,0)
    # assume i get a valid index
    result = []
    name = []
    while b_field:
        b_ite = function_01(text,b_field,a_ite+len(a_field))
        if(b_ite == -1):
            b_ite = a_ite + len(a_field) + 10
        # value lies between [a_ite + len(a_field) ... b_ite] 
        value = text[a_ite + len(a_field) : b_ite]
        
        if(a_field == 'Printed'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'MRN'):
            value = function_04(value,'num',[])
            result.append(value)
        elif(a_field == 'HAR'):
            value = function_04(value,'num',[])
            result.append(value)
        elif(a_field == 'Patient'):
            value = function_04(value,'alpha',[','])
            name = value.strip().split(',')
            result.append(value)
        elif(a_field == 'ENCOUNTER'):
            value = function_04(value,'num',['/'])
            result.append(value)
        elif(a_field == 'CSN'):
            value = function_04(value,'num',[])
            result.append(value)
        elif(a_field == 'Patient Class'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Unit'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Hospital Service'):
            value = function_04(value,'alpha',['(',')'])
            result.append(value)
        elif(a_field == 'Room/Bed'):
            value = function_04(value,'num',['/'])
            result.append(value)
        elif(a_field == 'Admitting Provider'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Adm Diagnosis'):
            value = function_04(value,'alnum',[',','.','(',')','[',']','*'])
            result.append(value)
        elif(a_field == 'Attending Provider'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Admit Source'):
            value = function_04(value,'alpha',['-'])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    i = 0
    file = open(output , 'w')
    fld = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_1.txt'),'r')
    key = fld.readline()[:-1]
    while key != 'PATIEN':
        file.write(key + ' : ' + result[i] + '\n')
        i += 1
        key = fld.readline()[:-1]
    fname = ''
    lname = ''
    if(len(name) > 0):
        fname = name[0]
    if(len(name) > 1):
        lname = name[0]
        fname = name[1]
    file.write('Patient First Name : ' + fname + '\n')
    file.write('Patient Last Name : ' + lname + '\n')
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
    pattern = '[0-9]{3}-[0-9]{3}-[0-9]{4}'
    pno = re.findall(pattern,text)
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_2.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','output','part_2.txt'),'w')
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
        elif(a_field == 'Race'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'DOB'):
            value = function_04(value,'num',['/','(',')','y','r','s'])
            result.append(value)
        elif(a_field == 'Address'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Ethnicity'):
            value = function_04(value,'alpha',['*'])
            result.append(value)
        elif(a_field == 'Sex'):
            value = function_04(value,'alpha',[])
            value = value.strip()
            adr = value.split(' ')
            for i in range(1,len(adr)):
                result[3] += ' ' + adr[i]
            if(len(adr) > 1):
                result.append(adr[0])
            else :
                result.append(value)
        elif(a_field == 'City'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Language'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'MS'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'PCP'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Religion'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Primary Phone'):
            value = function_04(value,'num',['-',])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    i = 0
    file = open(output , 'a')
    fld = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_2.txt'),'r')
    key = fld.readline()[:-1]
    if(len(pno) > 0):
        result[11] = pno[0]
    while key != 'GUARANTO':
        file.write(key + ' : ' + result[i] + '\n')
        i += 1
        key = fld.readline()[:-1]
    file.close()
    fld.close()
    
def function_06(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_3.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','output','part_3.txt'),'w')
    a_field = readFile.readline()[:-1]
    b_field = readFile.readline()[:-1]
    a_ite = function_01(text,a_field,0)
    # assume i get a valid index
    result = []
    first = True
    while b_field:
        b_ite = function_01(text,b_field,a_ite+len(a_field))
        if(b_ite == -1):
            b_ite = a_ite + len(a_field) + 10
        # value lies between [a_ite + len(a_field) ... b_ite] 
        value = text[a_ite + len(a_field) : b_ite]
        if(a_field == 'Guarantor'):
            if(first == False):
                value = function_04(value,'num',[])
                result.append(value)
            else :
                value = function_04(value,'alpha',[','])
                result.append(value)
            first = False
        elif(a_field == 'Date of Birth'):
            value = function_04(value,'num',['/'])
            result.append(value)
        elif(a_field == 'Address'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Sex'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Relation'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Home Phone'):
            value = function_04(value,'num',['-'])
            result.append(value)
        elif(a_field == 'Work Phone'):
            value = function_04(value,'num',['-'])
            result.append(value)
        elif(a_field == 'Guarantor Employer'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Status'):
            value = function_04(value,'alpha',[])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    file = open(output , 'a')
    file.write('Guarantor Name : ' + result[0] + '\n')
    file.write('Guarantor Date of Birth : ' + result[1] + '\n')
    temp = result[2]
    result[3] = result[3].strip().split(' ')
    if(len(result[3]) > 1):
        for i in range(1,len(result[3])):
            temp = temp + ' ' + result[3][i];
    file.write('Guarantor Address : ' + temp + '\n')
    file.write('Guarantor Sex : ' + result[3][0] + '\n')
    file.write('Guarantor Relation : ' + result[4] + '\n')
    file.write('Guarantor Home Phone : ' + result[5] + '\n')
    file.write('Guarantor ID : ' + result[6] + '\n')
    file.write('Guarantor Work Phone : ' + result[7] + '\n')
    file.write('Guarantor Employer : ' + result[8] + '\n')
    file.write('Guarantor Status : ' + result[9] + '\n')
    file.close()

def function_07(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_5.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','output','part_5.txt'),'w')
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
        if(a_field == 'Insurance'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Phone'):
            value = function_04(value,'num',['-'])
            result.append(value)
        elif(a_field == 'Plan'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Company'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Payor Name'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Subscriber Name'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Claim'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Address'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Eff From - Eff'):
            value = function_04(value,'num',['-','/'])
            result.append(value)
        elif(a_field == 'Pat. Rel. to'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Insurance'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'To'):
            value = function_04(value,'num',['/','-'])
            result.append(value)
        elif(a_field == 'Subscriber'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Type'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Group Number'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Subscriber ID'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Sub. DOB'):
            value = function_04(value,'num',['/'])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    file = open(output , 'a')
    if(result[0] ==  '' and result[2] == '' and result[4] == ''):
        for i in range(len(result)):
            result[i] = ''
    result[0] += ' ' + result[3]
    result[4] = result[0]
    result[6] += ' ' + result[7]
    result[8] += ' ' + result[11]
    result[9] += ' ' + result[12]
    result[10] += ' ' + result[13]
    file.write('PRIMARY Insurance Company : ' + result[0] + '\n')
    file.write('PRIMARY Phone : ' + result[1] + '\n')
    file.write('PRIMARY Plan Name : ' + result[2] + '\n')
    file.write('PRIMARY Payor Name : ' + result[4] + '\n')
    file.write('PRIMARY Subscriber Name : ' + result[5] + '\n')
    file.write('PRIMARY Claim Address : ' + result[6] + '\n')
    file.write('PRIMARY Eff From - Eff To : ' + result[8] + '\n')
    file.write('PRIMARY Patient Relation To : ' + result[9] + '\n')
    file.write('PRIMARY Insurance Type : ' + result[10] + '\n')
    file.write('PRIMARY Group Number : ' + result[14] + '\n')
    file.write('PRIMARY Subscriber ID : ' + result[15] + '\n')
    file.write('PRIMARY Subscriber DOB : ' + result[16] + '\n')
    file.close()

def function_08(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_6.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','output','part_6.txt'),'w')
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
        if(a_field == 'Insurance'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Phone'):
            value = function_04(value,'num',['-'])
            result.append(value)
        elif(a_field == 'Plan'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Company'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Payor Name'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Subscriber Name'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Claim'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Address'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Eff From - Eff'):
            value = function_04(value,'num',['-','/'])
            result.append(value)
        elif(a_field == 'Pat. Rel. to'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Insurance'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'To'):
            value = function_04(value,'num',['/','-'])
            result.append(value)
        elif(a_field == 'Subscriber'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Type'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Group Number'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Subscriber ID'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Sub. DOB'):
            value = function_04(value,'num',['/'])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    file = open(output , 'a')
    if(result[0] ==  '' and result[2] == '' and result[4] == ''):
        for i in range(len(result)):
            result[i] = ''
    result[0] += ' ' + result[3]
    result[4] = result[0]
    result[6] += ' ' + result[7]
    result[8] += ' ' + result[11]
    result[9] += ' ' + result[12]
    result[10] += ' ' + result[13]
    file.write('SECONDARY Insurance Company : ' + result[0] + '\n')
    file.write('SECONDARY Phone : ' + result[1] + '\n')
    file.write('SECONDARY Plan Name : ' + result[2] + '\n')
    file.write('SECONDARY Payor Name : ' + result[4] + '\n')
    file.write('SECONDARY Subscriber Name : ' + result[5] + '\n')
    file.write('SECONDARY Claim Address : ' + result[6] + '\n')
    file.write('SECONDARY Eff From - Eff To : ' + result[8] + '\n')
    file.write('SECONDARY Patient Relation To : ' + result[9] + '\n')
    file.write('SECONDARY Insurance Type : ' + result[10] + '\n')
    file.write('SECONDARY Group Number : ' + result[14] + '\n')
    file.write('SECONDARY Subscriber ID : ' + result[15] + '\n')
    file.write('SECONDARY Subscriber DOB : ' + result[16] + '\n')
    file.close()
    
def function_09(text,output):
    readFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','part_7.txt'),'r')
    writeFile = open(os.path.join(os.getcwd(),'HospitalForms','JFK','output','part_7.txt'),'w')
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
        if(a_field == 'Insurance'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Phone'):
            value = function_04(value,'num',['-'])
            result.append(value)
        elif(a_field == 'Plan'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Company'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Payor Name'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Subscriber Name'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'Claim'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Address'):
            value = function_04(value,'alnum',[','])
            result.append(value)
        elif(a_field == 'Eff From - Eff'):
            value = function_04(value,'num',['-','/'])
            result.append(value)
        elif(a_field == 'Pat. Rel. to'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Insurance'):
            value = function_04(value,'alpha',[','])
            result.append(value)
        elif(a_field == 'To'):
            value = function_04(value,'num',['/','-'])
            result.append(value)
        elif(a_field == 'Subscriber'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Type'):
            value = function_04(value,'alpha',[])
            result.append(value)
        elif(a_field == 'Group Number'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Subscriber ID'):
            value = function_04(value,'alnum',[])
            result.append(value)
        elif(a_field == 'Sub. DOB'):
            value = function_04(value,'num',['/'])
            result.append(value)
        writeFile.write(value + '\n')
        a_ite = b_ite
        a_field = b_field
        b_field = readFile.readline()[:-1]
    readFile.close()
    writeFile.close()
    file = open(output , 'a')
    file = open(output , 'a')
    if(result[0] ==  '' and result[2] == '' and result[4] == ''):
        for i in range(len(result)):
            result[i] = ''
    result[0] += ' ' + result[3]
    result[4] = result[0]
    result[6] += ' ' + result[7]
    result[8] += ' ' + result[11]
    result[9] += ' ' + result[12]
    result[10] += ' ' + result[13]
    file.write('TERTIARY Insurance Company : ' + result[0] + '\n')
    file.write('TERTIARY Phone : ' + result[1] + '\n')
    file.write('TERTIARY Plan Name : ' + result[2] + '\n')
    file.write('TERTIARY Payor Name : ' + result[4] + '\n')
    file.write('TERTIARY Subscriber Name : ' + result[5] + '\n')
    file.write('TERTIARY Claim Address : ' + result[6] + '\n')
    file.write('TERTIARY Eff From - Eff To : ' + result[8] + '\n')
    file.write('TERTIARY Patient Relation To : ' + result[9] + '\n')
    file.write('TERTIARY Insurance Type : ' + result[10] + '\n')
    file.write('TERTIARY Group Number : ' + result[14] + '\n')
    file.write('TERTIARY Subscriber ID : ' + result[15] + '\n')
    file.write('TERTIARY Subscriber DOB : ' + result[16] + '\n')
    file.close()

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

def function_12(text,output):
    pattern = '[0-9]{3}-[0-9]{3}-[0-9]{4}'
    pno = re.findall(pattern,text)
    yes = []
    no = []
    idx = function_01(text,'Yes',0)
    yes.append(idx)
    idx = function_01(text,'No',0)
    no.append(idx)
    I = function_01(text,'Primary Phone',0) + 17
    unknown = ''
    while not text[I].isdigit():
        unknown += text[I]
        I += 1
    file = open(output , 'a')
    name = unknown.split(' ')[0]
    rel = unknown
    lg = ''
    if(yes[0] != -1):
        lg = 'Yes'
    elif (no[0] != -1):
        lg = 'No'
    phone = ''
    if(len(pno) > 0):
        phone = pno[0]
    
    file.write('Emergency Contact Name : ' + name + '\n')
    file.write('Emergency Is Legal Guradian : ' + lg + '\n')
    file.write('Emergency Relationship to Patient : ' + rel + '\n')
    file.write('Emergency Primary Phone : ' + phone + '\n')
    file.close()

def function_jfk(location):
    output = function_11(location)
    ocroutput = function_03(location)
    p = function_01(ocroutput,'PATIENT',0)
    function_02(ocroutput[:p+7], output)
    q = function_01(ocroutput,'GUARANTOR',0)
    function_05(ocroutput[p:q+9],output)
    r = function_01(ocroutput,'EMERGENCY CONTACT',0)
    function_06(ocroutput[q:r+17],output)
    s = function_01(ocroutput,'COVERAGE',0)
    function_12(ocroutput[r:s+9],output)
    t = function_01(ocroutput,'SECONDARY',0)
    function_07(ocroutput[s:t+9],output)
    u = function_01(ocroutput,'TERTIARY',0)
    function_08(ocroutput[t:u+8],output)
    v = function_01(ocroutput,'Referred By',0)
    function_09(ocroutput[u:v+12],output)

    

