import requests,time,random,json,re,os,sys
#成员房间号可在这里查询：https://github.com/chinshin/CQBot_hzx/blob/master/roomID.conf
#时间戳可在这里转换：http://tool.chinaz.com/Tools/unixtime.aspx

class RoomMonitor():
	def __init__(self,roomID,func,lastTime,account = None,password = None):
		self.log = func
		self.roomID = roomID
		self.memberID = None
		self.account = account
		self.password = password
		self.lastTime = lastTime
		self.loginUrl = 'https://puser.48.cn/usersystem/api/user/v1/login/phone'
		self.liveMonitorUrl = 'https://plive.48.cn/livesystem/api/live/v1/memberLivePage'
		self.ErrorLogPath = "c:\\coolQ\\coolQlog\\Error.dat"
		self.reLoginFlag = True
		self.token = self.login()
		string = "{}登陆完毕\ntoken:{}".format(account,self.token)
		self.log(string)
		print(string)
		self.videoList = []
		#获得.py所在的文件夹的绝对路径
		py_file_path = os.path.dirname(os.path.abspath(__file__))
		self.filePath = py_file_path
		self.log(self.filePath)

		self.emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)
	
	def textProcess(self,text):
		if text == None:
			return None
		else:
			text = self.emoji_pattern.sub(r'',text)
			text = text.replace("\n","")
			text = text.replace("\r","")
			return self.emoji_pattern.sub(r'',text)
	
	def login(self):
		s = requests.Session()
		headers = {
				'os':'android',
				'User-Agent':'Mobile_Pocket',
				'IMEI':'863526430568945',
				'token':'0',
				'version':'5.3.0',
				'Content-Type':'application/json;charset=utf-8',
				'Host':'puser.48.cn',
				'Connection':'Keep-Alive',
				'Accept-Encoding':'gzip',
				'Cache-Control':'no-cache'
			}
		s.headers = headers
		params = {"latitude":'0',"longitude":'0',"account":self.account,'password':self.password}
		p = json.dumps(params)
		#while True:
			#try:
		a = s.post(self.loginUrl,data = p,timeout = (5,10))
		#if a.status_code == 200:
		b = a.content.decode("utf-8")
		r = json.loads(b)
		token = r["content"]["token"]
		reLoginFlag = False
		return token
				#else:
					#a = 1/0
			#except:
				#self.log("口袋48登陆失败，冷却中")
				#time.sleep(10)

	def timeHandle(self,timeSiring):
		timeArray = time.localtime(int(timeSiring/1000))
		otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
		return otherStyleTime
	
	#获取视频列表#
	def getLiveList(self):
		headers = {"Content-type": "application/json; charset=utf-8","version":'5.0.1',"os":"android",
               "token":self.token}
		params = {"lastTime":self.lastTime,"groupId":0,"type":1,"memberId":self.roomID,"limit":20,"giftUpdTime":0}
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
				messageDic = {"title":subTitle,"time":messageTime,"url":streamPath,"lastTime":startTime}
				self.videoList.append(messageDic)
				# try:
				# 	#标题有可能是特殊符号 不兼容 醉了
				# 	messageString = "视频位置: " + str(len(self.videoList))+ "    " + messageTime + " " + subTitle 
				# 	self.log(self.textProcess(messageString))
				# except:
				# 	messageString = "视频位置: " + str(len(self.videoList))+ "    " + messageTime + " "
				# 	self.log(self.textProcess(messageString))
				# self.log(streamPath)
				messageString = ""
		self.log("本次结束",self.videoList)

	def run(self):
		self.getLiveList()