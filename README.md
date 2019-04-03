# 12306Grab-votes
简易抢票程序，能够将登录二维码发送到邮箱，通过12306手机端扫描登录。
用户需要在main里修改username, passwd, order, passengers, dtime, starts, ends,mail_name,mail_pass,smtp_server,to_addr为用户个人信息及所需订票车次。
此脚本需求python环境，并安装好以下python包：
import requests
from splinter.browser import Browser
from time import sleep
import traceback
import time
from selenium import webdriver
from email.mime.text import MIMEText
import smtplib
使用Browser工具，建议用户使用Chrome浏览器，并安装chromedriver.exe，在line35处修改executable_path指向chromedriver.exe。
如果Firefox，请同时修改line34 与line35的driver_name，executable_path。
