from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Inisialisasi scheduler untuk mengirim email sesuai jadwal
scheduler = BackgroundScheduler()

# Simulasi penyimpanan harapan (dalam praktik nyata bisa menggunakan database)
hopes = []

# Fungsi untuk mengirim email
def send_email(to_email, subject, body):
    from_email = "youremail@example.com"
    from_password = "yourpassword"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Fungsi untuk memeriksa dan mengirim email sesuai jadwal
def check_and_send_hopes():
    today = datetime.date.today().strftime("%Y-%m-%d")
    for hope in hopes:
        if hope['date'] == today:
            send_email(hope['email'], "Your Hope for Today", hope['hope'])

# Mengatur scheduler untuk memeriksa harapan setiap hari
scheduler.add_job(check_and_send_hopes, 'interval', days=1)
scheduler.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hope', methods=['GET', 'POST'])
def hope():
    if request.method == 'POST':
        hope_text = request.form['hope']
        email = request.form['email']
        date = request.form['date']
        hopes.append({'hope': hope_text, 'email': email, 'date': date})
        return redirect(url_for('list_hope'))
    return render_template('hope.html')

@app.route('/list_hope')
def list_hope():
    return render_template('list_hope.html', hopes=hopes)

if __name__ == '__main__':
    app.run(debug=True)
