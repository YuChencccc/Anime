import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


st.title('🤖️Anime Ratings Analysis & 🧚Recommendeing System')


df_anime = pd.read_csv('anime.csv')
df_anime.dropna(subset=['type'], inplace=True)
df_anime.dropna(subset=['genre'], inplace=True)
df_anime.dropna(subset=['rating'], inplace=True)

df_anime=df_anime[~df_anime['episodes'].isin(["Unknown"])] 
df_anime['episodes'] = df_anime['episodes'].astype('int')
df_anime = df_anime.sample(5000)

 
from PIL import Image
image = Image.open('anime.jpg')
caption= st.write('Hello, *Anime!* :sunglasses:')
st.image(image, caption)


rating_filter = st.sidebar.slider('Anime rating:', 1.0, 10.0, 5.0)
df_anime= df_anime[df_anime.rating >= rating_filter]


episodes_filter = st.sidebar.radio(
    'Choose Number of episodes',
    ('Short(<20)','Medium(20-100)','Long(>100)','All length')
)
if episodes_filter == 'Short(<20)':
    df_anime = df_anime[df_anime.episodes <= 20]
if episodes_filter == 'Long(>100)':
    df_anime= df_anime[df_anime.episodes > 100]
if episodes_filter == 'Medium(20-100)':
    df_anime = df_anime[(df_anime.episodes > 20)&(df_anime.episodes <= 100)]
        



fig,ax = plt.subplots(figsize = (10,6))

member = df_anime.sort_values(by='members', ascending = False)
member10 = member.head(10)

bar_colors = ['firebrick','maroon','brown','salmon','tomato','rosybrown','lightcoral','indianred','darksalmon','mistyrose']

member10chat = member10['members']

member10chat.plot(kind="bar",color=bar_colors,edgecolor="snow",stacked=True)
plt.xlabel('Anime name')
plt.ylabel('Total members')

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
data = member10

tab1.subheader("Top Animes Based on rating members")
tab1.pyplot(fig)

st.write('**Is there any *relationship* between rating and members?**')
expander = st.expander("See explanation")
expander.write("""
    The chart above shows top 10 rating members within the range users selected.
    Since low rating has more members and high has less,
    we guess there is a negative association.
    The sample is selected *at random*.
""")

tab2.subheader("A tab with the data")
tab2.write(data)



#genre fig
df3 = pd.read_csv('anime3.csv')
st.subheader('Popular Genre tags')

genre_filter = st.multiselect(
    'genre selector',
     df3.genre.unique(),
     df3.genre.head(10)
     )

df3 =df3 = df3[df3.genre.isin(genre_filter)]
df3 = df3[['name','genre']].groupby('genre').count()

fig, ax = plt.subplots(figsize = (10,6))
genre_num = df3.sort_values(by='name')

genre_chat = genre_num['name']
genre_chat.plot(kind="barh",color=bar_colors,edgecolor="snow",stacked=True)
plt.xlabel('number of anime')
plt.ylabel('genre of anime')
st.pyplot(fig)

st.write('**Which genre is the *most popular* one within the range users selected?**')
expander = st.expander("See explanation")
expander.write("""
    The chart above shows popular genre tags within the range users selected.
    The genre tag on the top is the most popular one.
    The sample is selected *at random*.
""")


df = pd.read_csv('anime2.csv')
df_type = df[['name','type']].groupby('type').count()
df_type['name']= df_type['name']/len(df)

fig1, ax = plt.subplots(figsize = (10,10))
pie_colors = ['rosybrown','lightcoral','hotpink','palevioletred','pink','mistyrose']
df_type.plot.pie(subplots=True,ax=ax, autopct= '%.2f%%', fontsize=13,colors = pie_colors)
plt.ylabel('types')
plt.title('Anime Categories Distribution ')
st.pyplot(fig1)



fig2, ax = plt.subplots(figsize = (10,6))
df_rating = df['rating']

df_rating.plot(kind="hist",bins=20,color="palevioletred",edgecolor="snow",density=True,label="hist",stacked=True)
df_rating.plot(kind="kde",color="darkslateblue",label="distribution of rating")
plt.xlabel('rating')
plt.ylabel('total')
plt.title('Anime Average Rating Distribution ')
st.pyplot(fig2)