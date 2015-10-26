from flask import flash, Flask, g, render_template, session, redirect, url_for, escape, request, send_from_directory
from functools import wraps
import os
from os import listdir
from os.path import isfile, join
import platform
from datetime import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText

#set up for for python program
app= Flask(__name__, static_folder='static')
app.secret_key = (';\x88\xcb\xdfz\xafh\xff\xff:*8!\x96\xcd\xd5\x0b]\xef\x9cF\xa0\xc8')

genPass = "idk"


@app.route('/', methods=['GET', 'POST'])
def index():
  if 'client' not in session:
    session['client'] = False
  print session['client']
  return render_template('home.html', currentpage="comp", client=session['client']);

@app.route('/company', methods=['GET', 'POST'])
def almostIndex():
  return render_template('home.html', currentpage="comp", client=session['client']);


@app.route('/logging', methods=['POST'])
def enter():
  if request.method == "POST":
    """m = hashlib.md5()
    m.update((request.form['pass']).encode() )
    password = m.digest()"""
    password = request.form['pass']
    print password
    #improve security later
    if password == genPass:
      session['client'] = True
    return redirect('/')

@app.route('/logout', methods=['GET'])
def clear():
  session['client'] = False
  return redirect('/')

@app.route('/team', methods=['GET', 'POST'])
def people():
  return render_template('team.html', currentpage="team", client=session['client'])

@app.route('/invest', methods=['GET', 'POST'])
def philo():
  return render_template('philo.html', currentpage="philo", client=session['client'])

@app.route('/letter', methods=['GET', 'POST'])
def letter():
  path = "static\statements"
  print path
  letterFiles = [ f for f in listdir(path) if isfile(join(path,f))]
  print letterFiles
  return render_template('letters.html', currentpage="letr", client=session['client'], files = letterFiles)

@app.route('/pubs', methods=['GET', 'POST'])
def publications():
  return render_template('publications.html', currentpage="pubs", client=session['client'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  return render_template("contact.html", currentpage="contact", client=session['client'])

@app.route('/msg', methods=['GET', 'POST'])
def send():
  if request.method == "POST":
    print request.form['msg']
    message = MIMEText(request.form['msg'])
    sender = request.form['email']
    print sender
    message["From"] = sender
    subj = request.form['subj']
    print subj
    message["Subject"] = request.form['subj']
    message['To'] = "benedict.bolton@gmail.com"
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, ["benedict.bolton@gmail.com"], message.as_string())
    s.quit
  return render_template("contact.html", currentpage="contact", client=session['client'], msgSent=True)


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.debug = True
  app.run(host='0.0.0.0', port=port)
