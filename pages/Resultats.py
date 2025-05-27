import streamlit as st

st.set_page_config(page_title="Résultats")

st.title("🌞 Résultats")

if not all(k in st.session_state for k in ("lat", "lon", "timezone", "selected_date")):
    st.warning("Données manquantes. Retournez en arrière pour sélectionner lieu et date.")
    st.stop()

st.write(f"Lieu : lat {st.session_state.lat:.4f}, lon {st.session_state.lon:.4f}, fuseau {st.session_state.timezone}")
st.write(f"Date : {st.session_state.selected_date}")

# Ici tu peux mettre le calcul ou affichage des heures de lever/coucher, hauteur etc.

st.success("Ici, les résultats calculés et affichés !")
