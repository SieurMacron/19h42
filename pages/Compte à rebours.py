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
st.title(" Compte à rebours jusqu'au prochain 19h42")

# 1. Récupération des coordonnées via navigateur
st.markdown("#### Autorisez le navigateur à accéder à votre position pour continuer.")

# Insertion d’un composant HTML + JS
get_position_code = """
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
"""

position = st.empty()
html(get_position_code, height=0)

# 2. Traitement du message
location_data = st.query_params.get("location_data")


if not location_data:
    # Écoute du message postMessage via JS
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

# 3. Chargement et vérification
try:
    data = json.loads(location_data[0].replace("'", '"'))
    if "error" in data:
        st.error(f"Erreur de géolocalisation : {data['error']}")
        st.stop()
    lat, lon = data["lat"], data["lon"]
    st.success(f"📍 Position détectée : {lat:.4f}, {lon:.4f}")
except Exception as e:
    st.error(f"Erreur de traitement des données de localisation : {e}")
    st.stop()

# 4. Fuseau horaire
tf = TimezoneFinder()
timezone = tf.timezone_at(lat=lat, lng=lon)
if not timezone:
    st.error("Impossible de déterminer le fuseau horaire.")
    st.stop()

# 5. Hauteur de référence
def hauteur_reference_patmos():
    patmos = LocationInfo("Patmos", "Greece", "Europe/Athens", 37.3236, 26.5401)
    tz = pytz.timezone(patmos.timezone)
    dt = tz.localize(datetime(2021, 6, 28, 19, 42))
    return elevation(patmos.observer, dt)

hauteur_ref = hauteur_reference_patmos()

# 6. Recherche des moments dans la journée
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
    st.error("☁️ Le soleil n'atteint pas cette hauteur aujourd’hui à votre position.")
    st.stop()

# 7. Compte à rebours
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
