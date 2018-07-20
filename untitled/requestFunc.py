import requests
def RequestFunc(request_url,request_type,request_header,datatype,request_data):
    if(len(request_header)<=0):
            request_header={}
    else:
            request_header = eval(request_header)

    if(request_type=="POST"):
            print("post")
            if(datatype=="applicationjson"):
                print("request_data",request_data)
                request_data=eval(request_data)
                print("request_datatype",type(request_data))
                send=requests.post(url=request_url,headers=request_header,json=request_data).json()
                print(send)
            if(datatype!="applicationjson"):
                request_data=eval(request_data)
                send=requests.post(url=request_url,headers=request_header,data=request_data).json()
                print(send)

    if (request_type == "GET"):
            send = requests.get(url=request_url, headers=request_header).json()
            print(send)