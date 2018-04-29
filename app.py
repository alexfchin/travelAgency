from flask import Flask, render_template, session, request, json
from flask.ext.mysql import MySQL
app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password123'
app.config['MYSQL_DATABASE_DB'] = 'TravelAgency'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _groupname = request.form['inputGroup']
    print(_name + " " + _email + " " + _password)
    #execute sql query
    cursor = mysql.connect().cursor()
    cursor.execute("")

    data = cursor.fetchall() #transaction check
    if len(data) is 0:
        conn.commit() #commit change to the database
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})


@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)