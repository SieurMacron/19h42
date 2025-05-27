import streamlit as st
import streamlit_folium
from folium import Map
from folium.plugins import MousePosition
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Sélection du lieu", layout="wide")
st.title("Claire = prout")

geolocator = Nominatim(user_agent="sun_position_app")
tf = TimezoneFinder()

# Détection par recherche texte
st.subheader("🔎 Rechercher un lieu")
place_name = st.text_input("Entrez un nom de lieu (ville, pays, etc.)")

if place_name:
    location = geolocator.geocode(place_name)
    if location:
        st.success(f"Lieu trouvé : {location.address}")
        st.write(f"📍 Coordonnées : {location.latitude:.4f}, {location.longitude:.4f}")
        if st.button("✅ Confirmer ce lieu (recherche)"):
            tz = tf.timezone_at(lat=location.latitude, lng=location.longitude)
            st.session_state.lat = location.latitude
            st.session_state.lon = location.longitude
            st.session_state.timezone = tz or "UTC"
            st.session_state.confirmed_location = True
            st.success(f"Lieu confirmé ! Fuseau horaire : {tz}")
    else:
        st.error("❌ Lieu non trouvé. Veuillez réessayer.")

# OU bien sélection par carte
st.subheader("🗺️ Ou cliquez sur la carte")
col1, col2 = st.columns([3, 1])

with col1:
    m = Map(location=[45, 0], zoom_start=3)
    MousePosition().add_to(m)
    map_data = streamlit_folium.st_folium(m, width=700, height=450)

with col2:
    clicked_latlon = map_data.get("last_clicked")
    if clicked_latlon:
        lat, lon = clicked_latlon["lat"], clicked_latlon["lng"]
        st.write(f"📍 Coordonnées sélectionnées : {lat:.4f}, {lon:.4f}")
        if st.button("✅ Confirmer ce lieu (carte)"):
            tz = tf.timezone_at(lat=lat, lng=lon)
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.timezone = tz or "UTC"
            st.session_state.confirmed_location = True
            st.success(f"Lieu confirmé ! Fuseau horaire : {tz}")
    else:
        st.info("Cliquez sur la carte pour sélectionner un lieu.")

# Message de rappel
if not st.session_state.get("confirmed_location", False):
    st.info("Veuillez confirmer un lieu via la carte ou la recherche.")
