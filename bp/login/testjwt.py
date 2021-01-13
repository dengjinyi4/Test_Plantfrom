from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import pyotp,base64,os

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/protected', methods= ["GET", "POST"])
@jwt_required()
def protected():
    print type(current_identity)
    return '%s' % current_identity

if __name__ == '__main__':
    # app.run()
    # sec=pyotp.random_base32()
    # sec='base32secret3232'
    # sec= base64.b32encode(os.urandom(10)).decode('utf-8')
    # topt=pyotp.TOTP(sec)
    # qr_uri = pyotp.totp.TOTP(sec).provisioning_uri('test1111')
    # print qr_uri
    # img = qrcode.make(qr_uri)
    # img.get_image().show()
    # print topt
    # print topt.verify(524923)
    tmplist=[1,2,3]
    tmp=4
    fun1=lambda x:x**x
    h=fun1(tmp)
    print h
    print list(map(fun1,tmplist))
    print map(fun1,tmplist)
    newlist=[item for item in tmplist if item>2]
    print newlist
