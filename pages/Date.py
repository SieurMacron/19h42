import streamlit as st
from datetime import date

st.set_page_config(page_title="Choix de la date", layout="centered")
st.title("📅 Sélectionnez une date")

if not st.session_state.get("confirmed_location"):
    st.warning("Veuillez d'abord sélectionner un lieu sur la carte.")
    st.page_link("Home", label="⬅️ Retour à la sélection du lieu")
    st.stop()

st.subheader("📍 Lieu confirmé :")
st.write(f"- Latitude : `{st.session_state.lat:.4f}`")
st.write(f"- Longitude : `{st.session_state.lon:.4f}`")
st.write(f"- Fuseau horaire : `{st.session_state.timezone}`")

st.markdown("---")

selected_date = st.date_input(
    "📆 Choisissez une date",
    min_value=date.today(),
    max_value=date(2100, 12, 31),
    value=date.today()
)

if st.button("✅ Confirmer cette date"):
    st.session_state.date = selected_date
    st.session_state.confirmed_date = True
    st.success(f"Date sélectionnée : {selected_date.strftime('%d %B %Y')}")
    st.page_link("pages/Resultats.py", label="➡️ Voir l’heure où le soleil atteint la hauteur", icon="🌞")

