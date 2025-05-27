import streamlit as st
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
import pytz
import time

st.set_page_config(page_title="Compte à rebours solaire", layout="centered")
st.title("🔍 Compte à rebours solaire par lieu")

# Entrée utilisateur pour chercher un lieu
lieu = st.text_input("Entrez une ville ou un lieu :")

if lieu:
    geolocator = Nominatim(user_agent="sun_countdown_app")
    location = geolocator.geocode(lieu)
    if not location:
        st.error("❌ Lieu introuvable. Essayez un autre nom.")
        st.stop()

    lat, lon = location.latitude, location.longitude
    st.success(f"📍 Lieu trouvé : {location.address} ({lat:.4f}, {lon:.4f})")

    # Fuseau horaire
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=lat, lng=lon)
    if not timezone:
        st.error("❌ Impossible de déterminer le fuseau horaire.")
        st.stop()

    # Hauteur de référence à Patmos
    def hauteur_reference_patmos():
        patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
        tz = pytz.timezone(patmos.timezone)
        dt = tz.localize(datetime(2021, 6, 28, 19, 42))
        return elevation(patmos.observer, dt)

    hauteur_ref = hauteur_reference_patmos()

    # Heures de la journée atteignant la hauteur de référence
    def heures_hauteur_aujourdhui(lat, lon, timezone_str, hauteur_cible):
        loc = LocationInfo(latitude=lat, longitude=lon, timezone=timezone_str)
        tz = pytz.timezone(timezone_str)
        date_now = datetime.now(tz).date()
        dt_start = tz.localize(datetime.combine(date_now, datetime.min.time()))
        dt_end = dt_start + timedelta(days=1)

        heures_valides = []
        dt = dt_start
        delta = timedelta(minutes=1)
        while dt <= dt_end:
            elev = elevation(loc.observer, dt)
            if abs(elev - hauteur_cible) < 0.1:
                heures_valides.append(dt)
            dt += delta
        return heures_valides

    heures = heures_hauteur_aujourdhui(lat, lon, timezone, hauteur_ref)
    now = datetime.now(pytz.timezone(timezone))
    prochaine_heure = next((h for h in heures if h > now), None)

    if not prochaine_heure:
        st.error("☁️ Le soleil n'atteint pas cette hauteur aujourd’hui.")
        st.stop()

    # Affichage du compte à rebours
    st.success(f"🎯 Hauteur de référence : {hauteur_ref:.2f}°")
    st.info(f"🕒 Prochaine occurrence : {prochaine_heure.strftime('%H:%M:%S')} ({timezone})")

    countdown = st.empty()
    while True:
        now = datetime.now(pytz.timezone(timezone))
        delta = prochaine_heure - now
        if delta.total_seconds() <= 0:
            countdown.success("☀️ Le soleil est à la hauteur cible !")
            break
        countdown.markdown(f"## ⏳ Temps restant : `{str(delta).split('.')[0]}`")
        time.sleep(1)
else:
    st.info("🔎 Veuillez entrer un lieu pour démarrer.")
