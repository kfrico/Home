# -*- coding: utf-8 -*-
'''
Created on 2011/12/13

@author: KK
'''
import tkinter as tk
import tkinter.messagebox
import http.cookiejar
import urllib.request
import urllib.parse
import re
import threading
import random
import time

tests = []
id_list = []
lock = threading.Condition()
is_status = '啟動'


#設定標頭檔和cookie
cookie_jar = http.cookiejar.CookieJar()
cjhdr  =  urllib.request.HTTPCookieProcessor(cookie_jar)
opener = urllib.request.build_opener(cjhdr)
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#------------------------------
def logins():
    lock.acquire()
    login = login_var.get()
    cookie_jar.clear()#丟棄所有session和cookies
    user = user_var.get()
    password = password_var.get()
    if login == 'L':
        url="https://login.i-part.com.tw/login.php"
        values={
                "f":"/file/file_my.php?",
                "password":password,
                "r":"http://www.i-part.com.tw/index.php",
                "username":user
                }
        datas=urllib.parse.urlencode(values)#轉為url資料傳輸碼
        binary_data = datas.encode('utf-8')
        opener.open(url,binary_data)#登入

    else:
        url = 'https://login.i-part.com.tw/signup.php'   
        seach_data = opener.open(url).read().decode('utf-8','replace')
                
        
        url = re.search("""href\=\"(.*)\".*\"images\/login\_yahoo\.gif\"""", seach_data).group(1)
        seach_data = opener.open(url).read().decode('utf-8','replace')
        
                
        tries = re.search("""name\=\"\.tries\" value\=\"(.*)\"""", seach_data).group(1)
        src = re.search("""name\=\"\.src\" value\=\"(.*)\"""", seach_data).group(1)
        md5 = re.search("""name\=\"\.md5\" value\=\"(.*)\"""", seach_data).group(1)
        hashs = re.search("""name\=\"\.hash\" value\=\"(.*)\"""", seach_data).group(1)
        js = re.search("""name\=\"\.js\" value\=\"(.*)\"""", seach_data).group(1)
        last = re.search("""name\=\"\.last\" value\=\"(.*)\"""", seach_data).group(1)
        promo = re.search("""name\=\"promo\" value\=\"(.*)\"""", seach_data).group(1)
        intl = re.search("""name\=\"\.intl\" value\=\"(.*)\"""", seach_data).group(1)
        lang = re.search("""name\=\"\.lang\" value\=\"(.*)\"""", seach_data).group(1)
        bypass = re.search("""name\=\"\.bypass\" value\=\"(.*)\"""", seach_data).group(1)
        partner = re.search("""name\=\"\.partner\" value\=\"(.*)\"""", seach_data).group(1)
        u = re.search("""name\=\"\.u\" value\=\"(.*)\"""", seach_data).group(1)
        v = re.search("""name\=\"\.v\" value\=\"(.*)\"""", seach_data).group(1)
        challenge = re.search("""name\=\"\.challenge\" value\=\"(.*)\"""", seach_data).group(1)
        yplus = re.search("""name\=\"\.yplus\" value\=\"(.*)\"""", seach_data).group(1)
        emailCode = re.search("""name\=\".emailCode\" value\=\"(.*)\"""", seach_data).group(1)
        pkg = re.search("""name\=\"pkg\" value\=\"(.*)\"""", seach_data).group(1)
        stepid = re.search("""name\=\"stepid\" value\=\"(.*)\"""", seach_data).group(1)
        ev = re.search("""name\=\"\.ev\" value\=\"(.*)\"""", seach_data).group(1)
        hasMsgr = re.search("""name\=\"hasMsgr\" value\=\"(.*)\"""", seach_data).group(1)
        chkP = re.search("""name\=\"\.chkP\" value\=\"(.*)\"""", seach_data).group(1)
        done = re.search("""name\=\"\.done\" value\=\"(.*)\"""", seach_data).group(1)
        pd = re.search("""name\=\"\.pd\" value\=\"(.*)\"""", seach_data).group(1)
        ws = re.search("""name\=\"\.ws\".*value\=\"(.*)\"""", seach_data).group(1)
        cp = re.search("""name\=\"\.cp\".*value\=\"(.*)\"""", seach_data).group(1)
        pad = re.search("""name\=\"pad\".*value\=\"(.*)\"""", seach_data).group(1)
        aad = re.search("""name\=\"aad\".*value\=\"(.*)\"""", seach_data).group(1)
        persistent = re.search("""name\=\'\.persistent\'.*value\=\'(.*)\'""", seach_data).group(1)       
            
        url="https://login.yahoo.com/config/login"
        values={
                ".bypass":bypass,    
                ".challenge":challenge,
                ".chkP":chkP,
                ".cp":cp,
                ".done":done,
                ".emailCode":emailCode,    
                ".ev":ev,    
                ".hash":hashs,    
                ".intl":intl,
                ".js":js,
                ".lang":lang,
                ".last":last, 
                ".md5":md5,     
                ".partner":partner, 
                ".pd":pd,
                ".persistent":persistent,            
                ".save":"",            
                ".src":src, 
                ".tries":tries,
                ".u":u,
                ".v":v,
                ".ws":ws,
                ".yplus":yplus,  
                "aad":aad,
                "hasMsgr":hasMsgr,
                "login":user,
                "pad":pad,
                "passwd":password,          
                "passwd_raw":"",              
                "pkg":pkg,
                "promo":promo, 
                "stepid":stepid  
                }
         
        datas=urllib.parse.urlencode(values)#轉為url資料傳輸碼
        binary_data = datas.encode('utf-8')
        seach_data = opener.open(url,binary_data).read().decode('utf-8','replace')#登入
        
        re_href = re.search("""Please\s\<a\shref\=\"(.*)\"""", seach_data)
        if re_href:
            re_href = re_href.group(1)  
            opener.open(re_href)#登入



    user_cookie = cookie_check()
    if user_cookie:
        msg_var.set('登入成功')
        submit.config(state = tk.NORMAL)
    else:
        msg_var.set('登入失敗')
    lock.release()#釋放鎖
#------------------------------
def cookie_check():
    cookies = dict([(cookie.name, cookie.value) for cookie in cookie_jar])
    if 'SID' in  cookies.keys():
        return cookies['SID']
    else:
        return False
def online_check(people_id):
    people_id
    seach_data = opener.open("http://www.i-part.com.tw/file/file_viewfile.php?u=" + people_id).read().decode('utf-8','replace')
    if re.search('offline.gif', seach_data):
        return True
    else:
        return False
#------------------------------
def seach():
    submit.config(state = tk.DISABLED)
    submit_stop.config(state = tk.NORMAL)
    post.config(state = tk.DISABLED)
    msg_posting.config(text=str('正在讀取中...'))
    city_vars = citys[citymenu.get()]
    sex_vars = sex_var.get()
    age1_vars = age1_var.get()
    age2_vars = age2_var.get()  


    seach_val={
            "Submit2":"立即尋找",
            "s_age[0]":age1_vars,
            "s_age[1]":age2_vars,
            "s_country":"1",
            "s_couple":"0",
            "s_from":city_vars,
            "s_height[]":"",
            "s_height[]":"",
            "s_photo":"1",
            "s_sex":sex_vars,
            "s_weight[]":"",
            "s_weight[]":"",
            "s_zone":"",
            "type":"simple"
            }
    seach_url = urllib.parse.urlencode(seach_val)
    seach_binary = seach_url.encode('utf-8')
    seach_data = opener.open("http://www.i-part.com.tw/search/query_fast.php",seach_binary).read().decode('utf-8','replace')
    id_data = re.findall("""viewfile\.php\?u\=([0-9][0-9][0-9]*?)\"""", seach_data)
    
    id_list_sorted = list(set(id_data))#把第一次搜尋到的資料做list消除重複
    id_list_sorted.sort(key=id_data.index)#list做排序
    
    pCount = re.search("""name\=\"pCount\" value\=\"([0-9]*?)\"""", seach_data).group(1)
    #幾筆資料
    rows = re.search("""name\=\"rows\" value\=\"([0-9]*?)\"""", seach_data).group(1)
        
    #總共有幾頁
    page = int(rows)//18
    #把頁數設定給msgpage_var
    msgpage_var.set("總頁數:"+str(page+1))
    #讀取people名單

    global id_list#設全預變數
    id_list.extend(id_list_sorted)#把第一次搜查資料加入id_list裡
    
    global is_status
    is_status = '啟動'#狀態設為啟動
    thread1 = threading.Thread(target=postmsg)
    thread1.start()
    thread2 = threading.Thread(target=stop)
    thread2.start()
    for page in range(1,page+1): 
        seachs_val={
                "pCount":pCount,
                "page": page,
                "rows":rows,
                "user_age[0]":age1_vars,
                "user_age[1]":age2_vars,
                "user_couple":"0",
                "user_from":city_vars,
                "user_height[]":"",    
                "user_height[]":"",    
                "user_photo":"1",
                "user_sex":sex_vars,
                "user_weight[]":"",    
                "user_weight[]":"",    
                "user_zone":""    
                }
        seach_url = urllib.parse.urlencode(seachs_val)
        seach_binary = seach_url.encode('utf-8')
        seach_data = opener.open("http://www.i-part.com.tw/search/query_advanced.php",seach_binary).read().decode('utf-8','replace')
        id_datas = re.findall("""viewfile\.php\?u\=([0-9][0-9][0-9]*?)\"""", seach_data)      
        id_list_sorted = list(set(id_datas))
        id_list_sorted.sort(key=id_datas.index)   
        id_list.extend(id_list_sorted)


#--------------------------------------------------
def postmsg():
    global lock
    global is_status
    global postmsgs
    global online_is
    global id_list
    online_is = online_var.get()
    postmsgs = post.get("1.0",tk.END)
    postmsgs = postmsgs.encode('utf-8') 
    
    lock.acquire()
    while len(id_list) > 0:
        people_list = read_depots("people.txt")
        if is_status == '暫停':  
            lock.wait()
        if  is_status == '啟動':
            lock.notify()           
        if len(id_list) > 0:
            if id_list[0] in people_list:
                msg_posting.config(text=str('重複名單' + id_list.pop(0)))
                time.sleep(0.2)
            else:
                people_id = id_list.pop(0)
                if online_is and online_check(people_id):
                    msg_posting.config(text=str('不在線上' + people_id))
                    time.sleep(0.2)
                else:           
                    url="http://www.i-part.com.tw/guestbook/guestbook.php?u="+people_id
                    seach_data = opener.open(url).read().decode('utf-8','replace')#登入


                    PostType = re.search("""\'PostType\'\:(.*)\,""", seach_data)
                    if PostType:
                        PostType = PostType.group(1)
                        
                    key = re.search("""key\:\'(.*)\'""", seach_data)
                    if key:
                        key = key.group(1)
                        
                    msg_type = re.search("""\'msg_type\'\:([0-9]*)\,""", seach_data)
                    if msg_type:
                        msg_type = msg_type.group(1)
                    else:
                        msg_type = re.search("""id\=\"no_use_stamp\".*value\=\"([0-9]*)\"""", seach_data)
                        if msg_type:
                            msg_type = msg_type.group(1)
                        
                    times = re.search("""time\:(.*)\,""", seach_data)
                    if times:
                        times = times.group(1)

                    #print(people_id,PostType,key,msg_type,times)

                    if people_id and PostType and key and msg_type and times:
                        url="http://www.i-part.com.tw/guestbook/ajax_post.php?act=postMsg"
                        values={
                                "PostType":PostType,
                                "key":key,
                                "msg_type":msg_type,
                                "text":postmsgs,
                                "time":times,
                                "u":people_id,
                                }
                        datas=urllib.parse.urlencode(values)#轉為url資料傳輸碼
                        binary_data = datas.encode('utf-8')
                        response = opener.open(url,binary_data).read().decode('utf-8','replace')
                        #print(response)
                        if response != '-992':
                            peoplefile = open("people.txt", "a")
                            peoplefile.write(people_id+"\n")
                            peoplefile.close()
                            msg_posting.config(text=str(people_id +'留言成功'))
                            sec = random.randint(10,15)#隨機秒數
                        else:
                            peoplefile = open("error.txt", "a")    
                            peoplefile.write(people_id+"\n")
                            peoplefile.close()    
                            msg_posting.config(text=str(people_id + '留言失敗'))
                            sec = random.randint(1,1)#隨機秒數                   
                    else:
                        peoplefile = open("error.txt", "a")    
                        peoplefile.write(people_id+"\n")
                        peoplefile.close()    
                        msg_posting.config(text=str(people_id + '留言失敗'))
                        sec = random.randint(1,1)#隨機秒數
                    
                    time.sleep(sec)
       
    else:      
        
        submit.config(state = tk.NORMAL)
        submit_stop.config(state = tk.DISABLED)
        post.config(state = tk.NORMAL)#解開
        msg_posting.config(text=str('傳送完成'))
        lock.release()#釋放鎖
        is_status = '結束'#結束留言函式
    
    
#--------------------------------------------------
def thread_seach():
    user_cookie = cookie_check()
    if user_cookie:
        thread = threading.Thread(target=seach)
        thread.start()
    else:
        tkinter.messagebox.showinfo("訊息", "請先登入" )
def thread_logins():
    msg_var.set('登入中...')
    thread = threading.Thread(target=logins)
    thread.start()        
def is_status_change():
    global is_status
    global online_is
    global postmsgs
    if is_status == '啟動':#如果是啟動狀態就更改為暫停
        post.config(state = tk.NORMAL)#解開
        is_status = '暫停'
        stop_var.set('繼續')#按鈕文字
        msg_posting.config(text=str('暫停中...'))
        
    elif is_status == '暫停':#如果是暫停狀態就更改為啟動
        post.config(state = tk.DISABLED)#鎖起來
        online_is = online_var.get()
        postmsgs = post.get("1.0",tk.END)
        postmsgs = postmsgs.encode('utf-8')   
        is_status = '啟動'
        stop_var.set('暫停')#按鈕文字
        msg_posting.config(text=str('讀取資料中...'))
    
def stop():
    global is_status
    global lock
    lock.acquire()
    while is_status != '結束':#如果不是結束狀態一直跑
        if is_status == '啟動':#如果是啟動狀態就凍結此線程
            lock.wait()
        if is_status == '暫停':#如果是暫停狀態就啟動此線程
            time.sleep(5)
            lock.notify()
    lock.release()#釋放鎖

#----------------------------------------
def read_depots(file): 
    depots = [] 
    depots_f = open(file)
    for line in depots_f:
        depots.append(line.rstrip()) 
    return depots 

#----------------------------------------
    
    
app = tk.Tk()
app.title("愛情公寓自動留言")
app.geometry('420x390+50+500')
app.resizable(width = False, height = False)#不讓它任意拉框

global_font=("Arial",11)

#選擇登入變數
login_var = tk.StringVar()
login_var.set("L")

user_var = tk.StringVar()
user_var.set("")
password_var = tk.StringVar()
password_var.set("")

msg_var = tk.StringVar()
msg_var.set("")


#年齡變數
age1_var = tk.IntVar()
age1_var.set(18)
age2_var = tk.IntVar()

#城市變數(預設台中)
citymenu = tk.StringVar() 
citymenu.set("台中市") 

#性別變數
sex_var = tk.StringVar()
sex_var.set("M")

#選擇上線才傳
online_var = tk.IntVar()

#下方訊息
msgposting_var = tk.StringVar()
msgposting_var.set("")

#搜尋資料的頁數-變數
msgpage_var = tk.StringVar()
msgpage_var.set("總頁數:")

stop_var = tk.StringVar()
stop_var.set('暫停')

#----------------------------------------------
#選擇登入方式
login_lab = tk.Label(app, font=global_font, text="選擇登入方式:").place( height=30,x=10,y=10)
login_lh = tk.Radiobutton(app, text="愛情公寓(預設)", font=global_font, variable=login_var, value="L").place( height=30,x=120,y=10)
login_yahoo = tk.Radiobutton(app, text="YAHOO", font=global_font, variable=login_var, value="Y").place( height=30,x=260,y=10)



#帳號欄位
user_lab = tk.Label(app, font=global_font, text="帳號:").place( height=30,x=10,y=50)
user=tk.Entry( app, font=global_font, width=10, textvariable = user_var).place( height=20,x=50,y=55)


#密碼欄位
password_lab = tk.Label(app, font=global_font, text="密碼:").place( height=30,x=130,y=50)
password=tk.Entry( app, font=global_font, width=10, show='*', textvariable = password_var).place( height=20,x=170,y=55)


#登入按鈕
login_button = tk.Button(app, font=global_font, text = "登入", command = thread_logins)
login_button.place( height=30,x=360,y=10)

#顯示訊息
msg = tk.Label(app, font=global_font, textvariable = msg_var).place( height=30,x=270,y=50)

#--------------------
#年齡1
tk.Label( app, font=global_font, text="年齡:").place( height=30,x=10,y=90)
tk.Entry( app, font=global_font, width=2, textvariable = age1_var).place( height=20,x=50,y=95)


#年齡2
tk.Label(app, font=global_font, text="~").place( height=30,x=70,y=90)
tk.Entry( app, font=global_font, width=2, textvariable = age2_var).place( height=20,x=85,y=95)

#city_menu
city_id = read_depots("city_id.txt") 
city = read_depots("city.txt")
citys = dict(zip(city,city_id))
tk.OptionMenu(app, citymenu, *city).place( height=30,x=110,y=90)


sex1 = tk.Radiobutton(app, text="男", font=global_font, variable=sex_var, value="M").place( height=30,x=200,y=90)
sex2 = tk.Radiobutton(app, text="女", font=global_font, variable=sex_var, value="F").place( height=30,x=240,y=90)


online_check_box = tk.Checkbutton(app, text = "上線才傳", font=global_font, variable = online_var, onvalue = 1, offvalue = 0).place( height=30,x=300,y=90)

#-----------------------------------------
#text訊息框
post = tk.Text(app, font=global_font,height=10)
post.place(width=400, height=200,x=10,y=140)
#-----------------------------------------
#下方顯示訊息
msg_posting = tk.Label(app, font=global_font)
msg_posting.place(height=30,x=10,y=350)
#下方顯示訊息
msg_page = tk.Label(app, font=global_font, textvariable = msgpage_var)
msg_page.place(height=30,x=200,y=350)

#送出按紐
submit = tk.Button(app, font=global_font,state=tk.DISABLED, text = "送出", command = thread_seach)
submit.place( height=30,x=360,y=350)

#暫停按紐
submit_stop = tk.Button(app, font=global_font, state=tk.DISABLED,textvariable = stop_var, command = is_status_change)
submit_stop.place( height=30,x=300,y=350)



#------------------------------------------
app.mainloop()
