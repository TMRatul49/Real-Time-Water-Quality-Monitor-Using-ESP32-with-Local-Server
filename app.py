
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


from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
import smtplib
from email.message import EmailMessage
import time

app = Flask(__name__)

# Firebase Initialization
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://water-quality-monitor-cdf19-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Email Alert Config
EMAIL_ADDRESS = 'tmmehrabhasan@gmail.com'
EMAIL_PASSWORD = 'ugqtgzmpnyobwsut'  # App Password (no spaces)

# List of recipients
EMAIL_RECIPIENTS = [
    'mdsaiful000ms@gmail.com',
    '315211012@hamdarduniversity.edu.bd',
    'tmratul28@gmail.com'
]

# Optional: Cache to avoid spamming email alerts repeatedly
last_alert_time = 0
alert_interval_sec = 30  # 30 second between alerts

def send_email_alert(subject, body):
    global last_alert_time
    now = time.time()
    if now - last_alert_time < alert_interval_sec:
        print("⚠️ Skipping alert to avoid spam (rate-limited)")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(EMAIL_RECIPIENTS)
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            last_alert_time = now
            print("🚨 Email alert sent!")
    except Exception as e:
        print("❌ Email failed:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    ref = db.reference('water')
    data = ref.get()
    print("Firebase data:", data)

    if data:
        try:
            temp = float(data.get('temperature', 0))
            ph = float(data.get('ph', 0))
            tds = float(data.get('tds', 0))
            turb = float(data.get('turbidity', 0))

            alert_msgs = []

            if temp < 0 or temp > 35:
                alert_msgs.append(f"🌡️ Temperature Alert: {temp} °C")
            if ph < 5.5 or ph > 10:
                alert_msgs.append(f"🧪 pH Alert: {ph}")
            if tds > 80:
                alert_msgs.append(f"💧 TDS Alert: {tds} ppm")
            if turb > 33:
                alert_msgs.append(f"🌫️ Turbidity Alert: {turb} NTU")

            if alert_msgs:
                send_email_alert("⚠️ Water Quality Alert", "\n".join(alert_msgs))

        except Exception as e:
            print("❌ Error processing sensor data:", e)

        return jsonify(data)
    return jsonify({})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
