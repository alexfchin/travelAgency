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
               "(Name, CardNumber, ExpDate, SVC, TransportationType, TransportationID) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
write_review = ("INSERT INTO Reviews "
               "(Name, Stars, Content) "
               "VALUES (%s, %s, %s)")
hotel_reservation = ("INSERT INTO Reservations "
                     "(PassengerID, Type, StartDate, EndDate) "
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
    return render_template('ShowTransportation.html', data=db_data) #pass data into the html

@app.route('/payment', methods=['POST'])
def payment():
    _transportationType = request.form['transportType']
    _transportationID = request.form['transportID']
    print(_transportationType + "    " + _transportationID)
    return render_template('Payment.html')

@app.route('/confirmPayment', methods=['POST'])
def confirmPayment(): #add passenger to sql db
    _transportationType = request.form['transportType']
    _transportationID = request.form['transportID']
    _cardNumber = request.form['cardNumber']
    _cardHolder = request.form['cardHolder']
    _month = request.form['month']
    _year = request.form['year']
    _svc = request.form['svc']

    _expDate = _month + '/' + _year
    passenger_data = (_cardHolder, _cardNumber, _expDate, _svc, _transportationType, _transportationID)
    cursor.execute(create_passenger,passenger_data)
    conn.commit() #commits to the db

    return render_template('ConfirmPayment.html')

@app.route("/reviews", methods=['GET','POST'])
def reviews():
    if request.method == 'POST':
        _name = request.form['name']
        _stars = request.form['stars']
        _content = request.form['content']
        review_data = (_name, _stars, _content)
        cursor.execute(write_review, review_data)
        cursor.execute("SELECT * FROM Reviews ORDER BY ReviewID DESC;")
        db_data = cursor.fetchall()  # get data from cursor
        return render_template('Reviews.html', data=db_data)
    else:
        #just show the reviews
        cursor.execute("SELECT * FROM Reviews ORDER BY ReviewID DESC;")
        db_data = cursor.fetchall()  # get data from cursor
        return render_template('Reviews.html', data=db_data)



@app.route("/test", methods=['POST'])
def test():
    _name = request.form['name']
    print(_name)
    return "OK"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
