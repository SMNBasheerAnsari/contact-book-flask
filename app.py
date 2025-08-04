from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

contacts=[] # in-memory storage list for contacts as a doctionary 

@app.route('/')
def index():
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        contacts.append({'name':name, 'phone': phone, 'email': email})
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
