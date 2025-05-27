import streamlit as st
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
import pytz

st.set_page_config(page_title="Résultat", layout="centered")
st.title("🌞 La belle lumière de 19h42 sera atteinte...🌞")

# Vérification des données nécessaires
if not (st.session_state.get("confirmed_location") and st.session_state.get("confirmed_date")):
    st.warning("Lieu et date doivent être confirmés avant d'accéder à cette page.")
    st.stop()

# Hauteur du soleil à Patmos le 1er août à 19h42
def hauteur_soleil_patmos():
    patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt_naif = datetime(2023, 8, 1, 19, 42)
    dt = tz.localize(dt_naif)
    return elevation(patmos.observer, dt)

hauteur_ref = hauteur_soleil_patmos()

# Recherche des heures où le soleil atteint cette hauteur
def heure_qui_atteint_hauteur(lat, lon, date, hauteur_cible, timezone_str):
    loc = LocationInfo(latitude=lat, longitude=lon, timezone=timezone_str)
    tz = pytz.timezone(timezone_str)
    dt_start = tz.localize(datetime(date.year, date.month, date.day, 0, 0))
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

# Récupération des données depuis la session
lat = st.session_state.lat
lon = st.session_state.lon
timezone = st.session_state.timezone
date_val = st.session_state.selected_date

heures = heure_qui_atteint_hauteur(lat, lon, date_val, hauteur_ref, timezone)

# Affichage du résultat
if not heures:
    st.error("❌ À cette date et à ce lieu, le soleil ne monte pas assez haut dans le ciel.")
else:
    matin = min(heures)
    soir = max(heures)
    st.info(f"🕗 Le matin, à **{matin.strftime('%H:%M')}**")
    st.info(f"🌇 Le soir, à **{soir.strftime('%H:%M')}**")
