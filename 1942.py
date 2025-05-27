import streamlit as st
from astral import LocationInfo
from astral.sun import elevation
from datetime import datetime, timedelta
import pytz

@st.cache_data
def hauteur_soleil_patmos():
    patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt = tz.localize(datetime(2023, 8, 1, 19, 42))
    return elevation(patmos.observer, dt)

def heures_qui_atteignent_hauteur(lat, lon, date, hauteur_cible, timezone_str):
    loc = LocationInfo(latitude=lat, longitude=lon, timezone=timezone_str)
    tz = pytz.timezone(timezone_str)
    dt_start = tz.localize(datetime(date.year, date.month, date.day))
    dt_end = dt_start + timedelta(days=1)

    heures_valides = []
    dt = dt_start
    while dt <= dt_end:
        elev = elevation(loc.observer, dt)
        if elev > 0 and abs(elev - hauteur_cible) < 0.1:
            if not heures_valides or (dt - heures_valides[-1]) > timedelta(minutes=5):
                heures_valides.append(dt)
        dt += timedelta(minutes=1)

    return heures_valides

# --- Interface Streamlit ---
st.title("À quelle heure le soleil atteint une certaine hauteur ?")

st.markdown("La hauteur de référence est celle atteinte à **Patmos** (Grèce), le 1er août à 19h42.")
hauteur_ref = hauteur_soleil_patmos()
st.write(f"Hauteur de référence : **{hauteur_ref:.2f}°**")

latitude = st.number_input("Latitude", value=48.8566)
longitude = st.number_input("Longitude", value=2.3522)
date_input = st.date_input("Date", value=datetime.now().date())
timezone_str = st.text_input("Fuseau horaire (ex: Europe/Paris)", value="Europe/Paris")

if st.button("Calculer"):
    try:
        heures = heures_qui_atteignent_hauteur(latitude, longitude, date_input, hauteur_ref, timezone_str)
        if heures:
            st.success("Heures où le soleil atteint la hauteur de référence :")
            for i, h in enumerate(heures, 1):
                st.write(f"**{i}.** {h.strftime('%H:%M')} ({timezone_str})")
        else:
            st.warning("Le soleil n'atteint pas cette hauteur ce jour-là à ce lieu.")
    except Exception as e:
        st.error(f"Erreur : {e}")
