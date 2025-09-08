from flask import Flask, render_template, request
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message_status = ""
    if request.method == 'POST':
        file = request.files['csv_file']
        if file:
            contacts = pd.read_csv(file)
            message_status = send_messages(contacts)
    return render_template('index.html', status=message_status)

def send_messages(contacts):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # لتشغيل بدون واجهة رسومية (اختياري)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")
    print("امسح QR Code لتسجيل الدخول...")
    time.sleep(15)  # وقت لمسح QR Code

    success = 0
    fail = 0

    for index, contact in contacts.iterrows():
        number = contact['Number']
        message = contact['Message']
        url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
        driver.get(url)
        time.sleep(10)
        try:
            send_btn = driver.find_element(By.XPATH, '//button[@data-testid="compose-btn-send"]')
            send_btn.click()
            success += 1
            time.sleep(5)
        except:
            fail += 1

    driver.quit()
    return f"تم إرسال {success} رسالة، وفشل {fail} رسالة."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
