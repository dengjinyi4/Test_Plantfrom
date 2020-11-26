__author__ = 'emar0901'
import pyotp
import qrcode
import base64,os
from utils import login as l
if __name__ == '__main__':

    # sec=pyotp.random_base32()
    # sec='base32secret3232'
    # # sec= base64.b32encode(os.urandom(10)).decode('utf-8')
    # topt=pyotp.TOTP(sec)
    # qr_uri = pyotp.totp.TOTP(sec).provisioning_uri('mytest')
    # print qr_uri
    # img = qrcode.make(qr_uri)
    # img.save('test.png')
    # print img.get_image
    # img.get_image().show()
    # print topt.verify(249422)
    print 1
    # os.chdir('../utils/login.py')
    # print os.getcwd()
    user=l.login(username='dengjinyi122222')
    imgurl=user.otppic()
    print imgurl
    # img.save(imgurl)




