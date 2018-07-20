from flask import Flask,render_template,request,jsonify,session,redirect,url_for
from flask_bootstrap import Bootstrap
import json
import requests
from db import  db
import time
import config
from model import User,RequestList,TaskList
import random
from flask_httpauth import HTTPBasicAuth
from flask_apscheduler import APScheduler
from task import taskserach,task,addtask
from requestFunc import RequestFunc
from os import path
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.config.from_object(config)
bootstrap = Bootstrap(app)
db.init_app(app)
auth = HTTPBasicAuth()
scheduler = APScheduler()
scheduler.init_app(app)



def task1(request_url,request_type,request_header,datatype,request_data):
    if (request_type == "POST"):
        if (datatype == "applicationjson"):
            request_data = eval(request_data)
            send = requests.post(url=request_url, headers=request_header, json=request_data).json()
            print(send)
        if (datatype != "applicationjson"):
            request_data = eval(request_data)
            send = requests.post(url=request_url, headers=request_header, data=request_data).json()
            print(send)

    if (request_type == "GET"):
        send = requests.get(url=request_url, headers=request_header).json()
        print(send)
    # return send
    print("定时启动了",request_url)



@app.route('/login')
def login():
    if session.get("username"):
        return render_template("ota.html")
    else:
        return  render_template("login.html")



@app.route('/logincommit',methods=["POST"])
def logincommit():
    data=request.form.get("data")
    print(data)
    data=json.loads(data)
    usrename=data.get("username")
    password=data.get("password")
    print("1111")
    user=User.query.filter(User.username ==usrename).first()
    print(user)

    if user==None :
        return ("4000")
    # if user!=None and user.password!=password:
    #     return ("5000")
    else:
        session['username']=user.username
        session['password']=user.password
        return ("2000")


@app.route('/ota')
def ota():
   # if session.get("username"):
        return render_template("ota.html",user=session.get("username"),password=session.get("password"))

   # else:
   #     return redirect(url_for("login"))


@app.route('/register')
def register():
    return  render_template("register.html")

@app.route('/registercommit')
def registercommit():
    print("user:",request.args.get("user"))
    print("password:",request.args.get("password"))
    if request.args.get("user")=="":
        return render_template("register.html", respones="用户名不能为空")
    if request.args.get("password")=="":
        return render_template("register.html", respones="密码不能为空")
    if request.args.get("passcommfit")=="":
        return render_template("register.html", respones="确认不能为空")
    if request.args.get("password")!="" and request.args.get("passcommfit")!="" and request.args.get("passcommfit")!=request.args.get("password"):
        return render_template("register.html", respones="二次输入的密码不一致")
    else:
        user = User.query.filter(User.username == request.args.get("user")).first()
        print(user)
        if user!=None:
            return render_template("register.html", respones="用户名已存在")
        else:
            # try:
                UserRegister=User(password=request.args.get("password"),username=request.args.get("user"))
                print(User)
                db.session.add(UserRegister)
                db.session.commit()
                print("注册成功")
                return render_template("login.html")

            # except Exception as err:
            #     print(err)
            #     db.session.rollback()
            #     print("注册不成功")
            #     return redirect(url_for('register'),302)






@app.route('/POST',methods=["POST"])
def POST():
    data=request.form.get("mallInstitution")
    data=json.loads(data)
    url=data[0]["value"]
    if(data[1]["value"]==""):
        header={}
    else:
        header=eval(data[1]["value"])
    data=eval(data[2]["value"])
    respones=requests.post(url=url,headers=header,json=data).json()
    print(respones)
    # #return (jsonify(jsonj))
    js=respones
    return (jsonify(js))


@app.route('/GET',methods=["GET"])
def GET():
    data=request.form.get("mallInstitution")
    data=json.loads(data)
    print(data[0]["value"])
    jsonj=[{"name":"login","value":"autoline@126.com"},{"name":"password","value":"123456"}]
    #return (jsonify(jsonj))
    print(session.get("user"))
    return render_template("yyyt.html",session=session.get("user"))

@app.route("/newota")
def newota():
    return render_template("newota.html")
# @app.before_request
# def before_request():
#     print("ceshi1")


@app.route("/otalist")
def otalist():
    requestList = RequestList.query.all()
    res=[]
    for request in requestList:
        request_status=request.request_status
        tasktime=request.tasktime
        url=request.request_url
        type=request.request_type
        header=request.request_header
        requestdatatype=request.datatype
        requestdata=request.request_data

        dd={"request_url":url,"request_type":type,"request_header":header,"datatype":requestdatatype,"request_data":requestdata,"times":tasktime,"status":request_status}
        res.append(dd)
    print(res)

    return render_template("otalist.html",res=res)


@app.route("/getotalist",methods=["POST"])
def getotalist():

    # print(request.headers)
    # ip = request.remote_addr
    # print(ip)
    # print("返回结束格式：",request.accept_mimetypes)
    data=request.form.get("data")
    data=json.loads(data)
    print(data)
    url=data[0]
    if(len(data)<4):
        request_type="GET"
    else:
        request_type="POST"
        request_data=str(data[2][1])
        datatype=data[2][0]["type"]
    header=data[1]
    if (len(header)!=0):
        header=str(header)
    else:
        header=""
    print("URLTYPE:",type(url))
    print("headerTYPE:",type(header))
    print("request_typeTYPE:",type(request_type))
    print("request_dataTYPE:",type(request_data))
    print("datatypeTYPE:",type(datatype))
    Task_status=data[3]["Task_status"]
    tasktime=data[3]["tasktime"]
    print(Task_status)
    print(tasktime)
    try:
        requestList=RequestList(request_url=url,request_type=request_type,request_header=header,datatype=datatype,request_data=request_data,request_status=Task_status,tasktime=tasktime)
        db.session.add(requestList)
        db.session.commit()
        print("提交成功")
    except BaseException as e:
        db.session.rollback()
        print("提交失败:",e)


    time.sleep(2)
    print(request.referrer)
    res={"123":random.randint(1,10) }
    return ("1"),201,{'Content-Type': 'text',"tpew":"123"}

@app.route("/ceshi",methods=["POST"])
def ceshi():
    time.sleep(2)
    return ("2")


@app.route("/test/<id>",methods=["GET"])
def test(id):
    print(id)
    return ("2")


users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]

@auth.get_password
def get_password(username):
    for user in users:
        if user['username'] == username:
            return user['password']
    return None


@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

@app.route('/testtest')
def testtest():
    return render_template("test.html")

@app.route("/TaskStart",methods=["POST"])
def TaskStart():
    try:
        data=request.form.get("data")
        data=json.loads(data)
        print(data)
        request_url=data[0]
        request_type=data[1]
        request_header=data[2]
        datatype=data[3]
        request_data=data[4]
        tasktime=data[6]
        request_id,rq=taskserach(request_url,request_type,request_header,datatype,request_data)
        # with app.app_context():  ###查询数据库必须加上App里面的appcontext()###
        #     rq = RequestList.query.filter(RequestList.id==1).first()
        #     request_url = rq.request_url
        #     request_type = rq.request_type
        #     request_header = rq.request_header
        #     datatype = rq.datatype
        #     request_data = rq.request_data
        #     request_header = eval(request_header)
        scheduler.add_job(func=RequestFunc, id="1", args=(request_url, request_type, request_header, datatype, request_data), trigger='interval', seconds=10, replace_existing=True)
        scheduler.start()
        add_task=addtask(request_id)
        db.session.add(add_task)
        rq.request_status="已启动"
        db.session.commit()
        return("任务启动成功")
    except BaseException as  e:
        print("任务启动失败：",e)
        return("任务启动失败")






if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0',port=5000,debug=True))
