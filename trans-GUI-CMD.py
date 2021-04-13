#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter.messagebox
import tkinter.ttk
from tkinter.filedialog import askdirectory
from tkinter import *
import time,os,sys
import subprocess
import ffmpeg

LOG_LINE_NUM = 0
w_dir = ".."
prefix = "file"
tou_c = 1
wei_c = 0
xuzhuan = {'左旋90°'   : ' -vf transpose=1 ',
           '右旋90°'   : ' -vf transpose=2 ',
           '上下翻转'  : ' -vf vflip ',
           '左右翻转'  : ' -vf hflip '}

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
    #设置窗口
    def set_init_window(self):
        #文件头
        self.init_window_name.title("转码工具_v1.2")           #窗口名                        
        self.init_window_name.geometry('1280x720+100+160')  #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_qiatou_s_label = Label(self.init_window_name, text="秒(s)",bg="pink",font=("微软雅黑", 15))
        self.init_quwei_s_label = Label(self.init_window_name, text="秒(s)",bg="pink",font=("微软雅黑", 15))
        self.init_malv_s_label = Label(self.init_window_name, text="bps ",bg="pink",font=("微软雅黑", 15))
        
        self.init_qiatou_label = Label(self.init_window_name, text="片头截取：",bg="pink",font=("微软雅黑", 15))
        self.init_quwei_label = Label(self.init_window_name, text="片尾截取：",bg="pink",font=("微软雅黑", 15))

        self.init_qiatou_label_1 = Label(self.init_window_name, text="截取时间：",bg="pink",font=("微软雅黑", 15))
        self.init_quwei_label_1 = Label(self.init_window_name, text="截取时间：",bg="pink",font=("微软雅黑", 15))
        
        self.init_rename_label = Label(self.init_window_name, text="重命名：",bg="pink",font=("微软雅黑", 15))
        self.init_malv_label = Label(self.init_window_name, text="转码码率：",bg="pink",font=("微软雅黑", 15))
        self.init_xuanzhuan_label = Label(self.init_window_name, text="旋转方向：",bg="pink",font=("微软雅黑", 15))

        #标签布局
        self.init_qiatou_label.place(x=15,y=15,width=110,height=29)
        self.init_quwei_label.place(x=15,y=65,width=110,height=29)
        self.init_rename_label.place(x=15,y=115,width=110,height=29)
        self.init_xuanzhuan_label.place(x=15,y=165,width=110,height=29)

        self.init_qiatou_label_1.place(x=230,y=15,width=110,height=29)
        self.init_quwei_label_1.place(x=230,y=65,width=110,height=29)
        self.init_malv_label.place(x=230,y=115,width=110,height=29)

        self.init_qiatou_s_label.place(x=470,y=15,width=45,height=29)
        self.init_quwei_s_label.place(x=470,y=65,width=45,height=29)
        self.init_malv_s_label.place(x=470,y=115,width=45,height=29)

        #输入框
        self.init_qiatou_entry =  Entry(self.init_window_name,show="",fg='steelblue',font=("微软雅黑", 10))
        self.init_qiatou_entry.place(x=345,y=15,width=110,height=29)

        self.init_quwei_entry =  Entry(self.init_window_name, show="",fg='steelblue',font=("微软雅黑", 10))
        self.init_quwei_entry.place(x=345,y=65,width=110,height=29)

        #下拉菜单
        self.init_qiatou_cmb = tkinter.ttk.Combobox(self.init_window_name,background='lightblue',foreground='blue')   #去片头
        self.init_qiatou_cmb['value'] = ('是','否')
        self.init_qiatou_cmb.current(0)

        self.init_quwei_cmb = tkinter.ttk.Combobox(self.init_window_name,background='lightblue',foreground='blue')   #去片尾 
        self.init_quwei_cmb['value'] = ('是','否')
        self.init_quwei_cmb.current(1)

        self.init_rename_cmb = tkinter.ttk.Combobox(self.init_window_name,background='lightblue',foreground='blue')  #重命名
        self.init_rename_cmb['value'] = ('是','否')
        self.init_rename_cmb.current(1)

        self.init_xuanzhuan_cmb = tkinter.ttk.Combobox(self.init_window_name,background='lightblue',foreground='blue')  #旋转
        self.init_xuanzhuan_cmb['value'] = ('左旋90°','右旋90°','不旋转','上下翻转','左右翻转')
        self.init_xuanzhuan_cmb.current(2)

        self.init_malv_cmb = tkinter.ttk.Combobox(self.init_window_name,background='lightblue',foreground='blue')  #转码
        self.init_malv_cmb['value'] = ('不转码','2000k','1500k','1000k','800k')
        self.init_malv_cmb.current(0)

        self.init_qiatou_cmb.place(x=125,y=15,width=70,height=29)
        self.init_quwei_cmb.place(x=125,y=65,width=70,height=29)
        self.init_rename_cmb.place(x=125,y=115,width=70,height=29)
        self.init_xuanzhuan_cmb.place(x=125,y=165,width=70,height=29)
        self.init_malv_cmb.place(x=345,y=115,width=110,height=29)

        #选择目录文本框
        self.dir_Text = Text(self.init_window_name,font=("微软雅黑", 10))
        self.dir_Text.place(x=75,y=217,width=460,height=29)
        #源文件文本框
        self.init_data_Text = Text(self.init_window_name, font=("微软雅黑", 8))
        self.init_data_Text.place(x=1,y=250,width=535,height=460)
        #修改信息文本框
        self.result_data_Text = Text(self.init_window_name,font=("微软雅黑", 8))  #处理结果展示
        self.result_data_Text.place(x=550,y=35,width=720,height=680)

        #按钮
        self.init_dir_button = Button(self.init_window_name, text="选择目录", bg="lightblue",command=self.selectPath,font=("微软雅黑", 10))
        self.init_dir_button.place(x=3,y=217,width=70,height=29)
        self.rename_file_button = Button(self.init_window_name, text="开始\n转码", bg="lightblue",command=self.exec_ffpneg,font=("微软雅黑", 15))  # 调用内部方法  加()为直接调用
        self.rename_file_button.place(x=475,y=155,width=60,height=60)

    def swarning(self,msg):
            tkinter.messagebox.showwarning('警告',msg)

    def rename(self):
        os.chdir(w_dir)
        file_list = os.listdir(w_dir)
        for file in file_list:
            file2 = re.sub("[\!\%\[\]\,\，\。\ \/\【\】\！\？\_\、\：\/\(\)\（\）\／\』\『\～\《\》\“\”\〖\〗\★]", "", file).upper()
            if file  != file2 :
                os.rename(file,file2)

    #获取视频时长，秒
    def get_lenth(self,file):
        os.chdir(w_dir)
        lent = 0
        cmd = "ffprobe.exe  {}".format(file)
        out,k = subprocess.Popen(args=cmd,cwd=w_dir,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
        for line in out.decode().split("\n") :
            if line.find("Duration") > 0:
                lst = line.split(" ")[3].replace(",","").split(":")
                b=0
                for i in lst :  
                    lent += float(i) * 60 ** (2 - b) 
                    b += 1 
        return int(lent)

    #选择工作目录
    def selectPath(self):
        global w_dir
        w_dir = askdirectory()
        self.init_data_Text.delete(1.0,END)
        self.dir_Text.delete(1.0,END)
        self.dir_Text.insert(END,str(w_dir))
        os.chdir(w_dir)
        for na in os.listdir(w_dir):
            self.init_data_Text.insert(END,'{}/{}\n'.format(w_dir,na))

    #掐头去尾时长
    def  cut_lenth(self,file):
        global tou_c
        global wei_c
        Flag = False
        if self.init_qiatou_cmb.get() == "是" :
            try :
                print(self.init_qiatou_entry.get())
                tou_c = int(self.init_qiatou_entry.get())
            except:
                Flag = True
        else:
            tou_c = 0
             
        if self.init_quwei_cmb.get() == "是" :
            try:
                print(self.init_quwei_entry.get())
                wei_c =  int(self.init_quwei_entry.get())
            except:
                Flag = True
        else:
            wei_c = 0
        return tou_c,wei_c,Flag
    
    #功能函数
    def exec_ffpneg(self):
        os.chdir(w_dir)
        if self.init_quwei_cmb.get() == "是" :
            self.rename()
        if self.init_malv_cmb.get() == "不转码":
            ffmpeg_malv_info = " -vcodec copy -acodec copy "
        else : 
            ffmpeg_malv_info = "  -b:v {} -vcodec h264  -acodec copy  ".format(self.init_malv_cmb.get())
        if self.init_xuanzhuan_cmb.get() == '不旋转' :
            ffmpeg_xuanzhuan_info = " "
        else:
            ffmpeg_xuanzhuan_info =  xuzhuan[self.init_xuanzhuan_cmb.get()]
            ffmpeg_malv_info = " -b:v 1500k -vcodec h264  -acodec copy   "
        self.result_data_Text.delete(1.0,END)
        file_list = os.listdir(w_dir)
        for file in file_list:
            if os.path.isfile(file):                    
                try:
                    #lenth = self.get_lenth(file)
                    lenth = int(float(str(ffmpeg.probe(file)['format']['duration'])))
                    tou,wei,flag = self.cut_lenth(file)
                    if  flag :
                        self.swarning("截取时间请输入数字")
                        self.init_data_Text.insert(END,"请检查各项输入是否正常")
                        break
                    if tou == 0 :
                        tou_info = ""
                    else:
                        tou_info = " -ss {} ".format(tou)
                    if wei == 0:
                        wei_info = ""
                    else:
                        end = lenth - wei - tou
                        if end < 5 :
                            wei_info = ""
                        else:
                            wei_info = " -t {} ".format(end)
                    ffmpeg_time_info = " -r 25 {} {} ".format(tou_info,end_info)
                except : 
                    ffmpeg_time_info = "-r 25 "

                s_file = "odl_" + file
                os.rename(file,s_file)
                cmd = "ffmpeg -i   {} {} {} {} {}.MP4".format(s_file,ffmpeg_time_info,ffmpeg_xuanzhuan_info,ffmpeg_malv_info,file)
                cmdD = subprocess.Popen(args=cmd,cwd=w_dir)
                cmdD.wait()
                c_time = self.get_current_time()
                success_info = "{}    {} \n".format(c_time,cmd)
                self.result_data_Text.insert(END,success_info)

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()


