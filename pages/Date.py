import streamlit as st
from datetime import date

st.set_page_config(page_title="Sélection de la date")

st.title("📅 Sélectionnez une date")

# Affiche le lieu sélectionné pour rappel
if all(k in st.session_state for k in ("lat", "lon", "timezone")):
    st.write(f"📍 Lieu sélectionné : lat {st.session_state.lat:.4f}, lon {st.session_state.lon:.4f}, fuseau {st.session_state.timezone}")
else:
    st.warning("Aucun lieu sélectionné. Retournez à la page d'accueil.")
    st.stop()

selected_date = st.date_input("Choisissez une date", value=date.today())

if st.button("✅ Confirmer la date"):
    st.session_state.selected_date = selected_date
    st.session_state.confirmed_date = True
    st.success(f"Date confirmée : {selected_date}")

# Plus de lien vers Resultats
if not st.session_state.get("confirmed_date", False):
    st.info("Veuillez sélectionner une date et confirmer.")
