
from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Firebase Initialization
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://water-quality-monitor-cdf19-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace with your database URL
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    ref = db.reference('water')  # <-- this must match your Firebase root key
    data = ref.get()
    print("Firebase data:", data)
    if data:
        return jsonify(data)
    return jsonify({})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
