from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    #Number of Messages
    num_messages = df.shape[0]
    
    #Number Of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    #Number of Media
    number_of_media_shared = df[df['messages']=="<Media omitted>\n"].shape[0]

    #Number Of URLs
    link = []
    for message in df['messages']:
        link.extend(extract.find_urls(message))

    return num_messages, len(words), number_of_media_shared,len(link)

def busiest_user(df):
    x = df['user'].value_counts().head()
    user_msg_percent = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"user":"name","count":"percentage"})
    return x, user_msg_percent


def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_word = f.read()

    if selected_user !='Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_word:
               words.append(word)
        
        return " ".join(words)

    temp['messages'] = temp['messages'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")

    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    
    f = open('stop_hinglish.txt', 'r')
    stop_word = f.read()

    if selected_user !='Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('daily').count()['messages'].reset_index()
    return daily_timeline

def weekly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day',columns='period', values='messages',aggfunc='count').fillna(0)
    return user_heatmap