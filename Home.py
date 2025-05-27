import streamlit as st
import streamlit_folium
from folium import Map
from folium.plugins import MousePosition
from timezonefinder import TimezoneFinder

st.set_page_config(page_title="Sélection du lieu", layout="wide")
st.title("🌍 Sélectionnez un lieu sur la carte")

# Crée une carte centrée sur l'Europe
m = Map(location=[45, 0], zoom_start=3)

# Ajoute les coordonnées en survol de la souris
MousePosition().add_to(m)

# Affiche la carte interactive
map_data = streamlit_folium.st_folium(m, width=1200, height=500)

# Récupère les coordonnées
clicked_latlon = map_data.get("last_clicked")
if clicked_latlon:
    lat, lon = clicked_latlon["lat"], clicked_latlon["lng"]
    st.write(f"📍 Coordonnées sélectionnées : {lat:.4f}, {lon:.4f}")
    
    # Bouton de confirmation
    if st.button("✅ Confirmer ce lieu"):
        tf = TimezoneFinder()
        tz = tf.timezone_at(lat=lat, lng=lon)
        st.session_state.lat = lat
        st.session_state.lon = lon
        st.session_state.timezone = tz or "UTC"
        st.session_state.confirmed_location = True
        st.success(f"Lieu confirmé ! Fuseau horaire : {tz}")
        st.page_link("pages/Date.py", label="➡️ Aller à la sélection de la date", icon="📅")

