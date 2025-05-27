import streamlit as st
from astral import LocationInfo
from astral.sun import elevation
from datetime import datetime, timedelta
import pytz

st.set_page_config(page_title="Résultat", page_icon="🌞")

if not all(st.session_state.get(k) for k in ["lat", "lon", "timezone", "selected_date"]):
    st.error("⛔ Lieu ou date manquants.")
    st.stop()

# Fonction 1 : hauteur du soleil de référence
def hauteur_soleil_patmos():
    patmos = LocationInfo(name="Patmos", region="Greece", timezone="Europe/Athens",
                          latitude=37.3236, longitude=26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt = tz.localize(datetime(2023, 8, 1, 19, 42))
    return elevation(patmos.observer, dt)

# Fonction 2 : trouver les heures où le soleil atteint la hauteur
def heures_hauteur(lat, lon, date, hauteur_cible, timezone_str):
    loc = LocationInfo(latitude=lat, longitude=lon, timezone=timezone_str)
    tz = pytz.timezone(timezone_str)
    dt_start = tz.localize(datetime(date.year, date.month, date.day))
    dt_end = dt_start + timedelta(days=1)

    delta = timedelta(minutes=1)
    heures = []

    dt = dt_start
    while dt <= dt_end:
        elev = elevation(loc.observer, dt)
        if abs(elev - hauteur_cible) < 0.1:
            heures.append(dt)
        dt += delta

    return heures

# Execution
hauteur_ref = hauteur_soleil_patmos()
heures = heures_hauteur(
    st.session_state.lat,
    st.session_state.lon,
    st.session_state.selected_date,
    hauteur_ref,
    st.session_state.timezone
)

st.title("🕓 Heure où le soleil atteint la hauteur cible")

if heures:
    matin = min(heures).strftime("%H:%M")
    soir = max(heures).strftime("%H:%M")
    st.success(f"Hauteur atteinte à {matin} et à {soir} ({st.session_state.timezone})")
else:
    st.warning("Le soleil n’atteint pas cette hauteur à cette date/lieu.")
