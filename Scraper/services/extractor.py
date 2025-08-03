import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import requests
import re

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_lat_lng_from_url(url: str) -> str:
    match = re.search(r'@([-.\d]+),([-.\d]+)', url)
    if match:
        lat = match.group(1)
        lng = match.group(2)
        return f"{lat},{lng}"
    return "NA"



def resolve_gmaps_shortlink(short_url):
    try:
        session = requests.Session()
        response = session.head(short_url, allow_redirects=True)
        return response.url
    except Exception as e:
        print("Shortlink resolution failed:", e)
        return short_url  



def get_structured_content(raw_content: str) -> dict:
    prompt = f"""
You are a data extraction assistant.

Extract structured data from the following Facebook rental post. Follow the schema exactly. 
If a value is missing, use "NA". For list fields, return an empty list when missing.

### Content:
\"\"\"{raw_content}\"\"\"

### Schema:
Return your output in this exact JSON format:
{{
  "is_rental_post": "yes/no",
  "apartment_name": "Name of the apartment/society/building, if mentioned",
  "title": "A short title or summary of the post (e.g., 1BHK for rent in Sector 15)",
  "address": "The full address or locality if mentioned",
  "address_google_map_location": "Copy-pasteable location string usable in Google Maps",
  "room_type": "Type of room (1BHK, 2BHK, shared, PG, etc.)",
  "bathroom_type": "Attached, shared, private, etc.",
  "property_type": "Apartment, flat, PG, hostel, independent house, etc.",
  "furnishing": "Furnished, semi-furnished, unfurnished",
  "gated": "Yes/No/NA — is it in a gated society?",
  "rent": "Monthly rent in INR",
  "deposit": "Security deposit in INR",
  "availability": "When is the property available (e.g. Immediate, from 1st Sept, etc.)",
  "phone": "Phone number(s) mentioned",
  "for_whom": "Who it's suitable for (e.g. Girls, Boys, Family, Working professionals)",
  "nearby_places": ["Landmarks, colleges, IT parks, metro stations, etc."],
  "highlights": ["Key selling points mentioned — like north-facing, newly renovated, etc."],
  "amenities": ["Amenities like WiFi, fridge, AC, power backup, etc."],
  "safety_note": "Any safety-related info (e.g., CCTV, guard available)",
  "nearby_police_station": "If mentioned, else NA",
  "metro_connectivity": "Mention nearby metro stations or distance to metro",
  "bus_connectivity": "Mention nearby bus stops or routes",
  "taxi_connectivity": "Mention if Ola/Uber/auto availability is discussed"
}}

Only return a valid JSON. No extra explanation, no markdown.
"""

    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        start = text_response.find('{')
        end = text_response.rfind('}') + 1
        json_string = text_response[start:end]
        
        data = json.loads(json_string)

        if data.get("is_rental_post", "").lower() != "yes":
            return {"error": "Not a rental-related post."}
        map_link = data.get("address_google_map_location", "")
        if "maps.app.goo.gl" in map_link:
            raw_location = resolve_gmaps_shortlink(map_link)
            data["address_google_map_location"] = extract_lat_lng_from_url(raw_location)

        return data

    except Exception as e:
        print("Gemini Error:", e)
        return {
            "is_rental_post": "no",
            "apartment_name": "NA",
            "title": "NA",
            "address": "NA",
            "address_google_map_location": "NA",
            "room_type": "NA",
            "bathroom_type": "NA",
            "property_type": "NA",
            "furnishing": "NA",
            "gated": "NA",
            "rent": "NA",
            "deposit": "NA",
            "availability": "NA",
            "phone": "NA",
            "for_whom": "NA",
            "nearby_places": [],
            "highlights": [],
            "amenities": [],
            "safety_note": "NA",
            "nearby_police_station": "NA",
            "metro_connectivity": "NA",
            "bus_connectivity": "NA",
            "taxi_connectivity": "NA"
        }
