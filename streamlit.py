import streamlit as st
import pandas as pd
import numpy as np

st.title("Hello , Streamlit !")
st.write(".streamlit : This is your first streamlit")
st.text("Let get started")

name = st.text_input("Enter your name :")
if st.button("Greet"):
    st.success("Hello,{name}!")

df = pd.DataFrame(np.random.randn(10,2),columns=["A ", "B"])
st.line_chart(df)
st.bar_chart(df)

upload_file = st.file_uploader("upload a CSV file",type = 'csv')
if upload_file:
    df = pd.read_csv(upload_file)
    st.dataframe(df)

import streamlit as st

st.title("Text and Markdown Demo")
st.header("This is a header")
st.subheader("This is a Subheader")

st.markdown("**Bold**, *Italic*, `Code`, [Link](https://example.com)")
st.code("for i in range(5):\n    print(i)", language="python")

st.text_input("What is your name?")
st.text_area("Write Something")

st.number_input("Pick a number", min_value=0)

st.slider("Choose a range", 0, 100)

st.selectbox("Select a fruit", ["Apple", "Banana"])

st.multiselect("Choose Toppings", ["Cheese", "Tomato"])

st.radio("Pick one", ["Option A", "Option B"])

st.checkbox("I agree to the terms")

if st.checkbox("Show Details"):
    st.info("Here are more detail...")

option = st.radio("Choose view", ["Show Chart" , "Show table"])
if option =="Show Chart":
    st.write("Chart would appear here")
else:
    st.write("Table wuld appear here")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        st.success("Welcome",{username})