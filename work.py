from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "dfdfdffdad"

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/mystring')
def mystring():
    return 'my 1111string'

@app.route('/dataFromAjax')
def dataFromAjax():
    test = request.args.get('mydata')
    print(test)
    return 'dataFromAjax'

@app.route('/333/mydict', methods=['GET', 'POST'])
def mydict():
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)
@app.route('/333/mydict1/<id>', methods=['GET', 'POST'])
def mydict1(id):
    d = "test"+str(id)
    print d
    return d

@app.route('/mylist')
def mylist():
    l = ['xmr', 18]
    return jsonify(l)


if __name__ == '__main__':
   app.run( host="0.0.0.0",port=21333,debug=True,threaded=True)