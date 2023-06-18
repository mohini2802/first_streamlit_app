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
  
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
                                      
                                                                                                 
                                             

                     
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)
def insert_row_snowflake(new_fruit):
   my_cnx.cursor().execute("insert into pc_rivery_db.public.fruit_load_list values(new_fruit)")
   return 'Thank you for adding'+ new_fruit
                          
if streamlit.button('Add a fruit to the list'):
    add_fruit = streamlit.text_input('What fruit would you like to add') 
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_fruit)
    streamlit.text(back_from_function)

    
streamlit.header("View Our Fruit List - Add Your Favourites!")
if streamlit.button("Get Fruit List"):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   with my_cnx.cursor() as my_cur:
      my_cur.execute("delete from pc_rivery_db.public.fruit_load_list where fruit_name like 'test' or fruit_name ='from streamlit'")
      my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
      my_data_row = my_cur.fetchall()
                                                                                 
streamlit.dataframe(my_data_row)


# --------------------------------------------
import streamlit
import snowflake.connector
import pandas
streamlit.title('Zena\'s Amazing Athleisure Catalog')
# connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()
# put the dafta into a dataframe
df = pandas.DataFrame(my_catalog)
# temp write the dataframe to the page so I Can see what I am working with
# streamlit.write(df)
# put the first column into a list
color_list = df[0].values.tolist()
# print(color_list)
# Let's put a pick list here so they can pick the color
option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))
# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'
# use the option selected to go back and get all the info from the database
my_cur.execute(f"select direct_url, price, size_list, upsell_product_desc from catalog_for_website")
df2 = my_cur.fetchone()
streamlit.image(
df2[0],
width=400,
caption= product_caption
)
streamlit.write('Price: ', df2[1])
streamlit.write('Sizes Available: ',df2[2])
streamlit.write(df2[3])

                     

