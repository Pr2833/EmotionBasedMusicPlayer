import streamlit as st
from deta import Deta
from streamlit import experimental_set_query_params
import cv2
import numpy as np
from keras.models import model_from_json
from Test_Images import emotion


DETA_KEY = 'd0igzacyuds_iRoN5CBg76A2vfoJoZid6HWotfUmWeqT'

deta = Deta(DETA_KEY)

db = deta.Base('Authenticate')
def login():
        st.subheader(':blue[Login]')
        email = st.text_input(label='Email',key='email',value="", placeholder='Enter Email')
        password = st.text_input(label='Password', key="Password",value="",placeholder='Enter Password', type='password')

        if st.button('Submit'):
            if email and '@' in email:
                user_data = db.get(email)
            if user_data and user_data['Password'] == password:
                st.success("Logged in successfully!")
                st.experimental_set_query_params(login=False, Test_Images=True)
                return True
                # Redirect to Test_Images after 3 seconds
            elif user_data:
                st.warning("Incorrect Password!")
            else:
                st.warning("Email does not exist!")

        return False
if __name__=="__main__":

    if login():

        emotion()