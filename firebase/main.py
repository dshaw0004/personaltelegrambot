import firebase_admin
from firebase_admin import credentials

import os, json

creds_str = os.getenv('FIREBASE_CREDS', '')

cred = credentials.Certificate(json.loads(creds_str))
app = firebase_admin.initialize_app(cred)


