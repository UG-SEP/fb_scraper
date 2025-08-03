from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
import os
from ..save_cookies import save_cookies

COOKIE_PATH = os.path.join("cookies", "fb_cookies.pkl")

def load_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    chrome_options.add_argument("window-size=1920x1080")
    return webdriver.Chrome(options=chrome_options)

def apply_cookies(driver):
    with open(COOKIE_PATH, "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        cookie.pop('sameSite', None)
        try:
            driver.add_cookie(cookie)
        except:
            continue

def scrape_facebook_post(url):
    if not os.path.exists(COOKIE_PATH):
        print("Cookies not found, triggering save_cookies()...")
        save_cookies()
        if not os.path.exists(COOKIE_PATH):
            raise Exception("Failed to save Facebook cookies automatically.")

    driver = load_driver()
    driver.get("https://www.facebook.com/")
    time.sleep(3)
    apply_cookies(driver)
    driver.get(url)
    time.sleep(4)

    try:
        content = driver.find_element(By.XPATH, '(//div[@data-ad-preview="message"])[last()]').text
    except Exception as e:
        content = f"Failed to extract content: {e}"

    image_urls = []
    try:
        post_id = url.strip("/").split("/")[-1]
        anchors = driver.find_elements(By.XPATH, f'//a[contains(@href, "{post_id}")]')
        for a in anchors:
            try:
                img = a.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")
                if src and "scontent" in src:
                    image_urls.append(src)
            except:
                continue
        if not image_urls:
            imgs = driver.find_elements(By.XPATH, '//img[contains(@src, "scontent")]')
            image_urls = list(set(img.get_attribute("src") for img in imgs if img.get_attribute("src")))
    except Exception as e:
        print(f"Error extracting images: {e}")

    driver.quit()

    return {
        "content": content,
        "images": image_urls
    }
