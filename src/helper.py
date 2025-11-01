from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

url = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_msg=df[df['message']=='<Media omitted>'].shape[0]

    links = []
    for message in df['message']:
        links.extend(url.find_urls(message)) 

    return num_messages, len(words), num_media_msg,len(links)


def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name',"user":"percent"})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['user'] != 'group_notification']
    df = df[df['message']!='<Media omitted>']

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message']!='<Media omitted>']

    f=open("stop_hinglish.txt",'r')
    stop_words =f.read()

    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    time_line = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time =[]
    for i in range(time_line.shape[0]):
        time.append(time_line['month'][i]+"-"+str(time_line['year'][i]))

    time_line['time']=time

    return time_line

def dialy_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()