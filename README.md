# Facebook Post Scraper 🕵️‍♂️

A Django-based scraper that extracts content and images from public Facebook posts using Selenium, and analyzes the post using Gemini API.

---

## ⚙️ Features

- Headless Selenium browser scraping  
- Login using Facebook credentials (cookies-based)  
- Gemini API-powered content extraction  
- Rental post detection  
- Django web interface  

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/UG-SEP/fb_scraper.git
cd fb_scraper
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

---

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

### 4. Setup `.env` File

Create a `.env` file in the root directory and add the following environment variables:

```env
FB_EMAIL=your_facebook_email
FB_PASSWORD=your_facebook_password
GEMINI_API_KEY=your_gemini_api_key
```

---


### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit [http://localhost:8000/scraper](http://localhost:8000/scraper)

---

## 📌 Notes

- Ensure that Chrome is installed and your `chromedriver` version matches it.
- This project scrapes **public** Facebook posts only.
- `extractor.py` uses Gemini to identify if a post is a rental. If not, it skips irrelevant details.

---

## 🧠 Tech Stack

- Django  
- Selenium  
- Gemini API (Google AI)  
- HTML/CSS (minimal UI)  

---
