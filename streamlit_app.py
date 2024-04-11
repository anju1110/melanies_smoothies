# Import python packages
import streamlit as st
import requests
import numpy
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your cutstom Smoothie!
    """
)

name_on_order = st.text_input(
    'Name on Smoothie:')


st.write('The name on your smoothie will be:', name_on_order)

from snowflake.snowpark.functions import col
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#Convert the snowpark into Pandas dataframe to use loc function
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string=''
    for  f in ingredients_list:
        ingredients_string+=f+ ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == f, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', f,' is ', search_on, '.')
        
        st.subheader(f + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + f)
        #st.text(fruityvice_response.json())
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt="""insert into smoothies.public.orders(ingredients,name_on_order ) values('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered,{name_on_order}!")

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# #st.text(fruityvice_response.json())
# fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
