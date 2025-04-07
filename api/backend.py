from flask import Flask, request
from flask_cors import CORS, cross_origin
  

from firebase.db import get_all_message, add_new_message

app = Flask(__name__, template_folder='firebase', static_folder='api')

cors = CORS(app, resources={r'/*': {"origins": "*"}})
# CORS(app, origins=['http://localhost:3000/', 'https://dshaw0004.netlify.com', 'https://dshaw0004.web.app'])

@app.route('/')
def index():
    return '''<div>
			<b>Want a different way to talk to me</b><br /><strong 
				><a
					href="https://telegram.me/dshawpersonalbot"
					target="_blank"
					rel="noopener noreferrer">chat with my bot</a
				></strong
			>
		</div>'''

@app.route("/get_all_messages")
def get_all_messages_from_db():
  messages = get_all_message()
  return messages


@app.route('/addnew', methods=['POST'])
@cross_origin(origin=['http://localhost:3000/', 'https://dshaw0004.netlify.com', 'https://dshaw0004.web.app'])
def addnew():
  content_type = request.headers.get('Content-Type')
  if content_type != 'application/json':
    return 'Content-Type not supported!'
  json = request.json
  inputdata = {
  'message': json['message'],
    'sender_name': json['senderName'],
    'sender_contact': json['senderContact']
  }
  add_new_message(message=inputdata['message'], senderName=inputdata['sender_name'], senderContact=inputdata['sender_contact'])
  # print(inputdata)

  return 'done'
      

def start_api():
  app.run(host='0.0.0.0', port=1312)
  