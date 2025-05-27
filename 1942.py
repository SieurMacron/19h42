import streamlit as st
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
from timezonefinder import TimezoneFinder
import pytz
from streamlit_folium import st_folium
import folium
import time

# ---- Initialisation session_state ----
for key in ["lat", "lon", "timezone", "date", "confirmed_location", "confirmed_date"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---- Page 1 : sélection du lieu ----
if st.session_state.lat is None:
    st.title("🌍 Choisissez un lieu")

    m = folium.Map(location=[48.85, 2.35], zoom_start=3)
    m.add_child(folium.LatLngPopup())
    map_data = st_folium(m, height=400, width=700)

    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=lat, lng=lon)

        st.session_state["lat"] = lat
        st.session_state["lon"] = lon
        st.session_state["timezone"] = timezone

        st.success(f"Vous avez sélectionné :\n- Latitude : {lat:.4f}\n- Longitude : {lon:.4f}\n- Fuseau : {timezone}")

        if st.button("✅ Confirmer ce lieu"):
            st.session_state.confirmed_location = True
            # Effet fondu : écran noir simulé
            with st.empty():
                st.markdown("<div style='background-color:black;height:400px'></div>", unsafe_allow_html=True)
                time.sleep(1)
            st.experimental_rerun()

# ---- Page 2 : sélection de la date ----
elif st.session_state.date is None:
    st.title("📅 Choisissez une date")
    date = st.date_input("Sélectionnez une date", min_value=datetime(2022,1,1).date())
    if st.button(f"✅ Confirmer la date {date}"):
        st.session_state["date"] = date
        st.session_state.confirmed_date = True
        # Effet fondu : écran noir simulé
        with st.empty():
            st.markdown("<div style='background-color:black;height:400px'></div>", unsafe_allow_html=True)
            time.sleep(1)
        st.experimental_rerun()

# ---- Page 3 : résultat ----
else:
    st.title("🕒 Résultat")

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

    st.success(f"📍 Lieu : {st.session_state.lat:.4f}, {st.session_state.lon:.4f} ({st.session_state.timezone})")
    st.success(f"📅 Date : {st.session_state.date}")

    hauteur_ref = hauteur_soleil_patmos()
    heures = heures_qui_atteignent_hauteur(
        st.session_state.lat,
        st.session_state.lon,
        st.session_state.date,
        hauteur_ref,
        st.session_state.timezone
    )

    if heures:
        st.markdown(f"🌞 Le soleil atteindra **{hauteur_ref:.2f}°** à ces heures :")
        for h in heures:
            st.write(f"→ {h.strftime('%H:%M')} ({st.session_state.timezone})")
    else:
        st.warning("Le soleil n’atteint pas cette hauteur ce jour-là à ce lieu.")

    # Option de recommencer
    if st.button("🔄 Recommencer"):
        for key in ["lat", "lon", "timezone", "date", "confirmed_location", "confirmed_date"]:
            st.session_state[key] = None
        st.experimental_rerun()
