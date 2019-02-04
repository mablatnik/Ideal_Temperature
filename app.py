from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField
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
	max_temp = IntegerField("Set the maximum temperature for your comfort zone.", validators=[DataRequired()])
	min_temp = IntegerField("Set the minimum temperature for your comfort zone.", validators=[DataRequired()])
	submit = SubmitField("Submit")

@app.route('/',methods=['GET','POST'])
def home():
	max_temp = False
	min_temp = False

	form = TempForm()

	if form.validate_on_submit():
		max_temp = form.max_temp.data
		min_temp = form.min_temp.data
		create_platform_event(min_temp, max_temp)
		session['max_temp'] = form.max_temp.data
		session['min_temp'] = form.min_temp.data
		form.max_temp.data = ''
		form.min_temp.data = ''
		return redirect(url_for('thank_you'))

	return render_template('home.html',form=form, max_temp=max_temp, min_temp=min_temp)

@app.route('/thankyou')
def thank_you():

    return render_template('thank_you.html')

def create_platform_event(min_temp, max_temp):
	headers = {
		"Content-type": "application/json",
		"Authorization": "Bearer %s" % access_token
		}
	data = {
		"deskId__c" : "0634",
		"MAX_TEMPERATURE__c" : max_temp,
		"MIN_TEMPERATURE__c" : min_temp
		}

	r = requests.post(instance_url+'/services/data/v44.0/sobjects/Temp_Global_Variable__e', headers=headers, json=data, timeout=10)
	print(r)

if __name__ == "__main__":
	app.run()