import requests
import tweepy
import os

key="EnQaXrqXBrlyGmCot7Eic8Fl5"
secret='4M29YFccJUCKX4Hp6ZYb9yeUkMlm8bzItAbR7iyUWOhTVAzoer'




auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token('1431473124281774084-RipZ0OgBNOTtDXhLrXNZegZxqeD3b6', 'hIIf5y4GXe8q2evTyU3a0HSbs0lZ6aibFVvvNhrnD8Tlk')

# Create API object
api = tweepy.API(auth,wait_on_rate_limit=True)

def lookupFollowing(screen_name):
 following=False
 user_ids=[]
 return api.lookup_friendships(screen_name=[screen_name])[0].is_followed_by
 
import pandas as pd

def extend(df,worksheet):
    for i, col in enumerate(df.columns):
        column_len = df[col].astype(str).str.len().max()
        column_len = max(column_len, len(col)) + 2
        worksheet.set_column(i, i, column_len)
