import streamlit as st
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
import pytz

st.title("🌞 Heure où le soleil atteint une hauteur spécifique")

if not (st.session_state.get("confirmed_location") and st.session_state.get("confirmed_date")):
    st.warning("Lieu et date doivent être confirmés avant d'accéder à cette page.")
    st.stop()

def hauteur_soleil_patmos():
    patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt_naif = datetime(2023, 8, 1, 19, 42)
    dt = tz.localize(dt_naif)
    return elevation(patmos.observer, dt)

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

hauteur_ref = hauteur_soleil_patmos()

lat = st.session_state.lat
lon = st.session_state.lon
timezone = st.session_state.timezone
date_val = st.session_state.date

heures = heure_qui_atteint_hauteur(lat, lon, date_val, hauteur_ref, timezone)

if not heures:
    st.error("❌ À cette date et à ce lieu, le soleil ne monte pas assez haut dans le ciel.")
else:
    matin = min(heures)
    soir = max(heures)
    st.success(f"🎯 Hauteur de référence : {hauteur_ref:.2f}°")
    st.info(f"🕗 Heure du matin : **{matin.strftime('%H:%M')}**")
    st.info(f"🌇 Heure du soir : **{soir.strftime('%H:%M')}**")
