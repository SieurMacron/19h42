import streamlit as st

# Initialisation de la page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Barre de navigation horizontale
page = st.radio("Navigation", ["Home", "Date", "Résultats"],
                index=["Home", "Date", "Résultats"].index(st.session_state.page),
                horizontal=True)

st.session_state.page = page

# Exécution des fichiers dans le même contexte que le script principal
page_files = {
    "Home": "home.py",
    "Date": "date_page.py",
    "Résultats": "resultats.py"
}

with open(page_files[page], "r", encoding="utf-8") as f:
    exec(f.read(), globals())
