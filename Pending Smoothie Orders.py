# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col, when_matched
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Pendientes smoothie! :cup_with_straw:")
st.write(
    """Ordenes pendientes!
    """
)
###
##title = st.text_input("Name on Smoothie", "")
###st.write("The name on your smoothie is ", title)
####
session = get_active_session()

#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)


    submitted =  st.button('Submit')
    
    if submitted:
    
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success("Someone clicked the button", icon= "👍")
        except:
            
            st.write(  """error!
        """)
    st.write(  """error2!""")


else:

     st.success("No hay ordenes pendientes", icon= "👍")


