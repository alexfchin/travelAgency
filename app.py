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
                     "(ReservationID, HotelName, Location, Name, CardNumber, ExpDate, SVC) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)")

@app.route("/")
def index():
    return render_template('Flights.html')

@app.route('/flights')
def flights():
    return render_template('Flights.html')

@app.route('/cruises')
def cruise():
    return render_template('Cruises.html')

@app.route('/hotels')
def hotels():
    return render_template('Hotels.html')

@app.route('/showHotels', methods=['POST'])
def reservation():
    #send what type of thing
    _location = request.form['location']

    select_hotel = ("SELECT * FROM Hotels WHERE Location = '"+ str(_location)+ "';")
    cursor.execute(select_hotel)
    print(select_hotel)
    db_data = cursor.fetchall() #get data from cursor
    return render_template('showHotel.html', data=db_data)

@app.route("/showTransportation", methods=['POST']) #grab from database and display values
def showTransportation():
    #send what type of thing
    _transportType = request.form['transportType']
    _from = request.form['from']
    _to = request.form['to']
    _departDate = request.form['departDate']
    _returnDate = request.form['returnDate']
    _class = request.form['class']

    select_transportation = ("SELECT * FROM " + _transportType
                             + " WHERE Class = '"+ str(_class)+ "';")
    cursor.execute(select_transportation)

    db_data = cursor.fetchall() #get data from cursor
    return render_template('ShowTransportation.html', data=db_data) #pass data into the html



@app.route('/payment', methods=['POST'])
def payment():
    return render_template('Payment.html')

@app.route('/hotelPayment', methods=['POST'])
def payment():
    return render_template('HotelPayment.html')


@app.route('/confirmHotel', methods=['POST'])
def confirmHotel():
    _hotelName = request.form['hotelName']
    _location = request.form['hotelLocation']
    _cardNumber = request.form['cardNumber']
    _cardHolder = request.form['cardHolder']
    _month = request.form['month']
    _year = request.form['year']
    _svc = request.form['svc']

    _expDate = _month + '/' + _year
    reservation_data = (_hotelName, _location, _cardHolder, _cardNumber, _expDate, _svc)
    cursor.execute(hotel_reservation,reservation_data)
    conn.commit() #commits to the db


    return render_template('ConfirmPayment.html')

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

@app.route("/reviews")
def reviews():
    #just show the reviews
    cursor.execute("SELECT * FROM Reviews ORDER BY ReviewID DESC;")
    db_data = cursor.fetchall()  # get data from cursor
    return render_template('Reviews.html', data=db_data)

@app.route('/writeReview', methods=['GET','POST'])
def writeReview():
    if request.method == 'POST':
        _name = request.form['name']
        _stars = request.form['rating']
        _content = request.form['content']
        review_data = (_name, _stars, _content)
        cursor.execute(write_review, review_data)
        conn.commit()
        return render_template('WriteReview.html')
    else:
        return render_template('WriteReview.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
