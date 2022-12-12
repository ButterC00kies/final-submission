# Importing the dependencies
import mysql.connector as conn
import requests
from flask import Flask, request, jsonify

Movie = input("Movie_name : ")

# connecting DB with python
mydb = conn.connect(host="localhost", user="root", passwd="****")
Cursor = mydb.cursor()

try:
    # if required data is present inside the DB, then retrieve it
    q = f"SELECT * FROM API_TASK.movie_info where Title = '{Movie}'"
    Cursor.execute(q)
    result = Cursor.fetchall()

    # if the requested data is not inside the DB scrap it using API
    if len(result) == 0:
        apikey = "cb3d27fd"
        data = requests.get('http://www.omdbapi.com/?t=' + Movie + '&apikey=cb3d27fd')
        detail = data.json()
        keys = ['Title', 'Year', 'Released', 'Genre', 'imdbRating', 'imdbID']
        val = list(map(detail.get, keys))

        # Inserting the required information to the database after scraping it
        q = f'INSERT INTO API_TASK.movie_info (Title,Year,Released,Genre,imdbRating,imdbID) values("{val[0]}","{val[1]}","{val[2]}","{val[3]}","{val[4]}","{val[5]}")'
        Cursor.execute(q)
        mydb.commit()
        print("Data stored successfully")
        print(val)

    else:
        print(result)

except Exception as e:
    print(e)


# Creating flask api
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def login():
    try :
        if request.method == 'GET':
            user = request.form['value']
            column = request.form['column_name']
            mydb = conn.connect(host="localhost", user="root", passwd="_Aj@y1234_")
            Cursor = mydb.cursor()
            query = "USE API_TASK"
            Cursor.execute(query)
            """
            Here you need to write the column and relevant value in whose reference you want fetch the data 
            like select * from movie_info where Title = "Iron-Man';
            """
            query1 = f"SELECT * FROM movie_info where {column} = '{user}'"
            Cursor.execute(query1)

            result = Cursor.fetchall()
            return result

    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(port = 57558, debug=True)
