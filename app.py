#import flask   
from flask import Flask, render_template, abort


#render templates from templates folder
app = Flask(__name__)
# import cors from flask_cors

@app.route('/')
def index():
    api_key = "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg"
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return render_template('index.html')

@app.route('/map')
def map():  
    # creating a map in the view
    return render_template('map.html')

#run local server
if __name__ == '__main__':
    app.run(host="localhost",debug=True)
