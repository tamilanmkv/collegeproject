from cv2 import trace
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_cors import CORS

mydb = mysql.connector.connect(
    host="lin-2550-2638-mysql-primary.servers.linodedb.net",
    user="linroot",
    passwd="wgghNd0PB4h-zie1",
    database="find"
)


app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('home.html')
    

@app.route('/result')
def result():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findV")
    myresult = mycursor.fetchall()
    return render_template('result.html', results=myresult,)

@app.route('/results/<string:vehno>')
def results(vehno):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Latitude,Longitude FROM findV WHERE Vehno = %s", (vehno,))
    myresult = mycursor.fetchall()
    return render_template('results.html', results=myresult) 

@app.route('/result/<string:vehno>')
def result_vehno(vehno):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findV where Vehno = %s", (vehno,))
    myresult = mycursor.fetchall()
    return render_template('result.html', results=myresult,)

@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        vno = request.form.get('vno')
        # call /reults/vno
        # return for loop
        data = [data for data in results(vno)]
        return render_template('map.html',results=data)
    else:

        #data = list(results(vno))
        return render_template('map.html')
@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        Vehno = request.form.get('Vehno')
        Location = request.form.get('Location')
        mycursor = mydb.cursor()  
        mycursor.execute('''INSERT INTO findV(Vehno,Location) VALUES(%s,%s)''',(Vehno,Location))
        mydb.commit()
        mydb.close()
        return render_template("index.html")
    else:
        return render_template("index.html")
@app.route('/other')
def other():
    # fetch data from findBlock
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findBlock")
    myresult = mycursor.fetchall()
    return render_template('other.html', results=myresult,)
    #return render_template('other.html')

@app.route('/block', methods=['GET','POST'])
def block():
    #return render_template("block.html")
    if request.method == 'GET':
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM findBlock")
        myresult = mycursor.fetchall()
        mycursor.execute("select * from blockNO")
        myresult2 = mycursor.fetchall()
        print(myresult)
        print(myresult2)
        if myresult[0] == myresult2[0]:
        #mydb.commit()
            print(myresult)
            return render_template("block.html",results=myresult)
        
        return render_template("block.html")
    if request.method == 'POST':
        Vehno = request.form.get('Vehno')
        # drop table if exists
        mycursor = mydb.cursor()
        mycursor.execute("insert into blockNO(vno) values(%s)",(Vehno,))
        mydb.commit()
        mydb.close()
        return render_template("block.html")
        #mycursor.execute("DROPapp.route('/cameras')
#def cameras():
#    return render_template('block.html')   TABLE IF EXISTS findBlock")
#        
#    else:
#        return render_template("block.html")


    #  mycursor = mydb.cursor()


if __name__ == '__main__':
    app.run(debug=True)