
# from flask import Flask, render_template, jsonify
# import firebase_admin
# from firebase_admin import credentials, db

# app = Flask(__name__)

# # Firebase Initialization
# cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your path
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://water-quality-monitor-cdf19-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace with your database URL
# })

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_data')
# def get_data():
#     ref = db.reference('water')  # <-- this must match your Firebase root key
#     data = ref.get()
#     print("Firebase data:", data)
#     if data:
#         return jsonify(data)
#     return jsonify({})



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

import os
from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Configure Firebase
def initialize_firebase():
    # Try to get credentials from environment variable first
    if 'FIREBASE_CREDENTIALS' in os.environ:
        import json
        cred_dict = json.loads(os.environ['FIREBASE_CREDENTIALS'])
        cred = credentials.Certificate(cred_dict)
    else:
        # Fallback to serviceAccountKey.json
        cred = credentials.Certificate("serviceAccountKey.json")
    
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://water-quality-monitor-cdf19-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

initialize_firebase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    ref = db.reference('water')
    data = ref.get()
    return jsonify(data or {})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)