from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import DecimalField,SubmitField
from wtforms.validators import DataRequired
import requests
import os


params = {
	"grant_type": "password",
	"client_id": os.environ['CLIENT_ID'],
	"client_secret": os.environ['CLIENT_SECRET'],
	"username": os.environ['USERNAME'],
	"password": os.environ['PASSWORD']
}

r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")
# print(access_token)
# print(instance_url)

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

class TempForm(FlaskForm):
	temp = DecimalField("Enter your ideal office temperature.", validators=[DataRequired()])
	submit = SubmitField("Submit")

@app.route('/',methods=['GET','POST'])
def home():
	temp = False

	form = TempForm()

	if form.validate_on_submit():
		temp = form.temp.data
		create_platform_event(temp)
		session['temp'] = form.temp.data
		form.temp.data = ''
		return redirect(url_for('thank_you'))

	return render_template('home.html',form=form,temp=temp)

@app.route('/thankyou')
def thank_you():

    return render_template('thank_you.html')

def create_platform_event(temp):
	headers = {
		"Content-type": "application/json",
		"Authorization": "Bearer %s" % access_token
		}
	data = {
		"Coworker_Name__c" : "Mark Blatnik",
		"Ideal_Temperature__c" : temp
		}

	r = requests.post(instance_url+'/services/data/v44.0/sobjects/Ideal_Temperature__e', headers=headers, json=data, timeout=10)
	# print(r)

if __name__ == "__main__":
	app.run()