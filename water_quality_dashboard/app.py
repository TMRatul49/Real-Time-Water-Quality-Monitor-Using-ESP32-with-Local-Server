from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import json

app = Flask(__name__)

# Firebase Initialization using environment variable
# (Set GOOGLE_CREDENTIALS_JSON in Render with full service account JSON)
cred_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
if not cred_json:
    raise ValueError("GOOGLE_CREDENTIALS_JSON environment variable not set.")

cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://water-quality-monitor-cdf19-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace if needed
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    ref = db.reference('water')  # Match your Firebase structure
    data = ref.get()
    print("Firebase data:", data)
    return jsonify(data if data else {})

# Only runs when executed directly (not in Gunicorn)
if __name__ == '__main__':
    app.run(debug=True)
