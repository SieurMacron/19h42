import streamlit as st
import streamlit_folium
from folium import Map
from folium.plugins import MousePosition
from timezonefinder import TimezoneFinder

st.set_page_config(page_title="Sélection du lieu", layout="wide")
st.title("🌍 Sélectionnez un lieu sur la carte")

# Container carte + bouton
with st.container():
    m = Map(location=[45, 0], zoom_start=3)
    MousePosition().add_to(m)

    map_data = streamlit_folium.st_folium(m, width=900, height=450)

    clicked_latlon = map_data.get("last_clicked")

    if clicked_latlon:
        lat, lon = clicked_latlon["lat"], clicked_latlon["lng"]
        st.write(f"📍 Coordonnées sélectionnées : {lat:.4f}, {lon:.4f}")

        if st.button("✅ Confirmer ce lieu"):
            tf = TimezoneFinder()
            tz = tf.timezone_at(lat=lat, lng=lon)
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.timezone = tz or "UTC"
            st.session_state.confirmed_location = True
            st.success(f"Lieu confirmé ! Fuseau horaire : {tz}")

# Plus de lien pour aller à Date
if not st.session_state.get("confirmed_location", False):
    st.info("Veuillez sélectionner un lieu sur la carte et confirmer.")
