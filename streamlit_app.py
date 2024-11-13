import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)
title = st.text_input("Name on Smoothie", "")
st.write("The name on your smoothie is ", title)

# Connect to Snowflake and retrieve fruit options
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# User selects ingredients for the smoothie
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients :'
    , my_dataframe
    , max_selections=5
)

# If user has selected ingredients, proceed to fetch nutritional info
if ingredients_list:
    ingredients_string = ''
    fruityvice_data = []
    smoothiefroot_data = []
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # Retrieve 'SEARCH_ON' value for the selected fruit
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # Fetch nutrition info from FruityVice API
        try:
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
            fruityvice_response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
            fruityvice_data.append(fruityvice_response.json())  # Store the JSON data
            st.subheader(f"{fruit_chosen} Nutrition Information (FruityVice)")
            st.dataframe(fruityvice_response.json(), use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data for {fruit_chosen} from FruityVice: {e}")
            st.write(f"Response content: {fruityvice_response.text}")
        
        # Fetch nutrition info from SmoothieFroot API
        try:
            smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
            smoothiefroot_response.raise_for_status()
            smoothiefroot_data.append(smoothiefroot_response.json())
            st.subheader(f"{fruit_chosen} Nutrition Information (SmoothieFroot)")
            st.dataframe(smoothiefroot_response.json(), use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data for {fruit_chosen} from SmoothieFroot: {e}")
            st.write(f"Response content: {smoothiefroot_response.text}")
        
    # Insert order details into Snowflake when user submits
    my_insert_stmt = """ 
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('""" + ingredients_string + """','""" + title + """')
    """
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your smoothie is ordered, {title}!', icon="✅")
        except Exception as e:
            st.error(f"Failed to insert order into the database: {e}")
