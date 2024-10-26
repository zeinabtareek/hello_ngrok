import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract
from flask import Flask, jsonify
from flask_cors import CORS  # إضافة مكتبة CORS

app = Flask(__name__)
CORS(app)  # السماح بالوصول من جميع المصادر
app.secret_key = "MMM123MMM@mmm"

# Function to extract CAPTCHA text
def extract_and_submit_captcha(driver):
    # Wait for the CAPTCHA element to load
    captcha_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'captchaimg'))  # Use actual CAPTCHA element ID
    )
    # Take a screenshot of the CAPTCHA
    captcha_screenshot_path = 'captcha_screenshot.png'
    captcha_element.screenshot(captcha_screenshot_path)

    # Use OCR to extract the CAPTCHA text
    captcha_image = Image.open(captcha_screenshot_path)
    captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 8').strip()
    print(f"Extracted CAPTCHA text: {captcha_text}")
    return captcha_text

@app.route('/solve-captcha', methods=['GET'])
def solve_captcha():
    # Example usage
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.iobnet.co.in/ibanking/corplogin.do')

    # Try solving CAPTCHA
    captcha_text = extract_and_submit_captcha(driver)

    # Enter CAPTCHA and login info, then submit
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'loginsubmit_captchaid'))
    ).send_keys(captcha_text)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'loginsubmit_loginId'))
    ).send_keys('Nariox708')

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'loginsubmit_userId'))
    ).send_keys('Nariox7')

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'password'))
    ).send_keys('Abcd@1234')

    # Submit the form
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'btnSubmit'))
    ).click()

    driver.quit()

    return jsonify({'captcha': captcha_text})

if __name__ == '__main__':
    app.run(debug=True)
