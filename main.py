import streamlit as st

# Initialisation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Barre de navigation
page = st.radio("Navigation", ["Home", "Date", "Résultats"], index=["Home", "Date", "Résultats"].index(st.session_state.page), horizontal=True)
st.session_state.page = page

# Inclusion des pages
if page == "Home":
    import home
elif page == "Date":
    import date_page
elif page == "Résultats":
    import resultats
