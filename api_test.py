from flask import Flask,jsonify,request,session,render_template,make_response
import bcrypt,os,pymongo

# from HospitalForms.JFKMedical.index import processor_01
# from HospitalForms.RWJUH.index import processor_02
from HospitalForms.ocr2txt import toText
from HospitalForms.returnsJSON import getJson

from HospitalForms.JFK.index import function_jfk
from HospitalForms.RWJUH.index import function_rwjuh
from HospitalForms.ocr2txt import toText
from HospitalForms.returnsJSON import getJson

from xlwt import Workbook

import json
import pdfkit
from json2html import *
from flask import redirect, url_for
import paypalrestsdk
import stripe

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongoClient['Hospital']

app = Flask(__name__)

json = {}

def checkCredit(eMail,cnt):
    minAmount = 5
    users = db['users']
    cursor = users.find_one(
        {'email':eMail}
    )
    if(cursor['credit'] < minAmount*cnt):
        return False
    else :
        users.update_one(
            {'email':eMail},
            {'$set':{'credit':cursor['credit']-minAmount*cnt}}
        )
    return True

@app.route('/verify',methods=['POST'])
def verify():
    # get email and form type as arguments
    eMail = request.args.get('email')
    formType = request.args.get('hospital')
    if(request.method == 'POST'):
        patient = db['patient']
        if(formType == '1'):
            file = open(os.path.join(os.getcwd(),'HospitalForms','jfk.txt'),'r')
            txt = file.readline()
            fields = []
            while txt :
                txt = txt[:-1]
                if(txt[-1] == ':'):
                    txt = txt[:-1]
                fields.append(txt)
                txt = file.readline()
            file.close()
            json = {}
            json['Doctor_ID'] = eMail
            json['Hospital_ID'] = '1'
            for i in range(len(fields)-1):
                json[fields[i]] = request.form[fields[i]]
            json['timeStamp'] = request.form['timestamp']
            json['fileName'] = request.form['filename']
            patient.insert({'result':json})
        elif(formType == '2'):
            # RWJU Hospital
            file = open(os.path.join(os.getcwd(),'HospitalForms','rwjuh.txt'),'r')
            txt = file.readline()
            fields = []
            while txt :
                txt = txt[:-1]
                if(txt[-1] == ':'):
                    txt = txt[:-1]
                fields.append(txt)
                txt = file.readline()
            file.close()
            json = {}
            json['Doctor_ID'] = eMail
            json['Hospital_ID'] = '2'
            for i in range(len(fields)-1):
                json[fields[i]] = request.form[fields[i]]
            json['timeStamp'] = request.form['timestamp']
            json['fileName'] = request.form['filename']
            patient.insert({'result':json})
        else :
            pass
        return jsonify({'output':{'result':'Uploaded to the database'}}) , 200
    else :
        return jsonify({'output':{'result':'Wrong Method'}}), 400

@app.route("/retrieve",methods=['POST'])
def retrieve():
    if request.method == 'POST':
        patient = db['patient']
        #email as given Argument
        email = request.args.get('email')
        #timeStamp as a argument
        # timeStamp = request.args.get('time')
        # #fileName as a argument
        # filename = request.args.get('file')
        # find the records in dbs 
        query= {}
        query['result.Doctor_ID']=email;
        if(request.form['filename']!=""):
            query['result.fileName']=request.form['filename'];
        if(request.form['hospital']!=""):
            query['result.Hospital_ID']=request.form['hospital'];
        records = patient.find(query,{'_id':0})
        ans=[]
        for x in records:
            ans.append(x)
        # del records['_id']
        # del records['password']
        # send the records as json data
        if records:
            return jsonify({'output':ans})
        else:
            return jsonify({'output':'no output to show'})

@app.route("/upload", methods=['POST'])
def upload():
    # email is given as argument
    eMail = request.args.get('email')
    if(request.method == 'POST'):
        cnt = 0
        for upload in request.files.getlist('file'):
            cnt += 1;
        if(checkCredit(eMail,cnt)):
            doctor = eMail
            hospital = request.form['hospital']
            target = os.path.join(os.getcwd(),'HospitalForms')
            json_array = []
            if(hospital == '1'):
                newTarget = os.path.join(target,'JFK')
                filename = ''
                for upload in request.files.getlist('file'):
                    upload.save(os.path.join(newTarget,'images',upload.filename)) #uploaded file will be saved as its original name
                    filename = upload.filename
                    toText(os.path.join(newTarget,'images',filename))
                    function_jfk(os.path.join(newTarget,'input',filename.split('.')[0]+'.txt')) #location of txt file
                    json = getJson(os.path.join(newTarget,'output',(filename.split('.')[0]+'.txt')), doctor , hospital)
                    json_array.append(json)

            elif(hospital == '2'): # 2 is for RWJUH
                newTarget = os.path.join(target,'RWJUH')
                filename = ''
                for upload in request.files.getlist('file'):
                    upload.save(os.path.join(newTarget,'images',upload.filename)) #uploaded file will be saved as its original name
                    filename = upload.filename
                    toText(os.path.join(newTarget,'images',filename))
                    function_rwjuh(os.path.join(newTarget,'input',filename.split('.')[0]+'.txt')) #location of txt file
                    json = getJson(os.path.join(newTarget,'output',(filename.split('.')[0]+'.txt')), doctor , hospital)
                    json_array.append(json)
            else :
                pass
            return jsonify({'output':json_array})
        else :
            return jsonify({'output':{'result' : 'Insufficient Credit'}})
    return jsonify({'output':{'result' : 'Wrong Method'}}),400

@app.route('/login', methods=['POST'])
def login():
    if(request.method == 'POST'):
        users = db['users']
        login_user = users.find_one({'email': request.form['email']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                return jsonify({'output':[{
                    'result':'login Successful',
                    'email' :request.form['email']
                }]})
            else:
                return jsonify({'output':{'result' : 'Invalid password'}})
        else :
            return jsonify({'output':{'result' : 'Invalid email'}})
    return jsonify({'output':{'result' : 'Wrong method'}}),400

@app.route('/signup', methods=['POST'])
def signup():
    if(request.method == 'POST'):
        users = db['users']
        existing_user = users.find_one({'email' : request.form['email']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({
                'first name':request.form['first name'],
                'last name':request.form['last name'],
                'email':request.form['email'],
                'password': hashpass,
                'dob':'01-01-2020',
                'address':'New York',
                'state':'New York',
                'city':'New York',
                'zip':'000000',
                'credit':100
            })
            return jsonify({'output':{'result' : 'Signup Successful'}}),201
        else :
            return jsonify({'output':{'result' : 'User with this email already exist'}})	
    return jsonify({'output':{'result' : 'Wrong method'}}),400
    
@app.route('/profile',methods=['GET','POST'])
def profile():
    # email is given as argument
    eMail = request.args.get('email')
    users = db['users']
    cursor = users.find_one(
        {'email':eMail}
    )
    if(request.method == 'GET'):
        return jsonify({'output':{
            'first':cursor['first name'],
            'last':cursor['last name'],
            'email':cursor['email'],
            'dob':cursor['dob'],
            'address':cursor['address'],
            'state':cursor['state'],
            'city':cursor['city'],
            'zip':cursor['zip'],
            'credit':cursor['credit']
        }}) , 200
    elif(request.method == 'POST'):
        users.update_one(
            {'email':eMail},
            {'$set':{
                'first name':request.form['first name'],
                'last name':request.form['last name'],
                'email':request.form['email'],
                'password': bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()),
                'dob':request.form['dob'],
                'address':request.form['address'],
                'state':request.form['state'],
                'city':request.form['city'],
                'zip':request.form['zip']
            }}
        )
        return jsonify({'output':{
            'first':request.form['first name'],
            'last':request.form['last name'],
            'email':request.form['email'],
            'password': bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()),
            'dob':request.form['dob'],
            'address':request.form['address'],
            'state':request.form['state'],
            'city':request.form['city'],
            'zip':request.form['zip'],
            'credit':cursor['credit']
        }}) , 200
    return jsonify({'output':[{'result' : 'Wrong method'}]}),400

@app.route('/buycredit',methods=['GET'])
def buycredit():
    # email is given as argument
    eMail = request.args.get('email')
    users = db['users']
    if(request.method == 'GET'):
        cursor = users.find_one(
            {'email':eMail}
        )
        users.update_one(
            {'email':eMail},
            {'$set':{
                'credit':cursor['credit'] + 100
            }}
        )
        return jsonify({'output':{'result' : 'Buy successful'}}), 200
    return jsonify({'output':{'result' : 'Wrong method'}}), 400

@app.route('/dashboard',methods=['GET'])
def dashboard():
    # email is given as argument
    eMail = request.args.get('email')
    if(request.method == 'GET'):
        users = db['users']
        cursor = users.find_one(
            {'email':eMail}
        )
        creditcount = cursor['credit']
        patients = db['patient']
        cursor = patients.aggregate(
            [
                {'$match':{'result.Doctor_ID':eMail}},
                {'$group':{'_id':'$result.Hospital_ID' , 'count':{'$sum':1}}}
            ]
        )
        hospitals = []
        values = []
        for doc in cursor:
            if(doc['_id'] == '1'):
                hospitals.append('JFK Medical')
                values.append(doc['count'])
            elif(doc['_id'] == '2'):
                hospitals.append('RWJU Hospital')
                values.append(doc['count'])
        res = {}
        res['credit'] = creditcount
        res['Hospital'] = {
            'name':hospitals,
            'count':values
        }
        cursor1 = patients.aggregate(
            [
                {'$match':{'result.Doctor_ID':eMail}},
                {'$group':{'_id':'$result.Primary Plan' , 'count':{'$sum':1}}}
            ]
        )
        cursor2 = patients.aggregate(
            [
                {'$match':{'result.Doctor_ID':eMail}},
                {'$group':{'_id':'$result.Primary PlanName' , 'count':{'$sum':1}}}
            ]
        )
        cursor3 = patients.aggregate(
            [
                {'$match':{'result.Doctor_ID':eMail}},
                {'$group':{'_id':'$result.PRIMARY Insurance Company' , 'count':{'$sum':1}}}
            ]
        )
        PlanName = []
        values = []
        for doc in cursor1:
            if(doc['_id'] == None):
                continue
            PlanName.append(doc['_id'])
            values.append(doc['count'])
        for doc in cursor2:
            if(doc['_id'] == None):
                continue
            PlanName.append(doc['_id'])
            values.append(doc['count'])
        for doc in cursor3:
            if(doc['_id'] == None):
                continue
            PlanName.append(doc['_id'])
            values.append(doc['count'])
        res['PlanName'] = {
            'name':PlanName,
            'count':values
        }
        return jsonify({'output':res}),200
    else:
        return jsonify({'output':{'result' : 'Wrong method'}}),400

@app.route('/postjson', methods=['POST'])
def download():

    req_json=request.form
    print(req_json)
    zeher=req_json.to_dict()
    render=render_template('hello.html',result=zeher)
    pdf=pdfkit.from_string(render,False,configuration=config)

    response=make_response(pdf)
    response.headers['Content-Type']= 'application/pdf'
    response.headers['Content-Disposition']='attachment; filename=output.pdf'

    return response

pub_key = 'pk_test_qRHg5HqQPcwOiCMO2VEOMyZc00zpi2ubxO'
secret_key = 'sk_test_dWFvz5PvrPqadlAZC6X0WSSU00PXBXXNCO'

stripe.api_key = secret_key

amo=10

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "Abjx_oMTqkDGT9SeDpbPVzdiEYjXRdLvNkFCODEAbvOB-ak-r_6ar7rvS7ot2qndRFb7Y32dvO-ij5Oi",
  "client_secret": "EGbvrL0I2zwWkpLdcLNXPWi2jC5Y3PzoLUG85aIeFj69V_bwiuRP7yOFwm9oNh6VnToEj7znU12Tdjfw" })

@app.route('/payHome')
def index():
    return render_template('index.html', pub_key=pub_key,acc=request.args.get('email'))


@app.route('/thanks')
def thanks():
    return render_template('thanks.html',acc=request.args.get('email'))

@app.route('/pay', methods=['POST'])
def pay():
    
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amo*1000,
        currency='usd',
        description='The Product'
    )

    return redirect(url_for('thanks'))


@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "10.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return render_template('thanks.html') #jsonify({'success' : success})


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True,host='0.0.0.0')
