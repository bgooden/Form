import streamlit as st
import pandas as pd 
from streamlit_gsheets import GSheetsConnection

GSHEET_URL = "https://docs.google.com/spreadsheets/d/1OXYM4dz36wonTqNQkyWSiU6HNGqJHh_j9-p0wJZBJ-Q/edit?usp=sharing"

st.title("ΔΓΙ Interest Form")
conn = st.connection("gsheets", type=GSheetsConnection)
left_co, cent_co, right_co = st.columns([1, 2, 1])
with cent_co:
    st.image("dgi crest.jpg",caption="Diligence! Brotherhood! Integrity!", width = 300)
if "applications" not in st.session_state:
  st.session_state.applications = []

with st.form(key='my_form'):
    st.write("Please fill out the information below")

    year = st.radio( "What is your year?",['Freshman','Sophomore','Junior','Senior'])
    full_name = st.text_input("Full Name")
    number = st.text_input("Phone Number")
    major = st.text_input("Major")
    why = st.text_input("Why rush us?")
    col1,col2 = st.columns(2)
    with col1:
        social1 = st.text_input("Snapchat (Optional)")
    with col2:
        social2 = st.text_input("Instagram (Optional)")

    submitted = st.form_submit_button("Submit Form")

if submitted:
    if not full_name:
        st.error("You can't leave your full Name empty")
    elif not number:
        st.error("You can't leave your phone number empty")
    elif not major:
        st.error("You can't leave your major empty")
    elif not why:
        st.error("You can't leave why you are interesting in rush empty")
    else:
        with st.spinner("Submitting your application..."):
            try:
                existing_data = conn.read(spreadsheet=GSHEET_URL)
                if existing_data is None or existing_data.empty:
                    existing_data = pd.DataFrame()
            except Exception as e:
                st.error(e)
                existing_data = pd.DataFrame()

        new_applications = {
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": full_name,
            "Year": year,
            "Phone": number,
            "Major": major,
            "Snapchat": social1 if social1 else "N/A",
            "Instagram": social2 if social2 else "N/A",
            "Reason for Rushing": why,
        }

        try:

            new_row = pd.DataFrame([new_applications])
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)

            conn.update(spreadsheet=GSHEET_URL, data=updated_df)
            st.success(f"Success! Thank you for your time {full_name}!")

        except Exception as e:
            st.error(f"Error saving data: {e}")
