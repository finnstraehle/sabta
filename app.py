import streamlit as st

def main():
    """
    Main entry point for the Streamlit app.
    It displays a sidebar navigation menu that routes to different pages.
    """
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ("Home", "Case Prep", "Drills", "Sparring")
    )

    if page == "Home":
        from pages import home
        home.home_page()
    elif page == "Case Prep":
        from pages import case_prep
        case_prep.case_prep_page()
    elif page == "Drills":
        from pages import drills
        drills.drills_page()
    elif page == "Sparring":
        from pages import sparring
        sparring.sparring_page()

if __name__ == "__main__":
    main()
