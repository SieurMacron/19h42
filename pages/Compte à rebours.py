import streamlit as st
from streamlit.components.v1 import html
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
from timezonefinder import TimezoneFinder
import pytz
import time
import json

st.set_page_config(page_title="Compte à rebours solaire", layout="centered")
st.title("📍 Compte à rebours basé sur votre position")

# Étape 1 – Bouton pour déclencher la géolocalisation
if "geoloc_triggered" not in st.session_state:
    st.session_state.geoloc_triggered = False

if not st.session_state.geoloc_triggered:
    if st.button("📍 Utiliser ma position actuelle"):
        st.session_state.geoloc_triggered = True
        html("""
        <script>
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const coords = {
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude
                };
                window.parent.postMessage(JSON.stringify(coords), "*");
            },
            (err) => {
                const error = { error: err.message };
                window.parent.postMessage(JSON.stringify(error), "*");
            }
        );
        </script>
        """, height=0)
        html("""
        <script>
        window.addEventListener("message", (event) => {
            const data = JSON.stringify(event.data);
            const url = new URL(window.location.href);
            url.searchParams.set("location_data", data);
            window.location.href = url.href;
        });
        </script>
        """, height=0)
        st.stop()

# Étape 2 – Récupération des données de position
location_data = st.query_params.get("location_data")
if not location_data:
    st.info("Cliquez sur le bouton pour autoriser la géolocalisation.")
    st.stop()

# Étape 3 – Traitement
try:
    data = json.loads(location_data[0].replace("'", '"'))
    if "error" in data:
        st.error(f"Erreur de géolocalisation : {data['error']}")
        st.stop()
    lat, lon = data["lat"], data["lon"]
    st.success(f"📍 Position détectée : {lat:.4f}, {lon:.4f}")
except Exception as e:
    st.error(f"Erreur de traitement : {e}")
    st.stop()

# Fuseau horaire
tf = TimezoneFinder()
timezone = tf.timezone_at(lat=lat, lng=lon)
if not timezone:
    st.error("Impossible de déterminer le fuseau horaire.")
    st.stop()

# Hauteur de référence
def hauteur_reference_patmos():
    patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt = tz.localize(datetime(2021, 6, 28, 19, 42))
    return elevation(patmos.observer, dt)

hauteur_ref = hauteur_reference_patmos()

# Recherche des heures valides
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

# Compte à rebours
st.success(f"🎯 Hauteur solaire cible : {hauteur_ref:.2f}°")
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
