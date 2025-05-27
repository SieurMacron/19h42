import streamlit as st
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
from timezonefinder import TimezoneFinder
import pytz
from streamlit_folium import st_folium
import folium

# Calcul de la hauteur du soleil à Patmos
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

# --- Interface utilisateur ---
st.title("À quelle heure le soleil atteint une certaine hauteur ?")
hauteur_ref = hauteur_soleil_patmos()
st.markdown(f"🌞 Hauteur de référence (Patmos, 1er août à 19h42) : **{hauteur_ref:.2f}°**")

st.markdown("### 🌍 Sélectionnez un lieu sur la carte")

# Crée une carte avec pop-up lat/lon au clic
m = folium.Map(location=[48.85, 2.35], zoom_start=3)
m.add_child(folium.LatLngPopup())  # <-- Active le clic et la récupération de coordonnées

# Affiche la carte
map_data = st_folium(m, height=400, width=700)


if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # Trouver automatiquement le fuseau horaire
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=lat, lng=lon)

    st.success(f"Coordonnées sélectionnées : lat={lat:.4f}, lon={lon:.4f}")
    st.success(f"Fuseau horaire détecté : {timezone}")

    date_input = st.date_input("📅 Sélectionnez une date", value=datetime.now().date())

    if st.button("Calculer l’heure à laquelle le soleil atteint cette hauteur"):
        try:
            heures = heures_qui_atteignent_hauteur(lat, lon, date_input, hauteur_ref, timezone)
            if heures:
                st.success("🕒 Heures où le soleil atteint la hauteur :")
                for i, h in enumerate(heures, 1):
                    st.write(f"**{i}.** {h.strftime('%H:%M')} ({timezone})")
            else:
                st.warning("Le soleil n’atteint pas cette hauteur ce jour-là à ce lieu.")
        except Exception as e:
            st.error(f"Erreur : {e}")
else:
    st.info("Cliquez sur la carte pour choisir une position.")

