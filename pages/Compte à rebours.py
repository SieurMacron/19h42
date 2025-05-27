import streamlit as st
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
import pytz
import time

st.set_page_config(page_title="Compte à rebours solaire", layout="centered")
st.title("⏳ Compte à rebours solaire")

# Entrée utilisateur
st.subheader("🔍 Choisissez un lieu")
lieu_input = st.text_input("Ville ou lieu :", value=st.session_state.get("lieu_nom", ""))

# Fonction pour calculer la hauteur à Patmos (28 juin 2021 à 19h42)
def hauteur_reference_patmos():
    patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt = tz.localize(datetime(2021, 6, 28, 19, 42))
    return elevation(patmos.observer, dt)

hauteur_ref = hauteur_reference_patmos()

# Si l'utilisateur entre un lieu et qu'on ne l'a pas encore enregistré ou qu'il a changé
if lieu_input and (lieu_input != st.session_state.get("lieu_nom", "")):
    geolocator = Nominatim(user_agent="sun_countdown_app")
    location = geolocator.geocode(lieu_input)

    if not location:
        st.error("❌ Lieu introuvable.")
        st.stop()

    lat, lon = location.latitude, location.longitude
    tf = TimezoneFinder()
    tz = tf.timezone_at(lat=lat, lng=lon)

    if not tz:
        st.error("❌ Fuseau horaire introuvable.")
        st.stop()

    # Sauvegarde dans la session
    st.session_state.lieu_nom = lieu_input
    st.session_state.lat = lat
    st.session_state.lon = lon
    st.session_state.tz = tz
    st.success(f"📍 Lieu enregistré : {location.address} ({lat:.4f}, {lon:.4f})")

# Si on a déjà une position en session
if all(k in st.session_state for k in ("lat", "lon", "tz")):
    lat = st.session_state.lat
    lon = st.session_state.lon
    tz = st.session_state.tz

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

    heures = heures_hauteur_aujourdhui(lat, lon, tz, hauteur_ref)
    now = datetime.now(pytz.timezone(tz))
    prochaine_heure = next((h for h in heures if h > now), None)

    if not prochaine_heure:
        st.error("☁️ Le soleil n'atteint pas cette hauteur aujourd’hui.")
        st.stop()

    st.success(f"🎯 Hauteur de référence : {hauteur_ref:.2f}°")
    st.info(f"🕒 Prochaine occurrence : {prochaine_heure.strftime('%H:%M:%S')} ({tz})")

    countdown = st.empty()
    while True:
        now = datetime.now(pytz.timezone(tz))
        delta = prochaine_heure - now
        if delta.total_seconds() <= 0:
            countdown.success("☀️ Le soleil est à la hauteur cible !")
            break
        countdown.markdown(f"## ⏳ Temps restant : `{str(delta).split('.')[0]}`")
        time.sleep(1)
else:
    st.info("Veuillez saisir un lieu pour démarrer.")
