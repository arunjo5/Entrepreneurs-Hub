import streamlit as st
import yfinance as yf
import sqlite3
import streamlit as st
import datetime as dt
import yfinance as yf
from prophet import Prophet
from plotly import graph_objs as go
from prophet.plot import plot_plotly
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from streamlit_option_menu import option_menu
from streamlit_chat import message
import openai
from streamlit_chat import message
import requests
import pandas as pd
from mdtable import MDTable
from pathlib import Path

st.markdown(
    """
    <style>
    .block-container {
        text-align: center;

    }
    footer {visibility: hidden;}

    .title {
        align-self: flex-start;
     </style>
    """,
    unsafe_allow_html=True
)

background = Image.open("en-logo.png")
col1, col2, col3 = st.columns([0.8, 5, 0.2])
col2.image(background, width=500)

selected_page = option_menu(
    menu_title=None,
    options=["BizMatch", "BizBot", "Idea Oasis"],
    icons=["map", "person-circle", "info", "geo"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)


if selected_page == "BizMatch":
    conn = sqlite3.connect('investors.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS investors
                (name TEXT, description TEXT, funding REAL, industry TEXT, contact TEXT)''')
    conn.commit()

    # Investor Profile
    def investor_profile():
        st.subheader("Match with a Startup Founder!")
        name = st.text_input("Name")
        description = st.text_area("Description")
        funding = st.number_input("Funding Amount", min_value=0.0)
        interests = st.text_input("Interested Industries (comma-separated)")
        contact = st.text_input("Contact Information")
        if st.button("Submit"):
            interests_list = [interest.strip().lower()
                              for interest in interests.split(",")]
            for interest in interests_list:
                c.execute("INSERT INTO investors VALUES (?, ?, ?, ?, ?)",
                          (name, description, funding, interest, contact))
            conn.commit()
            st.success("Profile submitted successfully!")

    # Startup Founder
    def startup_founder():
        st.subheader("Match with an Investor!")
        industries = set()
        # Get all unique industries from the database
        for row in c.execute("SELECT DISTINCT industry FROM investors"):
            industries.add(row[0])
        selected_industry = st.selectbox(
            "Select an Industry", list(industries))
        if st.button("Find Investors"):
            # Get investors with similar interests from the database 
            c.execute(
                "SELECT * FROM investors WHERE LOWER(industry) = LOWER(?)", (selected_industry,))
            results = c.fetchall()
            st.subheader("Matching Investors:")
            for result in results:
                st.write("Name:", result[0])
                st.write("Description:", result[1])
                st.write("Funding:", result[2])
                st.write("Contact:", result[4])
                st.write("---")

    # Streamlit App
    def main():
        st.header("Investor-Founder Matcher")

        page = option_menu(
            menu_title=None,
            options=["Investor Profile", "Startup Founder"],
            icons=["map", "person-circle"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            key="nav_bar"
        )
        st.markdown("<br>", unsafe_allow_html=True) 

        if page == "Investor Profile":
            investor_profile()
        elif page == "Startup Founder":
            startup_founder()

    if __name__ == '__main__':
        main()

elif selected_page == "BizBot":
                
    openai.api_key = st.secrets["OPENAI_KEY"]
    st.subheader("Or ask any General Questions")
    query = st.text_input("Have any business questions?")

    if query:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].text

        st.write(answer)

openai.api_key = st.secrets["OPENAI_KEY"]
    # Openai GPT-3 requests
def generate_name(industry, budget, target_audience):
        prompt_text = f"Generate a unique business name with no period in the {industry} industry with a budget of {budget} , targeting {target_audience}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_text,
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()

def generate_idea(industry, budget, target_audience):
        prompt_text = f"Generate a unique business idea in the {industry} industry with a budget of {budget} , targeting {target_audience}."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_text,
            temperature=0.5,
            max_tokens=200
        )
        return response.choices[0].text.strip()

def get_competition(idea):
    prompt_text = f"Find potential competitors or similar companies for a business idea like: {idea}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_text,
        temperature=0.5,
        max_tokens=200
    )
    return response.choices[0].text.strip()

if selected_page == "Idea Oasis":
    st.subheader("Generate a Unique Idea ")
    
    industry = st.text_input("Industry")
    budget = st.text_input("Budget")
    target_audience = st.text_input("Target Audience")

    if st.button("Generate Idea"):
        name = generate_name(industry,budget,target_audience)
        idea = generate_idea(industry, budget, target_audience)

        st.markdown(f"### {name}\n{idea}")
    
    st.subheader("Discover the Competition")

    competition_idea = st.text_input("Enter your business idea")
    
    if st.button("Get Competitors"):
        competitors = get_competition(competition_idea)
        st.markdown(f"### Potential Competitors\n{competitors}")
