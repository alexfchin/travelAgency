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

#cursor to perform sql operations
conn = mysql.connect()
cursor = conn.cursor()

create_passenger = ("INSERT INTO Passengers "
               "(PassengerName, Email, Password, GroupName) "
               "VALUES (%s, %s, %s, %s)")

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/flights')
def flights():
    return render_template('Flights.html')


@app.route("/showTransportation", methods=['POST']) #grab from database and display values
def showTransportation():
    #send what type of thing
    _transportType = request.form['transportType']
    _from = request.form['from']
    _to = request.form['to']
    _departDate = request.form['departDate']
    _returnDate = request.form['returnDate']
    _class = request.form['class']

    transportData = (_transportType, _from, _to, _departDate, _returnDate, _class)
    print(transportData)


    select_transportation = ("SELECT * FROM " + _transportType
                             + " WHERE Class = '"+ str(_class)+ "';")
    print(select_transportation)
    cursor.execute(select_transportation)

    db_data = cursor.fetchall() #get data from cursor
    return render_template('test.html', data=db_data) #pass data into the html

@app.route('/payment', methods=['POST'])
def payment():
    _id = request.form['id']
    print(_id)
    return render_template('index.html')


@app.route('/cruises')
def cruises():
    return render_template('Cruises.html')

@app.route('/cars')
def cars():
    return render_template('Cars.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['username']
    _password = request.form['password']
    _email = request.form['email']
    _groupname = request.form['group']
    passenger_data = (_name,_password, _email, _groupname)
    #execute sql query

    cursor.execute(create_passenger,passenger_data)
    conn.commit() #commits to the db
    data = cursor.fetchOne()
    print(data)

    return "CREATED ACCOUNT"





@app.route("/test", methods=['POST'])
def test():
    _name = request.form['name']
    print(_name)
    return "OK"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
