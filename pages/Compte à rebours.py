import streamlit as st
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
import pytz
import time

st.set_page_config(page_title="Compte à rebours solaire", layout="centered")
st.title("⏳ Compte à rebours jusqu'à la hauteur solaire")

# Vérifier les données requises
if not st.session_state.get("confirmed_location"):
    st.warning("Vous devez d'abord confirmer un lieu.")
    st.stop()

# --------------------
# 1. Hauteur de référence à Patmos le 28 juin 2021 à 19h42
# --------------------
def hauteur_reference_patmos():
    patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt = tz.localize(datetime(2021, 6, 28, 19, 42))
    return elevation(patmos.observer, dt)

hauteur_ref = hauteur_reference_patmos()

# --------------------
# 2. Calcul des heures où cette hauteur est atteinte aujourd'hui à la position de l'utilisateur
# --------------------
def heures_hauteur_cible_aujourdhui(lat, lon, timezone_str, hauteur_cible):
    loc = LocationInfo(latitude=lat, longitude=lon, timezone=timezone_str)
    tz = pytz.timezone(timezone_str)
    date_now = datetime.now(tz).date()
    dt_start = tz.localize(datetime(date_now.year, date_now.month, date_now.day, 0, 0))
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

lat = st.session_state.lat
lon = st.session_state.lon
timezone = st.session_state.timezone

heures = heures_hauteur_cible_aujourdhui(lat, lon, timezone, hauteur_ref)

# --------------------
# 3. Trouver le prochain passage
# --------------------
now = datetime.now(pytz.timezone(timezone))
prochaine_heure = next((h for h in heures if h > now), None)

if not prochaine_heure:
    st.error("🌥️ Aujourd’hui, le soleil ne passe pas par cette hauteur.")
else:
    st.success(f"🎯 Hauteur solaire cible : {hauteur_ref:.2f}°")
    st.info(f"📍 Prochaine occurrence : {prochaine_heure.strftime('%H:%M:%S')}")

    # --------------------
    # 4. Affichage du compte à rebours
    # --------------------
    countdown_placeholder = st.empty()

    while True:
        now = datetime.now(pytz.timezone(timezone))
        delta = prochaine_heure - now

        if delta.total_seconds() <= 0:
            countdown_placeholder.success("☀️ Le soleil a atteint la hauteur cible !")
            break

        countdown_str = str(delta).split(".")[0]  # format hh:mm:ss
        countdown_placeholder.markdown(f"## ⏳ Temps restant : `{countdown_str}`")
        time.sleep(1)
