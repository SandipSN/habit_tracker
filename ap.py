import streamlit as st
import pandas as pd
import database as db
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ["ss13"]
usernames = ["ss13"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "ld_rc", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

    class main:
        def __init__(self):
            # Initialize a session state variable
            if "rc" not in st.session_state:
                st.session_state["rc"] = 0
            self.rc = st.session_state["rc"]
            self.run()

        def run(self):
            st.title("🚀")  

            date = st.date_input('Date')
            date = str(date)
            data = db.get_record(date)
            data = pd.DataFrame(data, index=[0])
                    
            try:
                st.metric(label="RCs", value=data.rcs)
            except:
                st.metric(label="RCs", value=0)
        
            #st.write(data) 

            col1, col2  = st.columns(2)

            with col1:                
                if st.button("  -1  "):
                    st.session_state["rc"] -=1
            
            with col2:
                if st.button("+1"):
                    st.session_state["rc"] +=1
                    
            st.write(self.rc)

            if st.button("Submit"):
                db.insert_record(date, self.rc)

            #st.metric(label="Date", value=date)
        
        # fetch data

            all_data = db.fetch_all()
            all_data = pd.DataFrame(all_data)

            all_data[['rcs']] = all_data[['rcs']].apply(pd.to_numeric)

            all_data = all_data.set_index("key")

            st.line_chart(data=all_data)

            st.write(all_data)

            #df = pd.DataFrame(new_data, index=[0])
            # st.write(df)  
            

    if __name__ == "__main__":
        main()
