import streamlit as st
import folium
from streamlit_folium import st_folium
from timezonefinder import TimezoneFinder

st.set_page_config(page_title="Choix du lieu", page_icon="🌍")

st.title("🌍 Choisissez un lieu")

# Session init
for key in ["lat", "lon", "timezone", "confirmed_location"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Carte interactive
m = folium.Map(location=[48.85, 2.35], zoom_start=3)
m.add_child(folium.LatLngPopup())
map_data = st_folium(m, height=400)

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    tz = TimezoneFinder().timezone_at(lat=lat, lng=lon)

    st.markdown(f"### Point sélectionné :\n- Latitude : {lat:.4f}\n- Longitude : {lon:.4f}\n- Fuseau horaire : `{tz}`")

    if st.button("✅ Confirmer ce lieu"):
        st.session_state.lat = lat
        st.session_state.lon = lon
        st.session_state.timezone = tz
        st.session_state.confirmed_location = True
        st.success("Lieu confirmé ✅")
        st.markdown("[➡️ Passer à la sélection de la date](Date)")

else:
    st.info("🖱 Cliquez sur la carte pour sélectionner un point.")
