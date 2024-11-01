# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose a fruit you want in your custom smoothie.
    """
)

# option=st.selectbox('What is your favourite fruit??',
#                    ('Banana','Apple','Kiwi','mango'))

# st.write('you favourite fruit is ',option)

name_on_order = st.text_input('Name on Smoothie : ')
# st.write("Name of your smoothie will be :",name_on_order)

# session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose upto 5 fruits',my_dataframe,max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string+"""','"""+name_on_order+"""')"""
    # st.write(my_insert_stmt) 
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+name_on_order+'!!', icon="✅")


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
# st.text(fruityvice_response.json())
# fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    


