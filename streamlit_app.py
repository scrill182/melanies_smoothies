# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response).jason())

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)
###
title = st.text_input("Name on Smoothie", "")
st.write("The name on your smoothie is ", title)
####
cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredientts :'
    , my_dataframe
    ,max_selections=5
)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string= ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '

  #  st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""','"""+ title+"""')"""

  #  st.write(my_insert_stmt)

    time_to_insert= st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+title, icon="✅")


