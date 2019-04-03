#!/usr/bin/python
# -*- coding:utf-8 -*-

# splinter爬虫
import requests
from splinter.browser import Browser
from time import sleep
import traceback
import time
from selenium import webdriver
# 邮件
from email.mime.text import MIMEText
import smtplib

class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends,mail_name,mail_pass,smtp_server,to_addr):
        self.username = username
        self.passwd = passwd
        # 车次，范围为自然数
        self.order = order
        # 乘客名
        self.passengers = passengers
        # 起始地和终点
        self.starts = starts
        self.ends = ends
        # 日期
        self.dtime = dtime
        # self.xb = xb
        # self.pz = pz
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
        self.executable_path = r'C:\Users\lzsy\AppData\Local\Google\Chrome\Application\chromedriver.exe'
        # email
        self.mail_name = mail_name #发件邮箱
        self.mail_pass = mail_pass#授权密码
        self.smtp_server = smtp_server # 输入SMTP服务器地址:
        self.port = 25 # SMTP协议默认端口是25
        self.to_addr = to_addr# 输入收件人地址:可为多个，组成列表
    # 登录功能实现
    def login(self):
        waiting = 0
        while waiting == 0 or waiting>60:
            self.b.visit(self.login_url)
            self.b.fill('loginUserDTO.user_name', self.username)
            # sleep(1)
            self.b.fill('userDTO.password', self.passwd)
            # sleep(1)
            print('请输入验证码...')
            start = time.clock()
            while True:
                if self.b.url != self.initMy_url:
                    sleep(1)
                    end = time.clock()
                    waiting = end-start
                    if waiting >60:
                        break
                else:
                    break
        
    # 邮件提醒
    def send_mail(self):
        """发送邮件通知"""
        # 发件信息
        msg = MIMEText('抢票成功！', 'plain', 'utf-8')
        msg['From'] = self.mail_name
        msg['To'] = self.to_addr[0]
        msg['Subject'] = '抢票成功通知！'
        # 开始登陆邮箱，并发送邮件
        server = smtplib.SMTP(self.smtp_server,self.port) #确认SMTP端口
        # server.set_debuglevel(1)
        server.login(self.mail_name, self.mail_pass)#登录
        server.sendmail(self.mail_name, self.to_addr, msg.as_string())#发件人姓名，收件人，信件内容
        server.quit()
    # 买票功能实现
    def start_buy(self):
        number = [x for x in range(1,101)]
        self.b = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        #窗口大小的操作
        self.b.driver.set_window_size(700, 500)
        self.login()
        self.b.visit(self.ticket_url)
        sleep(1)
        try:
            print('开始购票...')
            # 加载查询信息
            self.b.cookies.add({"_jc_save_fromStation": self.starts})
            self.b.cookies.add({"_jc_save_toStation": self.ends})
            self.b.cookies.add({"_jc_save_fromDate": self.dtime})
            self.b.reload()
            self.b.find_by_text('GC-高铁/城际').click()
            count = 0
            if self.order in number:
                while self.b.url == self.ticket_url:
                    self.b.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    now = time.strftime("%H:%M:%S")[0:5]
                    try:
                        if self.b.find_by_xpath('//*[@id="queryLeftTable"]/tr[1]/td')[3].value != '无' or self.b.find_by_xpath('//*[@id="queryLeftTable"]/tr[1]/td')[2].value != '无' and now != '22:59':
                            self.b.find_by_text('预订')[0].click()
                            print('准备预定...')
                            sleep(1)
                        elif self.b.find_by_xpath('//*[@id="queryLeftTable"]/tr[1]/td')[3].value == '无' or self.b.find_by_xpath('//*[@id="queryLeftTable"]/tr[1]/td')[2].value == '无' and now != '22:59':
                            print('暂无一等座二等座')
                            sleep(1)
                            continue
                        elif now == '22:59':
                            print('系统维护，暂停查询')
                            sleep(25320)
                            continue
                        else:
                            print('预定失败..')
                            self.b.reload()
                            self.b.find_by_text('GC-高铁/城际').click()
                            continue
                    except Exception as e:
                        print(e)
                        print('加载中，预定失败')
                        self.b.reload()
                        self.b.find_by_text('GC-高铁/城际').click()
                        continue
            else:
                print('请修改order选择车次,格式为自然数，例如1')
            print('开始预订...')
            sleep(1)
            print('开始选择用户...')
            for p in self.passengers:
                self.b.find_by_text(p).last.click()
                sleep(0.5)
                if p[-1] == ')':
                    self.b.find_by_id('dialog_xsertcj_cancel').click()
            print('提交订单...')
            # sleep(1)
            # self.b.find_by_text(self.pz).click()
            # sleep(1)
            # self.b.find_by_text(self.xb).click()
            # sleep(1)
            self.b.find_by_id('submitOrder_id').click()
            sleep(2)
            print('确认选座...')
            self.b.find_by_id('qr_submit_id').click()
            print('预订成功...')
            self.send_mail()
            print('发送邮件成功')
        except Exception as e:
            print(e)




if __name__ == '__main__':
    # 用户名
    username = 'username'
    # 密码
    password = 'password'
    # 车次选择，[1,2,3,···,n]
    order = 1
    # 乘客名，比如passengers = ['丁小红', '丁小明']
    # 学生票需注明，注明方式为：passengers = ['丁小红(学生)', '丁小明']
    passengers = ['passengers']
    # 日期，格式为：'2018-01-20'
    dtime = 'dtime'
    # 出发地(需填写cookie值)
    starts = 'starts' 
    # 目的地(需填写cookie值)
    ends = 'ends' 
    # cookie示例：%u6DF1%u5733%2CIOQ 深圳 
    # xb =['硬座座'] 
    # pz=['成人票']
    mail_name = 'mail_name' #发件邮箱
    mail_pass = 'mail_pass'#授权密码
    smtp_server = 'smtp_server'# 输入SMTP服务器地址
    to_addr = ['to_addr']# 输入收件人地址:可为多个，组成列表


    Buy_Tickets(username, password, order, passengers, dtime, starts, ends,mail_name,mail_pass,smtp_server,to_addr).start_buy()
    print("请问你是否需要退出？")
    out = "N"
    while  out != "Y":
        out=input("请输入Y/N")