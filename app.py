from flask import Flask ,render_template, request,Response 
import sqlite3
import os
import uuid
import csv
import io

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form.html',methods=['GET','POST'])
def form():
    return render_template('form.html')
    

@app.route('/submit-form', methods=['POST'])
def submit_form():
    id = str(uuid.uuid4())[0:15]

    date = request.form.get('date')
    place = request.form.get('place')
    name = request.form.get('name')
    gender = request.form.get('gender')
    cheif_complaint = request.form.get('complaint')
    past_medical_history = request.form.get('history')
    past_dental_visit = request.form.get('visit')
    personal_habits = request.form.get('habits')
    tooth_number = request.form.get('toothnumber')
    decayed = request.form.get('decayed')
    missing = request.form.get('missing')
    filled = request.form.get('filled')
    pain = request.form.get('pain')
    fractured = request.form.get('fractured')
    mobility = request.form.get('mobility')
    others = request.form.get('others')
    gingiva = request.form.get('gingiva')
    description = request.form.get('comment')
    dental_fluorosis = request.form.get('floro')
    malocclusion = request.form.get('malo')
    oral_muscosal_lesion = request.form.get('masc')
    condition = request.form.get('condition')
    location = request.form.get('location')
    treatment_done = request.form.get('treatment')
    expalnation = request.form.get('explanation')



    conn = sqlite3.connect('patient.db') # create a database if it does not exist
    c = conn.cursor()

    # create a table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS Patients
                (Patient_id TEXT,dateofvisit TEXT,place TEXT,name_of_patient TEXT,gender TEXT,cheif_complaint TEXT,past_medical_history TEXT,past_dental_visit TEXT,personal_habits TEXT,tooth_number INTEGER,decayed_tooth INTEGER,missing_tooth INTEGER,filled_tooth INTEGER,pain_in_tooth INTEGER,fractured_tooth INTEGER,mobility_tooth INTEGER,others TEXT,gingiva TEXT,description TEXT,dental_fluorosis TEXT, malocclusion TEXT,oral_muscosal_lesion TEXT,location TEXT,condition TEXT,treatment_done TEXT,expalnation TEXT)''')

    # insert data into the table
    c.execute("INSERT INTO Patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,date,place,name,gender,cheif_complaint,past_medical_history,past_dental_visit,personal_habits,tooth_number,decayed,missing,filled,pain,fractured,mobility,others,gingiva,description,dental_fluorosis,malocclusion,oral_muscosal_lesion,condition,location,treatment_done,expalnation))

    conn.commit()
    conn.close()
    return 'Form submitted successfully!'


# Define the route to display the data
@app.route('/display-data')
def display_data():
    # Connect to the database
    conn = sqlite3.connect('patient.db')

    # Get a cursor object
    cursor = conn.cursor()

    # Execute a SELECT query to get all the data from the table
    cursor.execute('SELECT * FROM Patients')

    # Fetch all the rows from the query result
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Pass the rows to a Jinja2 template for rendering
    return render_template('show.html', rows=rows)


@app.route('/download-data')
def download_data():
    # Get data from the database
    conn = sqlite3.connect('patient.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Patients')
    rows = cur.fetchall()
    conn.close()

    # Create a CSV file from the data
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Date', 'Place','Name','Gender', 'Cheif_complaint','past_medical_history','past_dental_visit','personal_habits','tooth_number','decayed','missing','filled','pain','fractured','mobility','others','gingiva','description','dental_fluorosis','malocclusion','oral_muscosal_lesion','condition','location','treatment_done','expalnation'])  # Add column headings
    for row in rows:
        writer.writerow(row)

    # Create a response object to return the file
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'

    return response



if __name__ == '__main__':
    app.run(debug=True)
    

