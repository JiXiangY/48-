
import requests,time,random,json,re,os


#获取视频列表
def getLiveList():
    videoList = []
    headers = {"Content-type": "application/json; charset=utf-8","version":'5.0.1',"os":"android",
               "token":"2/NeDE3TYLYTcw8AO1ImoW0uxadcXOsOwfZqUGuD5VEhC8S6hN7BMR1Yg2xz+PFSOY4eAF9ifbM="}
    params = {}
    if len(.ideoList) == 0:
        params = {"lastTime":0,"groupId":0,"type":1,"memberId":327591,"limit":20,"giftUpdTime":0}
    else:
        lastTime = videoList[-1]["lastTime"] - 1
        params = {"lastTime":lastTime,"groupId":0,"type":1,"memberId":327591,"limit":20,"giftUpdTime":0}
    data = json.dumps(params)
    response = requests.post('https://plive.48.cn/livesystem/api/live/v1/memberLivePage',headers = headers,data=data)
    
    messageString = ""
    if response.status_code != 200:  messageString = '列表获取失败 status != 200'
    if response.status_code != 'OK': messageString = '列表获取失败 reason !=  OK'
    hjson=response.json()

    print(response.text)
    reviewList = hjson['content']['reviewList']
    if reviewList:
        for messageDic in reviewList:
            subTitle = messageDic['subTitle']
            streamPath = messageDic['streamPath'] #视频地址
            startTime = messageDic['startTime']
            startTime = startTime/1000
            timeloa = time.localtime(startTime)
            messageTime = time.strftime("%Y-%m-%d %H:%M:%S", timeloa)
            messageString = messageString + messageTime + "\n" + subTitle + "\n" + streamPath + "\n"
            messageDic = {"title":subTitle,"time":messageTime,"url":streamPath,"lastTime":startTime}
            videoList.append(messageDic)
    

    

getLiveList()