import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message':messages,"message_date":dates})
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ') 
    df['message_date']=pd.to_datetime(df['message_date'],format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date':'date'},inplace=True)
    users = []
    messages = []
    users = []
    messages = []

    for message in df['user_message']:
        match = re.match(r'^([^:]+):\s(.*)', message)
        if match:
            users.append(match.group(1).strip())
            messages.append(match.group(2).strip())
        else:
            users.append('group_notification')
            messages.append(message.strip())

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year']=df['date'].dt.year
    df['month_num']  = df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['day_name']= df['date'].dt.day_name()

    return df

