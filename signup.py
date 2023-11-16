import streamlit as st
import datetime
import re
from deta import Deta

DETA_KEY = 'd0igzacyuds_iRoN5CBg76A2vfoJoZid6HWotfUmWeqT'

deta = Deta(DETA_KEY)

db = deta.Base('Authenticate')

def insert_user(username, email, password):
    date_joined = str(datetime.datetime.now())
    return db.put({'key': email, 'Username': username, 'Password': password, 'date_joined': date_joined})

def fetch_users():
    users = db.fetch()
    return users.items

def get_user_emails():
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails

def get_usernames():
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['Username'])
    return usernames

def validate_email(email):
    pattern = "^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pattern, email):
        return True
    return False

def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False


def sign_up():
    with st.form(key='SignUp', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        username = st.text_input('Username',value="", placeholder='Enter User Name')
        email = st.text_input('Email', placeholder='Enter Email')
        password = st.text_input('Password',value="", placeholder='Enter Password', type='password')
        password1 = st.text_input('Confirm Password',value="", placeholder='Confirm Password', type='password')

        submit_button = st.form_submit_button('Submit')

        if submit_button:
            if email and validate_email(email):
                if email not in get_user_emails():
                    if username and validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 4:
                                if len(password) >= 6:
                                    if password == password1:
                                        insert_user(username, email, password)
                                        st.success("Account created successfully!")
                                        st.write("Now you can login your account.")
                                        st.balloons()
                                        st.experimental_set_query_params(signup=False, login=True)
                                        return True
                                    else:
                                        st.warning("Passwords do not match!")
                                else:
                                    st.warning("Password is too short!")
                            else:
                                st.warning("Username is too short!")
                        else:
                            st.warning("Username already exists!")
                    else:
                        st.warning("Invalid Username!")
                else:
                    st.warning("Email already exists!")
            elif email:
                st.warning("Invalid Email!")

    return False


if __name__ == "__main__":
    sign_up()