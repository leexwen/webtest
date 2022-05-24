"""
使用一个邮箱对另外一个邮箱发送测试报告的html文件,这里需要对发送邮件的邮箱进行设置,获取邮箱授权码
username = "发送邮件的邮箱 "
password = "邮箱授权码 "
mail_server = " 发送邮箱的服务器地址 "
这里常用的 有 qq邮箱——“stmp.qq.com",163邮箱——”stmp.163.com"
"""

# 自动发送邮件
import os
import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendEmail():
    def send_email(self, new_report):
        # 读取测试报告中的内容作为邮件的内容
        with open(new_report, 'r', encoding='utf-8') as f:
            mail_body = f.read()
        # 发件人地址
        send_address = '1339888671@qq.com'
        # 收件人地址
        receiver_address = '1339888671@qq.com'
        # 发送邮箱的服务器地址
        mail_server = 'smtp.qq.com'
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        # 邮件标题
        subject = 'web自动化测试报告' + now
        # 发件人的邮箱及其邮箱授权码
        username = '1339888671@qq.com'
        password = 'shcmltrnzweghdcf'

        message = MIMEMultipart()
        # 邮箱的内容和标题
        text = MIMEText(mail_body, 'html', 'utf-8')
        text['subject'] = Header(subject, charset='utf-8')
        message.attach(text)
        # 邮件的附件
        msg_file = MIMEText(mail_body, 'html', 'utf-8')
        msg_file['Content-Type'] = 'application/octet-stream'
        msg_file["Content-Disposition"] = 'attachment;filename=TestReport.html'
        message.attach(msg_file)

        # 发送邮件 使用的SMTP协议
        smtp = smtplib.SMTP()
        # 连接
        smtp.connect(mail_server)
        # 登录
        smtp.login(username, password)
        # 发送
        smtp.sendmail(send_address, receiver_address.split(','), message.as_string())
        # 退出
        smtp.quit()
        print('发送邮件成功')

    # 读取最新的测试报告地址
    def acquire_report_address(self, reports_address):
        # 测试报告文件夹中的所有文件加入到列表
        test_report_list = os.listdir(reports_address)
        # 按照升序排序生成新的列表
        new_test_reports_list = sorted(test_report_list)
        # 获取最新的测试报告
        the_last_report = new_test_reports_list[-1]
        # 最新的测试报告地址
        the_last_report_address = os.path.join(reports_address, the_last_report)
        return the_last_report_address