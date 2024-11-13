# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
import requests

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df= my_dataframe.to_pandas()
st.dataframe(pd_df)
st.warning('Por cerrar.')
st.stop()


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
################################
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen+'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_chosen)

####################################################
        
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df= st.dataframe(data= smoothiefroot_response.json(),use_container_width=True)

  #  st.write(ingredients_string)
    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""','"""+ title+"""')"""

  #  st.write(my_insert_stmt)



    time_to_insert= st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+title, icon="✅")


