#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time, datetime 
import threading
from tkinter import messagebox
from roomGrab import RoomMonitor
import tkinter as tk          # 导入 Tkinter 库
# 创建窗体
from tkinter import ttk
from infoData import InfoData
import os,sys
import downLoadVideo
from ffmpy3 import FFmpeg

window = tk.Tk()
window.title('口袋房间数据')
window.geometry('800x600')


roomID = ""
account = ""
password = ""
#数据数组
videoList = []
lastTime = 0


# 标签
house_label = tk.Label(window, text='房间号')
house_label.place(x=0, y=0, height=40, width=100)

# 房间选择
house_CurrentSelect = tk.StringVar()
house_selectBox = ttk.Combobox(window, textvariable=house_CurrentSelect)
house_selectBox['values'] = InfoData.house_Arr    # 设置下拉列表的值
house_selectBox.grid(column=1, row=1)      # 设置其在界面中出现的位置 column代表列 row 代表行
house_selectBox.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
house_selectBox.place(x=100, y=10, height=25, width=200)

# 手机号
phone_label = tk.Label(window, text='手机号')
phone_label.place(x=0, y=40, height=40, width=100)
# 手机输入框
phone_entry = tk.Entry(window)
phone_entry.width = 200
phone_entry.place(x=100, y=45, height=30)

# 密码
password_label = tk.Label(window, text='密码')
password_label.place(x=0, y=80, height=40, width=100)
# 密码输入框
password_entry = tk.Entry(window)
password_entry.width = 200
password_entry.place(x=100, y=85, height=30)

# 下载视频
down_label = tk.Label(window, text='视频编号:')
down_label.place(x=350, y=0, height=40, width=100)

# 视频选择
down_entry = tk.Entry(window)
down_entry.width = 200
down_entry.place(x=450, y=10, height=30)


#错误提示
scrollbar = tk.Scrollbar(window)
scrollbar.place(x=780, y=180, height=340)
listbox = tk.Listbox(window, yscrollcommand=scrollbar.set)
listbox.insert(tk.END, "信息提示:单次时间跨度不宜过长,根据小偶像房间频率而定.")
listbox.place(x=10, y=180, height=410, width=770)
scrollbar.config(command=listbox.yview)

#下载提示
downscrollbar = tk.Scrollbar(window)
downscrollbar.place(x=650, y=120, height=120)
downlistbox = tk.Listbox(window, yscrollcommand=downscrollbar.set)
downlistbox.insert(tk.END, "下载提示")
downlistbox.place(x=350, y=40 , height=120, width=300)
downscrollbar.config(command=downlistbox.yview)


def timeHanld(timeString):
    # 转为时间数组
    timeArray = time.strptime(timeString, "%Y-%m-%d")   
    # timeArray可以调用tm_year等
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))
    return int(round(timeStamp * 1000))

#回调函数
def callback(message,arr = []):
    listbox.insert(tk.END, message)
    listbox.see(tk.END)
    if len(arr) > 0:
        for dic in arr:
            messageString = ""
            try:
                messageString = "视频位置: " + str(len(videoList)) + "  " + dic["time"] + " " + dic["title"] + " " + "url: "  + dic["url"]
                listbox.insert(tk.END, messageString)
                listbox.see(tk.END)
            except:
                messageString = "视频位置: " + str(len(videoList)) + "  " + dic["time"] + " " + "url: " + dic["url"]
                listbox.insert(tk.END, messageString)
                listbox.see(tk.END)
            videoList.append(dic)
            
            
            



#子进程


def click_StartButton():
    listbox.see(tk.END)
    #房间号
    roomID_arr = house_CurrentSelect.get().split(" = ")
    if len(roomID_arr) < 2:
        listbox.insert(tk.END,"错误\n请选择正确的房间号")
        return
    roomID = roomID_arr[1]
    #手机号
    account = phone_entry.get()
    if len(account) < 11:
        listbox.insert(tk.END,"错误\n请选择正确的手机号")
        return
    # 密码
    password = password_entry.get()
    if len(password) < 6:
        listbox.insert(tk.END,"错误\n请选择正确的密码")
        return

    def worker(interval):
        print("子进程")
        room = RoomMonitor(roomID,callback,lastTime,account,password)
        room.run() 
    p = threading.Thread(target = worker, args = (3,))
    p.start()
    #启动
    listbox.insert(tk.END, "数据获取中....")






start_Button = tk.Button(window,text = '登陆',command = click_StartButton,bg = "blue",font = 20)
start_Button.place(x = 60, y = 130,height = 40,width = 100)

def click_NextButton():
    listbox.see(tk.END)
    #房间号
    roomID_arr = house_CurrentSelect.get().split(" = ")
    if len(roomID_arr) < 2:
        listbox.insert(tk.END,"错误\n请选择正确的房间号")
        return
    roomID = roomID_arr[1]
    #手机号
    account = phone_entry.get()
    if len(account) < 11:
        listbox.insert(tk.END,"错误\n请选择正确的手机号")
        return
    # 密码
    password = password_entry.get()
    if len(password) < 6:
        listbox.insert(tk.END,"错误\n请选择正确的密码")
        return

    def worker(interval):
        print("子进程")
        lastTime = 0
        if len(videoList) == 0:
            lastTime = 0
        else:
            lastTime = (videoList[len(videoList)-1]["lastTime"] - 1 )*1000
        room = RoomMonitor(roomID,callback,lastTime,account,password)
        room.run() 

    p = threading.Thread(target = worker, args = (3,))
    p.start()
    #启动
    listbox.insert(tk.END, "数据获取中....")

next_button = tk.Button(window,text = '下一页',command = click_NextButton,bg = "blue",font = 20) 
next_button.place(x = 180, y = 130,height = 40,width = 100)


def click_DownButton():
    #根据视频编号下载视频
     #手机号
    video_number = int(down_entry.get())

    if video_number < 0:
        downlistbox.insert(tk.END, "错误\n请选择正确编号")
        return
    if video_number >= len(videoList):
        downlistbox.insert(tk.END, "错误\n请选择正确编号")
        return
        #获得.py所在的文件夹的绝对路径
    dic = videoList[video_number]
    url = dic['url']
    if 'xiaoka.tv' in url:
        downlistbox.insert(tk.END, 'xiaoka.tv 视频')
    elif 'http://cychengyuan-vod.48.cn' in url:
        url = url.replace('http://','https://')
    else:
        downlistbox.insert(tk.END, "url错误 下载失败")
        return
    name = dic['title'] + '_' + dic['time']
    py_file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = py_file_path+'/'+ name + '.mp4'
    ff = FFmpeg(
        inputs={
            url: None},
        outputs={file_path: '-c copy -bsf:a aac_adtstoasc'}
        )
    print(ff.cmd)
    try:
        ff.run_async()
        downlistbox.insert(tk.END, "请等待下载完成")
    except:
        downlistbox.insert(tk.END, "ffmpeg错误\n下载失败")
    



down_button = tk.Button(window,text = '下载',command = click_DownButton,bg = "blue",font = 20) 
down_button.place(x = 650, y = 0,height = 40,width = 100)


    


window.mainloop()                 # 进入消息循环



