import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Choix de la date", page_icon="📅")

if not st.session_state.get("confirmed_location"):
    st.error("⛔ Vous devez d'abord sélectionner un lieu.")
    st.stop()

st.title("📅 Sélectionnez une date")

date = st.date_input("Choisissez une date :", value=datetime.today())

if st.button("✅ Confirmer la date"):
    st.session_state.selected_date = date
    st.success(f"Date {date} confirmée.")
    st.markdown("[➡️ Afficher l'heure à laquelle le soleil atteint la hauteur cible](Resultats)")
