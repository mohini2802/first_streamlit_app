import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")
   
streamlit.header(' Breakfast Favorties')
streamlit.text('🥣 Omega 3 &  Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
fruits_to_show

# streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please enter fruit you would like information about.")
    else:
         back_from_action = get_fruityvice_data(fruit_choice)
         streamlit.dataframe(back_from_action)
    
except URLError as e:
    streamlit.error()

  
def insert_row_snowflake(new_fruit_1):
   my_cnx.cursor().execute("insert into pc_rivery_db.public.fruit_load_list values(new_fruit_1)")
   return 'Thank you for adding'+ new_fruit_1

def get_fruit_list():
    my_cnx.cursor().execute("select * from pc_rivery_db.public.fruit_load_list")
    my_data_row = my_cur.fetchall()
    streamlit.text("The fruit load list contains:")
    return my_data_row

try:
    if streamlit.button("View Our Fruit List - Add Your Favourites!"):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        bck_frm_fnctn_get_list = get_fruit_list()
        streamlit.dataframe(bck_frm_fnctn_get_list)
        add_fruit = streamlit.text_input('What fruit would you like to add?')
        insert_row_snowflake(add_fruit)
        streamlit.dataframe(my_data_row)
    
except URLError as e:
    streamlit.error()

