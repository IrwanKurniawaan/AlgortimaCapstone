from flask import Flask, request, sqlite3
import pandas as pd

app = Flask(__name__) 


@app.route('/data/')
def data():
    df = pd.read_csv('D:/_Training Algoritma/_Capstone/p4da-capstone-api-master/data/books_c.csv')
    return (df.to_json())

#GetCsvFileData
@app.route('/data/get/datacsv/<csvfile>', methods=['GET']) 
def getcsvfile(csvfile): 
    data = pd.read_csv('D:/_Training Algoritma/_Capstone/p4da-capstone-api-master/data/' + str(csvfile))
    return (data.to_json())

#bookinfo
@app.route('/data/get/books/<column>/<value>', methods=['GET']) 
def get_data_equal(column, value): 
   data = pd.read_csv('D:/_Training Algoritma/_Capstone/p4da-capstone-api-master/data/books_c.csv')
   mask = data[column] == value
   data = data[mask]
   return (data.to_json())

@app.route('/form', methods=['GET', 'POST']) #allow both GET and POST requests
def form():
    if request.method == 'POST':  # Hanya akan tampil setelah melakukan POST (submit) form
        key1 = 'name'
        key2 = 'age'
        name = request.form.get(key1)
        age = request.form[key2]

        return (f'''<h1>Your Name  is: {name}</h1>
                   <h1>Your Age is: {age}</h1>
                ''')


    return '''<form method="POST">
                  Name: <input type="text" name="name"><br>
                  Age: <input type="text" name="age"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/sebut_nama/<nama>', methods=['GET']) 
def sebut_nama(nama):
    return ("halo " + nama )

@app.route('/home')
def home():
    return 'Hello World Algoritma Capstone'

@app.route('/')
def fungsiroot():
	return 'Welcome to Home Page'

@app.route('/coba', methods=['GET', 'POST'])
def terserah():
    if request.method == 'GET':
        return "Ini adalah Hasil method GET"
    else:
        return "Ini adalah hasil method POST"

if __name__ == '__main__':
    app.run(debug=True, port=5000)