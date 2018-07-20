import  requests
from model import RequestList,TaskList
def taskserach(request_url,request_type,request_header,datatype,request_data):
    rq=RequestList.query.filter(RequestList.request_url==request_url and RequestList.request_type==request_type and RequestList.request_header==request_header,RequestList.datatype==datatype,RequestList.request_data==request_data ).first()
    print(type(rq.request_url))
    print(type(rq.request_type))
    print(type(rq.request_header))
    print(type(rq.request_data))

    request_url=rq.request_url
    request_type=rq.request_type
    request_header=rq.request_header
    datatype=rq.datatype
    request_data=rq.request_data
    request_id=rq.id
    task_time=rq.tasktime
    return request_id,rq
    # return request_id,request_url,request_type,request_header,datatype,request_data,task_time
    # if(len(request_header)<=0):
    #     request_header={}
    # else:
    #     request_header = eval(request_header)
    # if(request_type=="POST"):
    #     print("post")
    #     if(datatype=="applicationjson"):
    #         print("request_data",request_data)
    #         request_data=eval(request_data)
    #         print("request_datatype",type(request_data))
    #         send=requests.post(url=request_url,headers=request_header,json=request_data).json()
    #         print(send)
    #     if(datatype!="applicationjson"):
    #         request_data=eval(request_data)
    #         send=requests.post(url=request_url,headers=request_header,data=request_data).json()
    #         print(send)
    # if (request_type == "GET"):
    #     send = requests.get(url=request_url, headers=request_header).json()
    #     print(send)
    # #   return send
    # print("请求发送成功")
    # return ("123")


def task(requestsid):
    Task=TaskList.query.filter(TaskList.Request_id==requestsid).first()
    return Task.Request_id

def alltask():
    AllTask=TaskList.query.first()
    return AllTask.Request_id,AllTask.times


def addtask(requestsid):
    task= TaskList(Request_id=requestsid)
    return task



