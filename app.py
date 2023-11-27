import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose your File")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respect to ", user_list)
    # = st.sidebar.button('Show Analysis')
    if st.sidebar.button('Show Analysis'):
        num_messages, words,number_of_media, link = helper.fetch_stats(selected_user, df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total media Shared")
            st.title(number_of_media)
        with col4:
            st.header("Links")
            st.title(link)

        if selected_user =='Overall':
            st.title("Busiest User")
            col1,col2 = st.columns(2)
            x, user_msg_percent= helper.busiest_user(df)
            fig,ax =plt.subplots()


            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                # st.title("")
                st.dataframe(user_msg_percent)

        #WordCloud
        st.title(f"{selected_user} WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

            #Most Used Words
        st.title("Most Common Words")

        most_common_words_df = helper.most_common_words(selected_user,df)
        #st.dataframe(most_common_words_df)  

        fig,ax = plt.subplots()
        ax.barh(most_common_words_df[0],most_common_words_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

        st.title("Weeakly Activity")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        st.title("Timeline")
        col1,col2 = st.columns(2)
        #Monthly Timeline
        with col1: 
            timeline = helper.monthly_timeline(selected_user,df)
            st.header("Monthly Timeline")
            fig, ax = plt.subplots()
            ax.plot(timeline['time'],timeline['messages'])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)


        #Weekly Timeline
        with col2:
            st.header("Weekly Timeline")
            weekly_timeline = helper.weekly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(weekly_timeline.index,weekly_timeline.values)
            st.pyplot(fig)

        # #Monthly
        # st.title("Monthly Activity")
        # monthly_activity = helper.monthly_activity(selected_user,df)
        # fig,ax = plt.subplots()
        # plt.xticks(rotation="vertical")
        # ax.bar(monthly_activity.index,monthly_activity.values)
        # st.pyplot(fig)

        st.title("Activity MAP")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Daily Activity")
            daily_timeline = helper.daily_timeline(selected_user,df)
            fig,ax = plt.subplots()
            plt.xticks(rotation="vertical")
            ax.plot(daily_timeline['daily'], daily_timeline['messages'])
            st.pyplot(fig)
        with col2:
            st.header("Monthly Activity")
            monthly_activity = helper.monthly_activity(selected_user,df)
            fig,ax = plt.subplots()
            plt.xticks(rotation="vertical")
            ax.bar(monthly_activity.index,monthly_activity.values)
            st.pyplot(fig)