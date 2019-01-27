# Schultz Project

_Project Statement:_
Create a simple Heroku app in the language of your choice. This app will provide a simple web page where a user can enter a text value and press a SEND button. The app will then publish a Salesforce Platform Event defined by your Salesforce org. Upon receiving the event, a Process Builder process in the org will update a text field on a single Custom Object record with the value entered by the user.

_General Steps:_

1. Define a Platform Event in the org
2. Define a Connected App that represents the Heroku app. This Connected App will provide the OAuth client and secret needed to publish Platform Events to your Salesforce org.
3. Build a Heroku app with a simple web interface including a text field and Send button.
4. Write the Heroku logic to authenticate with Salesforce and publish the Platform Event.
5. Create a Process Builder process that subscribes to the Platform Event. The process will update the text field on one specific custom record in your org.