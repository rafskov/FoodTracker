import sqlite3
from flask import Flask, render_template,g,request
app = Flask(__name__)


#connect to database, helper function
def connect_db():
    sql = sqlite3.connect('food_log.db')
    #resuts in a dictionary instead of a tuple
    sql.row_factory = sqlite3.Row
    return sql

#helper function to get database if not already connected
def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    #closes database at end of request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':

        #get data from form and insert to db
        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])

        calories = protein * 4 + carbohydrates * 4 + fat * 9


        db=get_db()
        db.execute('insert into food (name,protein,carbohydrates,fat,calories) values (?,?,?,?,?)',[name,protein,carbohydrates,fat,calories])
        db.commit()

    #view the food items
    cur = get_db().execute('select name,protein,carbohydrates,fat,calories from food')
    results = cur.fetchall()

    #pass results to template
    return render_template('add.html',results=results)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html')

if __name__ == "__main__":
    app.run(debug=True)
