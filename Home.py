import streamlit as st
import folium
from streamlit_folium import st_folium
from timezonefinder import TimezoneFinder

st.set_page_config(page_title="Choisir un lieu", layout="wide")
st.title("🌍 Sélectionnez un lieu")

# Initialisation des variables de session
for key in ["lat", "lon", "timezone", "confirmed_location"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Affichage plein écran de la carte dans une colonne centrale
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    m = folium.Map(location=[48.85, 2.35], zoom_start=3)
    folium.LatLngPopup().add_to(m)
    map_data = st_folium(m, width="100%", height=600)

# Traitement du clic utilisateur
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    tz = TimezoneFinder().timezone_at(lat=lat, lng=lon)

    st.markdown("---")
    st.subheader("📍 Point sélectionné :")
    st.write(f"- Latitude : `{lat:.4f}`")
    st.write(f"- Longitude : `{lon:.4f}`")
    st.write(f"- Fuseau horaire : `{tz}`")

    if st.button("✅ Confirmer ce lieu"):
        st.session_state.lat = lat
        st.session_state.lon = lon
        st.session_state.timezone = tz
        st.session_state.confirmed_location = True

# Bouton de passage à l'étape suivante (si confirmation faite)
if st.session_state.get("confirmed_location"):
    st.success("Lieu confirmé ✅")
    st.markdown("⬇️ Passez à l'étape suivante")
    st.page_link("Date.py", label="➡️ Aller à la sélection de la date", icon="📅")
else:
    st.info("🖱 Cliquez sur la carte puis confirmez le lieu pour continuer.")
