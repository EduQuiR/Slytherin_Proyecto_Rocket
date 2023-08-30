import requests
import json
from twilio.rest import Client
from models import Contactos

tel=Contactos.query.get(Contactos.e_mail)
TWILIO_ACCOUNT_SID="ACa5fa3d08f59c562d4fb7aca9c8b281cf"
TWILIO_AUTH_TOKEN="aed23df4b6db3474314805cc1eb35197"
TWILIO_PHONE_NUMBER="+15315715022"
RECIPIENT_PHONE_NUMBER="Contactos.e_mail"
def get_location():
    ip=requests.get("https://api.ipify.org").text
    location_url=f"https://ipinfo.io{ip}/json"
    location_response=requests.get(location_url)
    location_data=json.loads(location_response.text)
    if "loc" in location_data:
        latitude,longitude=location_data["loc"].split(",")
        return latitude,longitude
    else:
        return None,None
latitude,longitude=get_location()

if latitude is not None and longitude is not None:
    message=f"mi ubicacion es{latitude},{longitude}"
    google_maps_link=f"https://www.google.com\maps\place\{latitude},{longitude}"

    client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
    client.messages.create(body= f"hola{message},puedes ver mi ubcacion en Google Maps:{google_maps_link}",
    from_=TWILIO_PHONE_NUMBER,
    to=RECIPIENT_PHONE_NUMBER)
    print("el mensaje fue enviado con exito")
else:("error")
