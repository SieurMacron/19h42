import streamlit as st

# Initialisation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Barre de navigation
page = st.radio("Navigation", ["Home", "Date", "Résultats"], index=["Home", "Date", "Résultats"].index(st.session_state.page), horizontal=True)
st.session_state.page = page

page_files = {
    "Home": "home.py",
    "Date": "date_page.py",
    "Résultats": "resultats.py"
}
with open(page_files[page], "r", encoding="utf-8") as f:
    code = f.read()
    exec(code, globals())
