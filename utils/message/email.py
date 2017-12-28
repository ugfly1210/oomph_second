#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from .base import BaseMessage
class Email(BaseMessage):
    def __init__(self):
        self.email = 'ugfly@qq.com'
        self.user = '777'
        self.pwd = ''
    def send(self,subject,body,to,name):
        msg = MIMEText(body,'plain','utf-8')
        msg['Form'] = formataddr([self.user,self.email])
        msg['To'] = formataddr([name,to])
        msg['Subject'] = subject
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # SMTP服务
        server.login(self.email, self.pwd) # 邮箱用户名和密码
        server.sendmail(self.email, [to, ], msg.as_string()) # 发送者和接收者
        server.quit()
# class Email(BaseMessage):
#     def __init__(self):
#         self.email = "m394559@126.com"
#         self.user = "wusir"
#         self.pwd = 'WOshiniba'
#
#     def send(self,subject,body,to,name):
#
#         msg = MIMEText(body, 'plain', 'utf-8')  # 发送内容  #
#         msg['From'] = formataddr([self.user,self.email])  # 发件人
#         msg['To'] = formataddr([name, to])  # 收件人
#         msg['Subject'] = subject # 主题
#
#
#         server = smtplib.SMTP("smtp.126.com", 25) # SMTP服务
#         server.login(self.email, self.pwd) # 邮箱用户名和密码
#         server.sendmail(self.email, [to, ], msg.as_string()) # 发送者和接收者
#         server.quit()


# import smtplib
# from email.mime.text import MIMEText
# import string
#
# #第三方SMTP服务
# mail_host = "smtp.qq.com"           # 设置服务器
# mail_user = "3@qq.com"        # 用户名
# mail_pwd  = ""      # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
# mail_to  = ['2@qq.com','2@qq.com',]     #接收邮件列表,是list,不是字符串
#
# #邮件内容
# msg = MIMEText("叉")      # 邮件正文
# msg['Subject'] = "大"     # 邮件标题
# msg['From'] = mail_user        # 发件人
# msg['To'] = ','.join(mail_to)         # 收件人，必须是一个字符串
#
# try:
#     smtpObj = smtplib.SMTP_SSL(mail_host, 465)
#     smtpObj.login(mail_user, mail_pwd)
#     smtpObj.sendmail(mail_user,mail_to, msg.as_string())
#     smtpObj.quit()
#     print("邮件发送成功!")
# except smtplib.SMTPException:
#     print ("邮件发送失败!")