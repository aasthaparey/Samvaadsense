
# from emoji import unicode_codes, analyze
# from urlextract import URLExtract
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# from collections import Counter
# extract = URLExtract()

# def fetch_stats(selected_user, df):
#     if selected_user=='Overall':
#         # fetching number of messages
#         num_messages = df.shape[0]
#         num_media_messages = df[df['message']== '<Media omitted>\n'].shape[0]
#         # fetching number of words
#         words = []
#         for message in df['message']:
#             words.extend(message.split())
#         links = []
#         for message in df['message']:
#             links.extend(extract.find_urls(message))
#         return num_messages, len(words), num_media_messages, len(links)
#     else:
#         num_messages = df[df['user']==selected_user].shape[0]
#         num_media_messages = df[(df['user'] == selected_user) & (df['message'] == '<Media omitted>\n')].shape[0]
#         words = []
#         links = []
#         for message in df[df['user']==selected_user]['message']:
#             words.extend(message.split())
#         for message in df[df['user'] == selected_user]['message']:
#             links.extend(extract.find_urls(message))
#         return num_messages, len(words), num_media_messages, len(links)

# def most_busy_users(df):
#     x = df['user'].value_counts().head()
#     name = x.index
#     count = x.values
#     df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
#     return name,count, df

# def create_wordcloud(selected_user,df):

#     f = open('stop_hinglish.txt', 'r')
#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

#     def remove_stop_words(message):
#         y = []
#         for word in message.lower().split():
#             if word not in stop_words:
#                 y.append(word)
#         return " ".join(y)

#     wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
#     temp['message'] = temp['message'].apply(remove_stop_words)
#     df_wc = wc.generate(temp['message'].str.cat(sep=" "))
#     return df_wc

# def most_common_words(selected_user, df):
#     if selected_user!= 'Overall':
#         df = df[df['user'] == selected_user]

#     temp = df[df['user']!='group_notification']
#     temp = temp[temp['message']!= '<Media omitted>\n']
#     f = open('stop_hinglish.txt')
#     stop_words = f.read()
#     words = []

#     for message in temp['message']:
#         for word in message.lower().split():
#             if word not in stop_words:
#                 words.append(word)
#     return_df = pd.DataFrame(Counter(words).most_common(20))
#     return return_df

# import emoji
# from collections import Counter

# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df

# def monthly_timeline(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
#     time = []

#     for i in range(timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
#     timeline['time'] = time
#     return timeline

# def daily_timeline(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     daily_timeline = df.groupby('only_date').count()['message'].reset_index()

#     return daily_timeline

# def week_activity_map(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     return df['day_name'].value_counts()

# def month_activity_map(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     return df['month'].value_counts()

# def activity_heatmap(selected_user, df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     # Create pivot table for messages by day and hour period
#     user_heatmap = df.pivot_table(
#         index='day_name',
#         columns='period',
#         values='message',
#         aggfunc='count'
#     ).fillna(0)

#     # ✅ Ensure correct chronological order of hours (24-hour format)
#     ordered_periods = [
#         '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10',
#         '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
#         '18-19', '19-20', '20-21', '21-22', '22-23', '23-00'
#     ]

#     # Reorder columns chronologically
#     user_heatmap = user_heatmap.reindex(columns=ordered_periods, fill_value=0)

#     # ✅ Optional: reorder days for consistency (Monday → Sunday)
#     day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     user_heatmap = user_heatmap.reindex(day_order)

#     return user_heatmap


# # ✨ NEW FEATURE: Contextual Summary Generator
# def generate_summary(df, selected_user):
#     # Filter for selected user
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     total_messages = df.shape[0]
#     total_words = df['message'].apply(lambda x: len(x.split())).sum()
#     total_media = df[df['message'] == '<Media omitted>\n'].shape[0]
#     avg_messages_per_day = round(total_messages / df['only_date'].nunique(), 2)

#     # Time-based insights
#     active_day = df['day_name'].value_counts().idxmax()
#     active_hour = df['hour'].value_counts().idxmax()

#     # Emoji insights
#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
#     most_used_emoji = max(Counter(emojis), key=Counter(emojis).get) if emojis else None

#     # Top 3 most active users
#     top_users = df['user'].value_counts().head(3)
#     top_users_text = ", ".join([f"{user} ({count} msgs)" for user, count in top_users.items()])

#     # Contextual tone
#     if active_hour < 12:
#         time_context = "in the mornings, showing early-day discussions or planning."
#     elif 12 <= active_hour < 18:
#         time_context = "in the afternoons, suggesting casual mid-day conversations."
#     else:
#         time_context = "in the evenings, indicating higher engagement after work or studies."

#     if active_day in ["Friday", "Saturday", "Sunday"]:
#         day_context = f"with **{active_day}s** being the most active, hinting that users are more social during weekends."
#     else:
#         day_context = f"with **{active_day}s** being the most active, reflecting weekday coordination and communication."

#     # Narrative summary
#     summary = f"""
# 📊 **General Analysis Summary**

# This chat contains **{total_messages} messages** exchanged with approximately **{total_words} words** in total.  
# Participants shared **{total_media} media files** (photos, videos, or voice notes).

# 🕒 On average, **{avg_messages_per_day} messages are sent per day**, showing consistent engagement levels.  
# The conversation is most active **around {active_hour}:00 hrs**, {time_context}  
# and {day_context}

# The most frequently used emoji is **{most_used_emoji if most_used_emoji else 'N/A'}**, reflecting the general tone and mood of the chat.  

# 👥 The **top 3 most active participants** are:  
# 👉 {top_users_text}

# {"This summary reflects overall group behaviour." if selected_user == 'Overall' else f"This summary focuses on the activity of **{selected_user}**."}
# """

#     return summary

from emoji import unicode_codes, analyze
from urlextract import URLExtract
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji

extract = URLExtract()

# -------------------------------------------------------------
# 📊 Fetch basic statistics
# -------------------------------------------------------------
def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        num_messages = df.shape[0]
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

        words = []
        for message in df['message']:
            words.extend(message.split())

        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_messages, len(links)
    else:
        df = df[df['user'] == selected_user]
        num_messages = df.shape[0]
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

        words = []
        links = []
        for message in df['message']:
            words.extend(message.split())
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_messages, len(links)


# -------------------------------------------------------------
# 👥 Most Busy Users
# -------------------------------------------------------------
def most_busy_users(df):
    x = df['user'].value_counts().head()
    name = x.index
    count = x.values
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}
    )
    return name, count, df_percent


# -------------------------------------------------------------
# ☁️ Word Cloud
# -------------------------------------------------------------
def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


# -------------------------------------------------------------
# 📝 Most Common Words
# -------------------------------------------------------------
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    f = open('stop_hinglish.txt')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


# -------------------------------------------------------------
# 😂 Emoji Analysis
# -------------------------------------------------------------
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


# -------------------------------------------------------------
# 🗓️ Monthly Timeline (Chronologically Fixed)
# -------------------------------------------------------------
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by year and month number to maintain order
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Sort by year and month number
    timeline = timeline.sort_values(['year', 'month_num']).reset_index(drop=True)

    # Create month-year labels
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline


# -------------------------------------------------------------
# 📅 Daily Timeline
# -------------------------------------------------------------
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


# -------------------------------------------------------------
# 📆 Weekly Activity Map
# -------------------------------------------------------------
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Count messages per day
    day_counts = df['day_name'].value_counts()

    # ✅ Reorder days chronologically (Mon → Sun)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = day_counts.reindex(day_order, fill_value=0)

    return day_counts


# -------------------------------------------------------------
# 📆 Monthly Activity Map (Chronologically Fixed)
# -------------------------------------------------------------
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    month_counts = df['month'].value_counts()

    # Reorder months chronologically
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    month_counts = month_counts.reindex(month_order, fill_value=0)

    return month_counts


# -------------------------------------------------------------
# 🔥 Activity Heatmap (Chronological Fix)
# -------------------------------------------------------------
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    ordered_periods = [
        '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10',
        '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
        '18-19', '19-20', '20-21', '21-22', '22-23', '23-00'
    ]

    # Reorder periods and days
    user_heatmap = user_heatmap.reindex(columns=ordered_periods, fill_value=0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    user_heatmap = user_heatmap.reindex(day_order)

    return user_heatmap


# -------------------------------------------------------------
# 🧠 AI-Like Chat Summary
# -------------------------------------------------------------
def generate_summary(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    total_messages = df.shape[0]
    total_words = df['message'].apply(lambda x: len(x.split())).sum()
    total_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    avg_messages_per_day = round(total_messages / df['only_date'].nunique(), 2)

    active_day = df['day_name'].value_counts().idxmax()
    active_hour = df['hour'].value_counts().idxmax()

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    most_used_emoji = max(Counter(emojis), key=Counter(emojis).get) if emojis else None

    top_users = df['user'].value_counts().head(3)
    top_users_text = ", ".join([f"{user} ({count} msgs)" for user, count in top_users.items()])

    # Context generation
    if active_hour < 12:
        time_context = "in the mornings, showing early-day discussions or planning."
    elif 12 <= active_hour < 18:
        time_context = "in the afternoons, suggesting casual mid-day conversations."
    else:
        time_context = "in the evenings, indicating higher engagement after work or studies."

    if active_day in ["Friday", "Saturday", "Sunday"]:
        day_context = f"with **{active_day}s** being the most active, hinting that users are more social during weekends."
    else:
        day_context = f"with **{active_day}s** being the most active, reflecting weekday coordination and communication."

    summary = f"""
📊 **General Analysis Summary**

This chat contains **{total_messages} messages** exchanged with approximately **{total_words} words** in total.  
Participants shared **{total_media} media files** (photos, videos, or voice notes).

🕒 On average, **{avg_messages_per_day} messages are sent per day**, showing consistent engagement levels.  
The conversation is most active **around {active_hour}:00 hrs**, {time_context}  
and {day_context}

The most frequently used emoji is **{most_used_emoji if most_used_emoji else 'N/A'}**, reflecting the general tone and mood of the chat.  

👥 The **top 3 most active participants** are:  
👉 {top_users_text}

{"This summary reflects overall group behaviour." if selected_user == 'Overall' else f"This summary focuses on the activity of **{selected_user}**."}
"""
    return summary

