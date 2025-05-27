import streamlit as st
from streamlit_js_eval import get_window_size
import pydeck as pdk
from geopy.geocoders import Nominatim

# Init session_state variables
if "selected_coords" not in st.session_state:
    st.session_state.selected_coords = None
if "selected_place" not in st.session_state:
    st.session_state.selected_place = None

st.title("🌍 Sélectionnez un lieu")

window_size = get_window_size()
width = window_size.get("width", 1000)

if width >= 768:
    st.write("💻 Mode Desktop — sélection via carte interactive")

    # Carte pydeck interactive
    initial_view = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1.5,
        pitch=0,
    )
    r = pdk.Deck(
        initial_view_state=initial_view,
        layers=[],
        map_style="mapbox://styles/mapbox/light-v9",
        tooltip={"text": "Cliquez pour sélectionner un point"},
        mapbox_key="YOUR_MAPBOX_ACCESS_TOKEN"  # remplace par ta clé si besoin
    )

    # Affiche la carte et récupère le clic
    selected = st.pydeck_chart(r)

    # Utilise st.pydeck_chart pour récupérer les clics (en mode carte seule, pas trivial)
    # Alternative : pydeck ne retourne pas l'événement clic directement
    # On peut utiliser st.map avec st_click ou un composant tiers pour capter le clic
    # Pour simplifier, remplaçons par un widget st.map avec selection manuelle

    coords = st.experimental_data_editor([], num_rows=1, key="coords_editor")
    # Ou simplement demander à l'utilisateur de cliquer sur la carte externe

    # Solution pratique :
    latitude = st.number_input("Latitude sélectionnée", value=20.0, format="%.6f")
    longitude = st.number_input("Longitude sélectionnée", value=0.0, format="%.6f")

    if st.button("Confirmer la sélection"):
        st.session_state.selected_coords = (latitude, longitude)
        st.success(f"Lieu sélectionné : lat {latitude}, lon {longitude}")

else:
    st.write("📱 Mode Mobile — sélection via barre de recherche")

    geolocator = Nominatim(user_agent="my_streamlit_app")

    lieu_cherche = st.text_input("Recherchez un lieu (ex: Paris, France)")

    if lieu_cherche:
        location = geolocator.geocode(lieu_cherche)
        if location:
            st.write(f"Résultat : {location.address}")
            st.write(f"Coordonnées : {location.latitude:.6f}, {location.longitude:.6f}")

            if st.button("Confirmer la sélection"):
                st.session_state.selected_coords = (location.latitude, location.longitude)
                st.session_state.selected_place = location.address
                st.success("Lieu confirmé !")
        else:
            st.error("Lieu non trouvé, essayez une autre recherche.")

# Bouton pour aller à la page suivante uniquement si un lieu est sélectionné
if st.session_state.selected_coords:
    if st.button("➡️ Aller à la sélection de la date"):
        st.session_state.page = "date_selection"  # À gérer selon ta navigation
        st.experimental_rerun()
else:
    st.info("Veuillez sélectionner un lieu et confirmer avant de continuer.")
