from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import pickle
import time

def save_cookies():
    load_dotenv()
    email = os.getenv("FB_EMAIL")
    password = os.getenv("FB_PASSWORD")

    if not email or not password:
        raise ValueError("FB_EMAIL and FB_PASSWORD must be set in .env")

    chrome_options = Options()
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.facebook.com/login")
        time.sleep(2)

        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        time.sleep(10)

        os.makedirs("cookies", exist_ok=True)
        with open(os.path.join("cookies", "fb_cookies.pkl"), "wb") as f:
            pickle.dump(driver.get_cookies(), f)

        print("Cookies saved to cookies/fb_cookies.pkl")

    except Exception as e:
        print(f"Failed to save cookies: {e}")

    finally:
        driver.quit()
