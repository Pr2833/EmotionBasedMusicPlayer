import streamlit as st
from log_in import login
from Test_Images import emotion
from signup import sign_up
def dashboard():
    st.subheader("Welcome to the Music World")

if __name__ == "__main__":
    menu = ["🏠Home", "🔒 Login", "🔒Signup"]
    choice = st.sidebar.selectbox("Let's get Started", menu)

    if choice == "🏠Home":
        st.subheader("🎶 🏠Home🏠🎶")
        st.write("Welcome to the **Music World**! : Let the rhythm guide you.")

        st.markdown(
            """🎶🎶🎶🎶🎶
            This is your gateway to an auditory adventure! Choose from options in the sidebar 
            to explore the magic of music. :headphones: 🎧🎧🎧🎧🎧
            """
        )

    elif choice == "🔒 Login":

        if login():
                emotion()

    elif choice == "🔒Signup":

        sign_up()
