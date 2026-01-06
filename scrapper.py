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

html="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top 25 IMDb Movies</title>

    <!-- Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg: #0e0f13;
            --card: #16181f;
            --text: #e6e6eb;
            --muted: #a0a3b1;
            --accent: #f5c518; /* IMDb gold */
            --border: rgba(255,255,255,0.06);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 40px 16px;
            background: radial-gradient(circle at top, #1b1e27, var(--bg));
            color: var(--text);
            font-family: 'Inter', system-ui, sans-serif;
        }

        .container {
            max-width: 1100px;
            margin: auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.8rem;
            margin: 0;
            letter-spacing: 0.5px;
        }

        header p {
            color: var(--muted);
            margin-top: 10px;
            font-size: 1rem;
        }

        .card {
            background: linear-gradient(180deg, #1b1e27, var(--card));
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.45);
            border: 1px solid var(--border);
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 700px;
        }

        thead th {
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--muted);
            padding: 14px 12px;
            border-bottom: 1px solid var(--border);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        tbody tr {
            transition: background 0.25s ease, transform 0.25s ease;
        }

        tbody tr:hover {
            background: rgba(255,255,255,0.03);
            transform: translateY(-2px);
        }

        tbody td {
            padding: 16px 12px;
            border-bottom: 1px solid var(--border);
            font-size: 0.95rem;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        .rank {
            font-weight: 600;
            color: var(--accent);
        }

        .title {
            font-weight: 500;
        }

        .rating {
            font-weight: 600;
            color: var(--accent);
        }

        footer {
            text-align: center;
            margin-top: 30px;
            color: var(--muted);
            font-size: 0.85rem;
        }

        @media (max-width: 768px) {
            header h1 {
                font-size: 2.2rem;
            }
        }
    </style>
</head>
<body>

<div class="container">

    <header>
        <h1>Top 25 Movies to Watch</h1>
        <p>Curated from IMDb • Updated Weekly</p>
    </header>

    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Title</th>
                    <th>Year</th>
                    <th>Rating</th>
                </tr>
            </thead>
            <tbody>
                {% for j in range(25) %}
                <tr>
                    <td class="rank">{{ j + 1 }}</td>
                    <td class="title">{{ df['Title'][j] }}</td>
                    <td>{{ df['Year'][j] }}</td>
                    <td class="rating">⭐ {{ df['Rating'][j] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <footer>
        Built with Python • BeautifulSoup • Jinja2 • GitHub Pages
    </footer>

</div>

</body>
</html>

"""
temp=Template(html)
html=temp.render(df=df)

with open('index.html','w',encoding='utf-8') as f:
    f.write(html)