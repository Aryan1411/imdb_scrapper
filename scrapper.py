import pandas as pd
from jinja2 import Template
import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.5"
}
data = requests.get(url,headers=headers)
print(data.status_code)

html = data.text

aman= BeautifulSoup(html,'html.parser')
item=aman.find_all('li', class_='ipc-metadata-list-summary-item')
name=[]
year=[]
time=[]
rating=[]
for i in item:
  name.append(i.find('h3', class_='ipc-title__text').text)
  year.append(i.find_all('div',class_='hTMtRz')[0].find_all('span')[0].text)
  time.append(i.find_all('div',class_='hTMtRz')[0].find_all('span')[1].text)
  rating.append(i.find_all('div',class_='hTMtRz')[0].find_all('span')[2].text)

df=pd.DataFrame({
    'Title':name,
    'Year':year,
    'Time':time,
    'Rating':rating
})
df.to_csv('imdb_top_movies.csv', index=False)

html="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>This is top 25 movies list to watch</h1>
    <table border="1">
        <tr>
            <th>Rank</th>
            <th>Title</th>
            <th>Year</th>
            <th>Rating</th>
        </tr>
        {% for j in range(25) %}
        <tr>
            <td>{{j+1}}</td>
            <td>{{df['Title'][j]}}</td>
            <td>{{df['Year'][j]}}</td>
            <td>{{df['Rating'][j]}}</td>
        </tr>
        {%endfor%}
    </table>
        
    
</body>
</html>
"""
temp=Template(html)
html=temp.render(df=df)

with open('index.html','w',encoding='utf-8') as f:
    f.write(html)