import os
from numpy.lib.function_base import select
import streamlit as st
from database.db import Tweet,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.keras.models import load_model
import re
import plotly.express as px



# settings
st.set_page_config(layout='wide')
embedding_dim=64
pad_type='post'
trunc_type='post'
maxlen=64

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

def save_tweet(text,sentiment):
    try:
        db = opendb()
        idx = sentiment.argmax()
        # st.write(text,sentiment,sentiment.argmax(),idx)
        if idx == 1:
            tweet = Tweet(text=text,prediction="🥳 positive 🥳",pos=sentiment[1],neg=sentiment[0],neu=sentiment[2])
        elif idx == 0:
            tweet = Tweet(text=text,prediction="😡 negative 😡",pos=sentiment[1],neg=sentiment[0],neu=sentiment[2])
        else:
            tweet = Tweet(text=text,prediction="😐 neutral 😐",pos=sentiment[1],neg=sentiment[0],neu=sentiment[2])
        db.add(tweet)
        db.commit()
        db.close()
        return tweet
    except Exception as e:
        st.write("database error:",e)
        return False

def load_tweets():
    db = opendb()
    results = db.query(Tweet).all()
    db.close()
    return results

def delete_tweet(sel_tweet):
    try:
        db = opendb()
        db.query(Tweet).filter(Tweet.id == sel_tweet.id).delete()
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.error("tweet could not deleted")
        st.error(e)
        return False


def ai_load_model():
    return load_model(r'trained_model\model.h5')

def load_tokenizer():
    with open(r'trained_model\tokenizer.pk','rb') as f:
        return pickle.load(f)

def load_encoder():
    with open(r'trained_model\encoder.pk','rb') as f:
        return pickle.load(f)

def predict_sentiment(tweetdata):
    model = ai_load_model()
    tokenizer = load_tokenizer()
    le = load_encoder()
    input_data =np.array(tweetdata)
    input_sequences=tokenizer.texts_to_sequences(input_data)
    input_final=pad_sequences(input_sequences,padding=pad_type,truncating=trunc_type,maxlen=maxlen)
    return np.round(model.predict(input_final),2)

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)



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
        tweets = tweet_content.split('\n')
        
        clean_tweets = [deEmojify(tweet) for tweet in tweets if tweet]
        sentiment_data = predict_sentiment(clean_tweets)
        for clean_tweet, sentiment in zip(clean_tweets,sentiment_data):
            if save_tweet(clean_tweet,sentiment):
                st.sidebar.success(f"updated the entry : {clean_tweet}")
    else:
        st.sidebar.info("Please start by adding the tweet in the form, which will be then analysed")

if choice == 'View tweets':
    st.image('images/1.png', use_column_width=True)
    st.header("view saved tweets")
    sel_tweet = st.sidebar.radio('select a tweet to view',load_tweets())
    if sel_tweet:
        
        c1,c2 = st.beta_columns(2)
        c2.markdown(f"## TWEET \n>{sel_tweet}\n")
        c2.markdown(f'## PREDICTION: \n>{sel_tweet.prediction.upper()}')
        c2.markdown(f'## DATE: \n>{sel_tweet.created_on}')
        fig = px.pie(names=['positive','negative','neutral'],values=[sel_tweet.pos,sel_tweet.neg,sel_tweet.neu],color=['green','red','white'],title='tweet analysis',hole=.5)
        c1.plotly_chart(fig)

    else:
        st.sidebar.info("Please select a tweet from the dropdown for viewing tweet")

if choice == 'Manage tweet data':
    st.image('images/3.png', use_column_width=True)
    st.header("manage saved tweets")
    sel_tweet = st.radio('select a tweet to remove',load_tweets())
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
    c1,c2= st.beta_columns(2)
    st.subheader("Team Members")
    c1.success("Pushkar dubey")
    # c1.image('images/pushkar.jpg')
    c2.success("Karina Singh")
    c1.success("Ritu Verma")
    c2.success("Priyanka verma")
    c1.success("Shivani Awasthi")