from typing import Any

import streamlit as st
import pandas as pd
from pandas import DataFrame

import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy as sp



df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df: DataFrame | Any = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olymics Analysis")
st.sidebar.image("C:/Users/neham/Downloads/Olympic_rings_without_rims.svg")
user_menu = st.sidebar.radio(
    "select an option",
    ('Medal Tally', "overall analysis", "Country-wise Analysis", "Athlete-wise Analysis")
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in  ' + str(selected_year) + 'Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_year) + " Olymics")

    st.table(medal_tally)

if user_menu == 'overall analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athlets = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("athletes")
        st.title(athlets)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations Over The YEars")
    st.plotly_chart(fig)

    events = helper.data_over_time(df, 'Event')
    fig = px.line(events,  x='Edition', y="Event")
    st.title("Events Over The Yeare")
    st.plotly_chart(fig)

    athlets_over_time  = helper.data_over_time(df, 'Name')
    fig = px.line(athlets_over_time,  x='Edition', y="Name")
    st.title("Athletes Over the Years")
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    ax= sns.heatmap(ax, annot=True, cmap="magma")
    st.pyplot(fig)

    st.title("Most Successful Athletss")
    sport_list =df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")

    select_sport = st.selectbox("Select a Sport",sport_list)
    x = helper.most_successful(df, "Overall")
    st.table(x)

if user_menu == "Country-wise Analysis":

    st.sidebar.title("Country-wise Analysis")

    country_list =df['region'].dropna().unique().tolist()
    country_list.sort()
    select_country = st.sidebar.selectbox("Select a Country", country_list)

    country_df=helper.yearwise_medal_tally(df,select_country)
    fig = px.line(country_df, x='Year', y="Medal")
    st.title(select_country + "Medal Tally  Over the Years")
    st.plotly_chart(fig)

    st.title(select_country + " excels in the following sports")
    pt=helper.country_event_heatmap(df,select_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes " + select_country)
    top10_df = helper.most_successful_countrywise(df,select_country)
    st.table(top10_df)

if user_menu == "Athlete-wise Analysis":
    st.sidebar.title("Athlete-wise Analysis")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig=ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                       show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of AGE")
    st.plotly_chart(fig)

    x=[]
    name=[]
    famous_sports=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis','Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig= ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of AGE wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    st.title('Height vs Weight')
    select_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_v_heigh(df,select_sport)
    fig,ax = plt.subplots()
    ax =  sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'],
                          hue = temp_df["Medal"],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title('Men VS  Women Over The Years')
    final=helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=['Male', "Female"], color_discrete_map={'Male': 'blue', 'Female': 'orange'})
    st.plotly_chart(fig)