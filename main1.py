from re import template
import re
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime

app = Flask(__name__, template_folder='template')

@app.route('/', methods=['GET', 'POST'])
def home():
    User_acc = ["", ""]
    if request.method == 'POST':
        User_acc[0] = request.form["username"]
        User_acc[1] = request.form["password"]
        if User_acc[0]=='root' and User_acc[1]=='cuong9401':
            return redirect(url_for('homepage'))
        return redirect(url_for('/'))
    return render_template("index.html")
################################################################
##CONNECT TO MYSQL
con = mysql.connector.connect(
    user='root',
    password='cuong9401',
    host='localhost',
    database='mydb'
)
cur = con.cursor()

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        if request.form['submitbutton'] == "Search for patient information":
            return redirect(url_for('search_patient'))
        elif request.form['submitbutton'] == "Add inpatient information":
            return redirect(url_for('add_inpatient'))
        elif request.form['submitbutton'] == "Add outpatient information":
            return redirect(url_for('add_outpatient'))
        elif request.form['submitbutton'] == "Search for information of patient treated by doctor":
            return redirect(url_for('patient_treatedby_doctor'))
        elif request.form['submitbutton'] == "Total payment":
            return redirect(url_for('total_payment'))
    return render_template('homepage.html')

@app.route('/homepage/search_patient', methods=['GET', 'POST'])
def search_patient():
    args = ['','']
    if request.method == 'POST':
        if request.form['button'] == "Home":
            return redirect(url_for('homepage'))
        elif request.form['button'] == "Search":
            args[0] = request.form["firstname"] 
            args[1] = request.form["lastname"]

    cur.callproc('Search_patient', args)
    for i in cur.stored_results():
        data = i.fetchall()
        for j in range (0, len(data)):
            if not data:
                pass
            else:
                data1 = list(data[j])
                if data1[5] == 'm': 
                    data1[5] = 'Male'
                elif data1[5] == 0:
                    data1[5] = 'f'
                else: 
                    continue
                data[j] = tuple(data1)
    print(data)
    return render_template('search_patient.html', data=data)

@app.route('/homepage/add_inpatient', methods=['POST', 'GET'])
def add_inpatient():
    if request.method == 'POST':
        if request.form['button'] == "Home":
            return redirect(url_for('homepage'))
        elif request.form['button'] == "Add":
            args = (
                request.form['code'],
                request.form['address'],
                request.form['firstname'],
                request.form['lastname'],
                datetime.datetime.strptime(request.form['birthday'], "%Y-%m-%d"),
                request.form['gender'],
                request.form['phonenumber'],
                request.form['nur_code'],
                datetime.datetime.strptime(request.form['DOA'], "%Y-%m-%d"),
                request.form['room'],
                datetime.datetime.strptime(request.form['DOD'], "%Y-%m-%d"),
                request.form['fee'],
                request.form['dia'],
            )
            print(args)
            cur.callproc('ADD_INPATIENT', args)
            con.commit()

    return render_template('add_inpatient.html')

@app.route('/homepage/add_outpatient', methods=['POST', 'GET'])
def add_outpatient():
    if request.method == 'POST':
        if request.form['button'] == "Home":
            return redirect(url_for('homepage'))
        elif request.form['button'] == "Add":
            args = (
                request.form['code'],
                request.form['address'],
                request.form['firstname'],
                request.form['lastname'],
                datetime.datetime.strptime(request.form['birthday'], "%Y-%m-%d"),
                request.form['gender'],
                request.form['phonenumber'],
                request.form['doc_code']
            )
            print(args)
            cur.callproc('ADD_OUTPATIENT', args)
            con.commit()

    return render_template('add_outpatient.html')

@app.route('/homepage/patient_treatedby_doctor', methods=['POST', 'GET'])
def patient_treatedby_doctor():
    args = ['','']
    if request.method == 'POST':
        if request.form['button'] == "Home":
            return redirect(url_for('homepage'))
        elif request.form['button'] == "Search":
            args[0] = request.form["firstname"] 
            args[1] = request.form["lastname"]

    cur.callproc('PRINT_PATIENTS_HAVE_DOCTOR', args)

    for i in cur.stored_results():
        data = i.fetchall()
        for j in range (0, len(data)):
            if not data:
                pass
            else:
                data1 = list(data[j])
                if data1[4] == 'm' or data1[4] == 1: 
                    data1[4] = 'Male'
                elif data1[4] == 'f' or data1[4] == 0:
                    data1[4] = 'Female'
                else: 
                    continue
                data[j] = tuple(data1)
    print(data)
    return render_template('patient_treatedby_doctor.html', data=data)

@app.route('/homepage/total_payment', methods=['POST', 'GET'])
def total_payment():
    args = ['']
    if request.method == 'POST':
        if request.form['button'] == "Home":
            return redirect(url_for('homepage'))
        elif request.form['button'] == "Search":
            args[0] = request.form["ID"]
    cur.callproc('TOTAL_PAYMENT', args)
    
    for i in cur.stored_results():
        data = i.fetchall()

    print(args)
    return render_template('total_payment.html', data=data)

if __name__ == "__main__":
    app.run(port=5000, debug=True)