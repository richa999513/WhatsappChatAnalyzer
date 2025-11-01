# cd "C:\Users\RICHA MISHRA\GURUKUL\python\my-python-project\src"

import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocess.preprocess(data)
    # st.dataframe(df)

    # fetch user names
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,word,num_media_msg,num_link= helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(word)

        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)

        with col4:
            st.header("Links Shared")
            st.title(num_link) 
        
        # Monthly time line 
        st.title("Monthly Timeline")
        time_line = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(time_line['time'],time_line['message'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Dialy TimeLine
        st.title("Dialy Timeline")
        time_line = helper.dialy_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(time_line['only_date'],time_line['message'],color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2=st.beta_columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        # find the busiest users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,n_df = helper.fetch_most_busy_users(df)
            fig,ax = plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(n_df)

        # wordcloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df = helper.most_common_words(selected_user, df)
        # st.dataframe(most_common_df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
