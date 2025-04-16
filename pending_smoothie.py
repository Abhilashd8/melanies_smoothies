# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# helpful_links = [
#     "https://docs.streamlit.io",
#     "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
#     "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
#     "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
# ]

st.title(":cup_with_straw: Pending Smoothie Orders!:cup_with_straw:")

st.write(" Orders that need to filled")


session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0)
#st.write(my_dataframe)

if my_dataframe.count()>0:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        #st.success('Someone clicked the button',icon = '👍')
    
        try:
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            #st.write(edited_dataset)
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         ,[when_matched().update({'ORDER_FILLED':edited_dataset['ORDER_FILLED']})]
                    )
            st.success('Order(s) is updated',icon = '👍')
        except:
            st.write('Something went wrong.')
else:
    st.success('There are no pendig orders right now',icon = '👍')
