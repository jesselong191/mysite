import os
from  django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

    send_mail(
        '来自爱圈内的确定邮件',
        '欢迎访问www.iqnei.com',
        'iqnei2020@sina.com',
        ['jesselong@qq.com'],
    )