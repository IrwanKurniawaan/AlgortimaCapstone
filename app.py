from flask import Flask, request
import sqlite3
import pandas as pd

app = Flask(__name__) 

#PROJECT CAPSTONE
@app.route('/data/')
def data():
    df = pd.read_csv('/data/books_c.csv')
    return (df.to_json())


#GetCsvFileData
@app.route('/data/get/datacsv/<csvfile>', methods=['GET']) 
def getcsvfile(csvfile): 
 	data = pd.read_csv('/data/' + str(csvfile))
 	return (data.to_json())

#Getfrom chinook
#Join 4 tables
@app.route('/data/get/chinook/topgenres') 
def topgenres():
 	conn = sqlite3.connect("data/chinook.db")
 	key1 = 'country'
	key2 = 'year'
	where = ''
	country = request.args.get(key2)
	sql = '''
		SELECT
			BillingCountry as Country, d.Name as Genre, strftime('%Y', a.invoicedate) Year
			FROM invoices a
			LEFT JOIN invoice_items b on a.InvoiceId = b.InvoiceId
			LEFT JOIN tracks c ON b.TrackId = c.TrackId
			LEFT JOIN genres d ON c.GenreId = d.GenreId
		'''

	if (country and year):
		where = " WHERE lower(Country) like '%" +country.lower()+"%' and Year='"+year+"'"
	elif (country):
		where = " WHERE lower(Country) like '%" +country.lower()+"%'"
	elif (year):
		where = " WHERE Year='"+year+"'"
	else:
		where = ''

	sql = sql + where
	topgenres = pd.read_sql_query(sql,conn)

	if(topgenres['Country'].notna().sum() > 0):
		return(topgenres.to_json())
	
	return 'Data Not Exists!!'


#salesriceYearly
#masih error, syhtax di jupyters jalan, tapi di comple python tidak jalan
#TabError: inconsistent use of tabs and spaces in indentation
@app.route('/data/get/salesrice/<salesyears>', methods=['GET']) 
def salesrice(salesyears): 
 	datacsv = pd.read_csv("/data/rice.csv",index_col=0,parse_dates=['purchase_time'])
	datacsv['PurchaseDOW'] = datacsv['purchase_time'].dt.day_name() 
	datacsv['PurchaseYear'] = datacsv['purchase_time'].dt.year
	#categorical operation
	datacsv[['category','sub_category','format','yearmonth','PurchaseDOW']] = datacsv[['category','sub_category','format','yearmonth','PurchaseDOW']].astype('category') 
	datacsv['unit_price'] = datacsv['unit_price'].astype('int64')
	datacsv['sales_value'] = datacsv['unit_price'] * datacsv['quantity']
	datacsv.drop(['receipt_id', 'receipts_item_id', 'sub_category','purchase_time','discount'], axis=1, inplace=True)
	#melt,groupby, frequency operation
	datacsv[datacsv['PurchaseYear'] == salesyears].\
	pivot_table(
	    index='yearmonth',
	    columns=['format'],
	    values='unit_price',
	    aggfunc='sum'
	).melt().groupby(['format']).sum()

	return (datacsv.to_json())

#2. Dynamic
@app.route('/data/get/chinook/')
def genre():
   pass 
  #df = pd.read_csv('/data/books_c.csv')
 #return (df.to_json())



#Document



# LATIHAN CAPSTONE
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