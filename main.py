import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import helper
import preprocessor
import importlib
import matplotlib as mpl
import matplotlib.font_manager as fm

# ✅ Force reload helper to apply latest edits
importlib.reload(helper)

# 🧩 Streamlit Page Config
st.set_page_config(page_title="🧠 SamvaadSense", page_icon="🧠", layout="wide")

# 🎨 Custom UI Styling
st.markdown("""
    <style>
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #f8f4ff;
        }

        /* General font */
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        /* Metric Values */
        div[data-testid="stMetricValue"] {
            color: #6f42c1;
            font-weight: bold;
            font-size: 28px;
        }

        /* Headings */
        h1, h2, h3 {
            color: #6f42c1;
        }

        /* Section Divider */
        hr {
            border: 1px solid #6f42c1;
            opacity: 0.3;
        }
    </style>
""", unsafe_allow_html=True)

# 🧠 SamvaadSense Header
st.markdown("""
    <h1 style='text-align: center; color: #6f42c1; font-size: 48px; font-weight: bold;'>
        🧠 SamvaadSense
    </h1>
    <p style='text-align: center; color: #6f42c1; font-size: 18px; font-style: italic;'>
        Making Conversations Make Sense 💬
    </p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar Upload Section
st.sidebar.title("📂 Upload WhatsApp Chat")
uploaded_file = st.sidebar.file_uploader("Choose a .txt file", type=["txt"])
st.sidebar.markdown("💡 *Tip: Export your chat **without media** for best results.*")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.markdown("## 📊 Key Statistics")

    # Fetch unique members
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Select user", user_list)

    if st.sidebar.button("Show Analysis"):
        # ---------------------------------------------------------
        # 🧮 ALIGNED KEY STATISTICS
        # ---------------------------------------------------------
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Total Messages", value=num_messages)
        with col2:
            st.metric(label="Total Words", value=words)
        with col3:
            st.metric(label="Media Shared", value=num_media_messages)
        with col4:
            st.metric(label="Links Shared", value=num_links)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 📆 Monthly Timeline
        # ---------------------------------------------------------
        st.title("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='#6f42c1', linewidth=2.5, marker='o')
        ax.set_xlabel("Month-Year")
        ax.set_ylabel("Messages Sent")
        ax.grid(alpha=0.3)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # 📅 Daily Timeline
        st.title("📆 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#b37feb', linewidth=1.8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Messages Sent")
        ax.grid(alpha=0.3)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 🗓️ Activity Map
        # ---------------------------------------------------------
        st.title('🗓️ Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#6f42c1')
            ax.set_ylabel("Message Count")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Active Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#ff9f1c')
            ax.set_ylabel("Message Count")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # 🔥 Weekly Heatmap
        st.title("🕒 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(user_heatmap, cmap="magma", ax=ax)
        st.pyplot(fig)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 👥 Most Busy Users (for group only)
        # ---------------------------------------------------------
        if selected_user == 'Overall':
            st.title('👥 Most Active Users')
            name, count, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(name, count, color='#e63946')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # ☁️ Word Cloud
        # ---------------------------------------------------------
        st.title("☁️ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # ---------------------------------------------------------
        # 🔠 Most Common Words
        # ---------------------------------------------------------
        st.title("🔠 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='#17a2b8')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 😂 Emoji Analysis (Fixed for visibility)
        # ---------------------------------------------------------
        st.title("😂 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            # ✅ Ensure emoji visibility (Windows fix)
            mpl.rcParams['font.family'] = 'Segoe UI Emoji'
            fig, ax = plt.subplots()
            ax.pie(
                emoji_df[1].head(),
                labels=emoji_df[0].head(),
                autopct="%0.2f",
                textprops={'fontsize': 12}
            )
            ax.set_title("Most Used Emojis", fontsize=14)
            st.pyplot(fig)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 📘 Summary Report
        # ---------------------------------------------------------
        st.title("📘 Summary Report")
        summary_text = helper.generate_summary(df, selected_user)
        st.markdown(summary_text)

        # ---------------------------------------------------------
        # Footer
        # ---------------------------------------------------------
        st.markdown("""
            <hr>
            <div style='text-align: center; color: #6f42c1; font-size:14px;'>
                Built with ❤️ using Streamlit | © 2025 <b>SamvaadSense</b>
            </div>
        """, unsafe_allow_html=True)

# import matplotlib.pyplot as plt
# import streamlit as st
# import seaborn as sns
# import helper
# import preprocessor
# import importlib
# import matplotlib as mpl
# import matplotlib.font_manager as fm

# # ✅ Force reload helper to apply latest edits
# importlib.reload(helper)

# # 🧩 Streamlit Page Config
# st.set_page_config(page_title="Samwad: WhatsApp Chat Analyser", layout="wide")
# st.sidebar.title("Samwad")

# uploaded_file = st.sidebar.file_uploader("Choose a file")

# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocessor.preprocess(data)

#     st.title("Top Statistics")

#     # Fetch unique members
#     user_list = df['user'].unique().tolist()
#     if 'group_notification' in user_list:
#         user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0, "Overall")
#     selected_user = st.sidebar.selectbox("Select user", user_list)

#     if st.sidebar.button("Show Analysis"):
#         # ---------------------------------------------------------
#         # 📊 ALIGNED KEY STATISTICS SECTION
#         # ---------------------------------------------------------
#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
#         st.markdown("### 📊 Key Statistics")

#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric(label="Total Messages", value=num_messages)
#         with col2:
#             st.metric(label="Total Words", value=words)
#         with col3:
#             st.metric(label="Media Shared", value=num_media_messages)
#         with col4:
#             st.metric(label="Links Shared", value=num_links)

#         # ---------------------------------------------------------
#         # 📆 Monthly Timeline
#         # ---------------------------------------------------------
#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message'], color='#1f77b4', linewidth=2)
#         ax.set_xlabel("Month-Year")
#         ax.set_ylabel("Messages Sent")
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # 📅 Daily Timeline
#         st.title("Daily Timeline")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#ff7f0e', linewidth=1.8)
#         ax.set_xlabel("Date")
#         ax.set_ylabel("Messages Sent")
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # ---------------------------------------------------------
#         # 🗓️ Activity Map
#         # ---------------------------------------------------------
#         st.title('Activity Map')
#         col1, col2 = st.columns(2)

#         with col1:
#             st.header("Most Busy Day")
#             busy_day = helper.week_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_day.index, busy_day.values, color='#6f42c1')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         with col2:
#             st.header("Most Busy Month")
#             busy_month = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values, color='#ff9f1c')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         # 🔥 Weekly Activity Heatmap
#         st.title("Weekly Activity Map")
#         user_heatmap = helper.activity_heatmap(selected_user, df)
#         fig, ax = plt.subplots(figsize=(10, 5))
#         sns.heatmap(user_heatmap, cmap="magma", ax=ax)
#         st.pyplot(fig)

#         # ---------------------------------------------------------
#         # 👥 Most Busy Users (for group only)
#         # ---------------------------------------------------------
#         if selected_user == 'Overall':
#             st.title('Most Busy Users')
#             name, count, new_df = helper.most_busy_users(df)
#             fig, ax = plt.subplots()
#             col1, col2 = st.columns(2)
#             with col1:
#                 ax.bar(name, count, color='#e63946')
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)

#         # ---------------------------------------------------------
#         # ☁️ Word Cloud
#         # ---------------------------------------------------------
#         st.title("Word Cloud")
#         df_wc = helper.create_wordcloud(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.imshow(df_wc)
#         ax.axis("off")
#         st.pyplot(fig)

#         # ---------------------------------------------------------
#         # 🔠 Most Common Words
#         # ---------------------------------------------------------
#         st.title("Most Common Words")
#         most_common_df = helper.most_common_words(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.barh(most_common_df[0], most_common_df[1], color='#17a2b8')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # ---------------------------------------------------------
#         # 😂 Emoji Analysis (Fixed for visibility)
#         # ---------------------------------------------------------
#         st.title("Emoji Analysis")
#         emoji_df = helper.emoji_helper(selected_user, df)
#         col1, col2 = st.columns(2)

#         with col1:
#             st.dataframe(emoji_df)

#         with col2:
#             # ✅ Ensure emoji visibility (Windows fix)
#             mpl.rcParams['font.family'] = 'Segoe UI Emoji'

#             fig, ax = plt.subplots()
#             ax.pie(
#                 emoji_df[1].head(),
#                 labels=emoji_df[0].head(),
#                 autopct="%0.2f",
#                 textprops={'fontsize': 12}
#             )
#             ax.set_title("Most Used Emojis", fontsize=14)
#             st.pyplot(fig)

#         # ---------------------------------------------------------
#         # 📘 Summary Report
#         # ---------------------------------------------------------
#         st.title("📘 Summary Report")
#         summary_text = helper.generate_summary(df, selected_user)
#         st.markdown(summary_text)

# # import matplotlib.pyplot as plt
# # import streamlit as st
# # import seaborn as sns
# # import helper
# # import preprocessor
# # import importlib   # ✅ Added to force reload of helper when changed

# # # ✅ Force Streamlit to use latest version of helper.py every run
# # importlib.reload(helper)

# # # 🧩 Streamlit Page Config
# # st.set_page_config(page_title="Samwad: WhatsApp Chat Analyser", layout="wide")
# # st.sidebar.title("Samwad")

# # uploaded_file = st.sidebar.file_uploader("Choose a file")

# # if uploaded_file is not None:
# #     bytes_data = uploaded_file.getvalue()
# #     data = bytes_data.decode("utf-8")
# #     df = preprocessor.preprocess(data)
# #     # st.dataframe(df)

# #     st.title("Top Statistics")

# #     # fetch unique members
# #     user_list = df['user'].unique().tolist()
# #     if 'group_notification' in user_list:
# #         user_list.remove('group_notification')
# #     user_list.sort()
# #     user_list.insert(0, "Overall")
# #     selected_user = st.sidebar.selectbox("Select user", user_list)

# #     if st.sidebar.button("Show Analysis"):
# #         # ---------------------------------------------------------
# #         # 📊 ALIGNED KEY STATISTICS SECTION
# #         # ---------------------------------------------------------
# #         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
# #         st.markdown("### 📊 Key Statistics")

# #         col1, col2, col3, col4 = st.columns(4)

# #         with col1:
# #             st.metric(label="Total Messages", value=num_messages)
# #         with col2:
# #             st.metric(label="Total Words", value=words)
# #         with col3:
# #             st.metric(label="Media Shared", value=num_media_messages)
# #         with col4:
# #             st.metric(label="Links Shared", value=num_links)

# #         # ---------------------------------------------------------
# #         # 📆 Monthly Timeline
# #         # ---------------------------------------------------------
# #         st.title("Monthly Timeline")
# #         timeline = helper.monthly_timeline(selected_user, df)
# #         fig, ax = plt.subplots()
# #         ax.plot(timeline['time'], timeline['message'])
# #         plt.xticks(rotation='vertical')
# #         st.pyplot(fig)

# #         # 📅 Daily Timeline
# #         st.title("Daily Timeline")
# #         daily_timeline = helper.daily_timeline(selected_user, df)
# #         fig, ax = plt.subplots()
# #         ax.plot(daily_timeline['only_date'], daily_timeline['message'])
# #         plt.xticks(rotation='vertical')
# #         st.pyplot(fig)

# #         # ---------------------------------------------------------
# #         # 🗓️ Activity Map
# #         # ---------------------------------------------------------
# #         st.title('Activity Map')
# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.header("Most Busy Day")
# #             busy_day = helper.week_activity_map(selected_user, df)
# #             fig, ax = plt.subplots()
# #             ax.bar(busy_day.index, busy_day.values, color='purple')
# #             plt.xticks(rotation='vertical')
# #             st.pyplot(fig)

# #         with col2:
# #             st.header("Most Busy Month")
# #             busy_month = helper.month_activity_map(selected_user, df)
# #             fig, ax = plt.subplots()
# #             ax.bar(busy_month.index, busy_month.values, color='orange')
# #             plt.xticks(rotation='vertical')
# #             st.pyplot(fig)

# #         # 🔥 Weekly Activity Heatmap
# #         st.title("Weekly Activity Map")
# #         user_heatmap = helper.activity_heatmap(selected_user, df)
# #         fig, ax = plt.subplots()
# #         ax = sns.heatmap(user_heatmap)
# #         st.pyplot(fig)

# #         # ---------------------------------------------------------
# #         # 👥 Most Busy Users (for group only)
# #         # ---------------------------------------------------------
# #         if selected_user == 'Overall':
# #             st.title('Most Busy Users')
# #             name, count, new_df = helper.most_busy_users(df)
# #             fig, ax = plt.subplots()
# #             col1, col2 = st.columns(2)

# #             with col1:
# #                 ax.bar(name, count, color='red')
# #                 plt.xticks(rotation='vertical')
# #                 st.pyplot(fig)
# #             with col2:
# #                 st.dataframe(new_df)

# #         # ---------------------------------------------------------
# #         # ☁️ Word Cloud
# #         # ---------------------------------------------------------
# #         st.title("Word Cloud")
# #         df_wc = helper.create_wordcloud(selected_user, df)
# #         fig, ax = plt.subplots()
# #         ax.imshow(df_wc)
# #         ax.axis("off")
# #         st.pyplot(fig)

# #         # ---------------------------------------------------------
# #         # 🔠 Most Common Words
# #         # ---------------------------------------------------------
# #         st.title("Most Common Words")
# #         most_common_df = helper.most_common_words(selected_user, df)
# #         fig, ax = plt.subplots()
# #         ax.barh(most_common_df[0], most_common_df[1])
# #         plt.xticks(rotation='vertical')
# #         st.pyplot(fig)

# #         # ---------------------------------------------------------
# #         # 😂 Emoji Analysis
# #         # ---------------------------------------------------------
# #         st.title("Emoji Analysis")
# #         emoji_df = helper.emoji_helper(selected_user, df)
# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.dataframe(emoji_df)
# #         with col2:
# #             fig, ax = plt.subplots()
# #             ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
# #             st.pyplot(fig)

# #         # ---------------------------------------------------------
# #         # 📘 Summary Report
# #         # ---------------------------------------------------------
# #         st.title("📘 Summary Report")
# #         summary_text = helper.generate_summary(df, selected_user)
# #         st.markdown(summary_text)
