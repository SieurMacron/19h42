import streamlit as st
from timezonefinder import TimezoneFinder
import folium
from streamlit_folium import st_folium

# Initialiser la session si besoin
for key in ["lat", "lon", "timezone", "confirmed_location"]:
    if key not in st.session_state:
        st.session_state[key] = None

st.title("🌍 Choisissez un lieu")

# Carte interactive
m = folium.Map(location=[48.85, 2.35], zoom_start=3)
m.add_child(folium.LatLngPopup())
map_data = st_folium(m, height=400, width=700)

# Réaction au clic sur la carte
if map_data and map_data.get("last_clicked"):
    temp_lat = map_data["last_clicked"]["lat"]
    temp_lon = map_data["last_clicked"]["lng"]
    temp_tz = TimezoneFinder().timezone_at(lat=temp_lat, lng=temp_lon)

    st.markdown("### 📍 Point sélectionné")
    st.write(f"- Latitude : {temp_lat:.4f}")
    st.write(f"- Longitude : {temp_lon:.4f}")
    st.write(f"- Fuseau horaire : {temp_tz}")

    if st.button("✅ Confirmer ce lieu"):
        st.session_state["lat"] = temp_lat
        st.session_state["lon"] = temp_lon
        st.session_state["timezone"] = temp_tz
        st.session_state["confirmed_location"] = True
        st.markdown("✅ Lieu confirmé. Vous pouvez maintenant passer à l'étape suivante.")
        st.markdown("[➡️ Passer à la sélection de la date](Date.py)")
else:
    st.info("🖱 Cliquez sur la carte pour sélectionner un lieu.")
