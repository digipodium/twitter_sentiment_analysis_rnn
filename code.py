import os
from numpy.lib.function_base import select
import streamlit as st
from database.db import Tweet,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# functions

def create_db():
    if not os.path.exists('database/db.sqlite3'):
        engine = create_engine('sqlite:///database/db.sqlite3')
        Base.metadata.create_all(engine)
        st.sidebar.success("database connected")

def opendb():
    engine = create_engine('sqlite:///database/db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_tweet(text):
    try:
        db = opendb()
        db.add(Tweet(text=text))
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

def load_tweets():
    db = opendb()
    results = db.query(Tweet).all()
    db.close()
    return results

def delete_tweet():
    try:
        db = opendb()
        db.query(Tweet).filter(Tweet.id == sel_tweets.id).delete()
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.error("tweet could not deleted")
        st.error(e)
        return False

def update_prediction(tweetid, prediction):
    pass

def load_model():
    pass

def predict_sentiment():
    pass


create_db()
############### UI for the project ######################
st.sidebar.image('images/side.png', use_column_width=True)
st.sidebar.title("Final year project @ BBD")
choice = st.sidebar.selectbox("select option",['Add new tweet','View Data Visualization','View tweets','Manage tweet data','About project team'])

if choice == 'Add new tweet':
    st.image('images/2.png', use_column_width=True)
    st.header("Add new tweet")
    form = st.form(key='form1')
    tweet_content = form.text_area("enter a tweet here")
    submit = form.form_submit_button("analyse")
    if tweet_content and submit:
        pass
    else:
        st.sidebar.info("Please start by adding the tweet in the form, which will be then analysed")

if choice == 'View tweets':
    st.image('images/1.png', use_column_width=True)
    st.header("view saved tweets")
    sel_tweet = st.sidebar.radio('select a tweet to view',load_tweets())
    if sel_tweet:
        st.warning("selected Tweet")
        st.header(sel_tweet)
        st.warning(f'PREDICTION: {sel_tweet.prediction}')
        st.warning(f'DATE: {sel_tweet.created_on}')
    else:
        st.sidebar.info("Please select a tweet from the dropdown for viewing tweet")

if choice == 'Manage tweet data':
    st.image('images/3.png', use_column_width=True)
    st.header("manage saved tweets")
    sel_tweet = st.sidebar.radio('select a tweet to remove',load_tweets())
    if sel_tweet:
        st.warning("Selected Tweet")
        st.header(sel_tweet)
        if st.button("delete"): 
            if delete_tweet(sel_tweet):
                st.info("tweet deleted from database")
            else:
                st.error("please read the error msg")
    else:
        st.sidebar.info("Please select a tweet from the dropdown for deleting from database")

if choice =='View Data Visualization':
    st.image('images/4.png', use_column_width=True)
    st.header("view dataset tweets visualization")
    graphs = os.listdir("graphs")
    graphs = [os.path.splitext(name)[0] for name in graphs]
    graph = st.selectbox("select a visualizations",graphs)
    if graph:
        graphpath = os.path.join('graphs',graph+'.png')
        st.image(graphpath,caption=graph)

if choice == 'About project team':
    st.image('images/1.png', use_column_width=True)
    st.header("About us")
    pass