from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

mydb = mysql.connector.connect(
    host="lin-2550-2638-mysql-primary.servers.linodedb.net",
    user="linroot",
    passwd="wgghNd0PB4h-zie1",
    database="find"
)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findV")
    myresult = mycursor.fetchall()
    return render_template('result.html', results=myresult,)

@app.route('/map', methods=['POST'])
def map():
    if request.method == 'POST':
        return render_template('map.html')

@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST' or 'GET':
        Vehno = request.form.get('Vehno')
        Location = request.form.get('Location')
        print(Vehno, Location)
        mycursor = mydb.cursor()  
        mycursor.execute('''INSERT INTO findV(Vehno,Location) VALUES("%s","%s")''',(Vehno,Location))
        mydb.commit()
        mydb.close()
        
        return '''
        <h1>Data Inserted Successfully</h1>
        
        '''
            
    else:
        return render_template('index.html')

if __name__ == '__main__':
    context = ('/home/mkv/Desktop/app/ca.crt')
    app.run(debug=True)