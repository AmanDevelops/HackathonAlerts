import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import os

load_dotenv()

cred = credentials.Certificate('secret.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('DATABASE_URLS')
})

ref = db.reference('hackathons')