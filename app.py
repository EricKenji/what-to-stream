import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import csv

POPULAR_MOVIES_URL = 'https://www.rottentomatoes.com/browse/movies_at_home/sort:popular'
POPULAR_SHOWS_URL= "https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular"
URL_ORIGIN = 'https://www.rottentomatoes.com'

app = Flask(__name__)
Bootstrap5(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/movies')
def movies():
    response = requests.get(POPULAR_MOVIES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_grid = soup.find("div", {"class": "discovery-tiles__wrap"})
    if not movie_grid:
        return render_template('movies.html', movies=[])
        
    movies_data = []
    movies = movie_grid.find_all("div", {"class": "flex-container"})

    for movie in movies:
        try:
            title = movie.find("span", {"class": "p--small"})
            critics_score = movie.find("rt-text", {"slot": "criticsScore"})
            audience_score = movie.find("rt-text", {"slot": "audienceScore"})
            img_element = movie.find("rt-img", {"class": "posterImage"})
            link = movie.find("a", {"data-qa": "discovery-media-list-item-caption"})
            link_end = link.get("href", "")
            slug = link_end.split("/m/")[1] if "/m/" in link_end else ""


            if all([title, critics_score, audience_score, img_element, link]):
                movies_data.append({
                    'title': title.text.strip(),
                    'critics_score': critics_score.text.strip(),
                    'audience_score': audience_score.text.strip(),
                    'img_url': img_element.get("src", ""),
                    'url': URL_ORIGIN + link_end,
                    'slug': slug
                })
        except AttributeError:
            continue
    return render_template('movies.html', movies=movies_data)

@app.route('/movie_details/<path:slug>')
def movie_details(slug):
    url = f'https://www.rottentomatoes.com/m/{slug}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_show_data = soup.find("div", {"id": "movie-overview"})
    if not movie_show_data:
        return render_template("details.html", error="Movie/Show not found")

    is_movie = False
    if '/m/' in url:
        is_movie = True


    title = ""
    critic_score = "N/A"
    audience_score = "N/A"
    synopsis = "No synopsis available"
    platforms = []
    critic_consensus = "No critics consensus available"
    aud_consensus = "No audience consensus available"
    img_url = ""

    try:
        hero = movie_show_data.find("media-hero")
        if hero:
            img_element = hero.find("rt-img", {"slot": "iconic"})
            if img_element and img_element.has_attr("src"):
                src_value = img_element["src"]
                img_urls = [url.strip() for url in src_value.split(",")]
                img_url = img_urls[-1]

        if movie_show_data.find("sr-text"):
            title = movie_show_data.find("sr-text").text.strip()

        if movie_show_data.find("rt-text", {"slot": "criticsScore"}):
            critic_score = movie_show_data.find("rt-text", {"slot": "criticsScore"}).text.strip()

        if movie_show_data.find("rt-text", {"slot": "audienceScore"}):
            audience_score = movie_show_data.find("rt-text", {"slot": "audienceScore"}).text.strip()

        synopsis_div = movie_show_data.find("div", {"slot": "description"})
        if synopsis_div:
            synopsis = synopsis_div.text.strip()

        where_to_watch_data = movie_show_data.find_all("where-to-watch-meta")
        if where_to_watch_data:
            platforms = [platform.find("span").text.strip() for platform in where_to_watch_data if platform.find("span")]

        critic_consensus_section = movie_show_data.find("div", id="critics-consensus")
        if critic_consensus_section and critic_consensus_section.find("p"):
            critic_consensus = critic_consensus_section.find("p").text.strip()

        aud_consensus_section = movie_show_data.find("div", id="audience-consensus")
        if aud_consensus_section and aud_consensus_section.find("p"):
            aud_consensus = aud_consensus_section.find("p").text.strip()

    except AttributeError as e:
        print(f"Error processing movie data: {e}")
    return render_template("details.html",
                         title=title,
                         critic_score=critic_score,
                         audience_score=audience_score,
                         synopsis=synopsis,
                         platforms=platforms,
                         critic_consensus=critic_consensus,
                         aud_consensus=aud_consensus,
                         img_url=img_url,
                           is_movie=is_movie)

@app.route('/shows')
def shows():
    response = requests.get(POPULAR_SHOWS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    show_grid = soup.find("div", {"class": "discovery-tiles__wrap"})
    if not show_grid:
        return render_template('shows.html', movies=[])

    shows_data = []
    shows = show_grid.find_all("div", {"class": "flex-container"})

    for show in shows:
        try:
            show_title = show.find("span", {"class": "p--small"})
            critics_score = show.find("rt-text", {"slot": "criticsScore"})
            audience_score = show.find("rt-text", {"slot": "audienceScore"})
            img_element = show.find("rt-img", {"class": "posterImage"})
            show_link = show.find("a", {"data-qa": "discovery-media-list-item-caption"})
            link_end = show_link.get("href", "")
            slug = link_end.split("/tv/")[1] if "/tv/" in link_end else ""

            if all([show_title, critics_score, audience_score, img_element, show_link]):
                shows_data.append({
                    'show_title': show_title.text.strip(),
                    'critics_score': critics_score.text.strip(),
                    'audience_score': audience_score.text.strip(),
                    'img_url': img_element.get("src", ""),
                    'show_url': URL_ORIGIN + show_link.get("href", ""),
                    'slug': slug
                })
        except AttributeError:
            continue

    return render_template('shows.html', shows=shows_data)

@app.route('/show_details/<path:slug>')
def show_details(slug):
    url = f'https://www.rottentomatoes.com/tv/{slug}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_show_data = soup.find("div", {"id": "tv-series-overview"})
    if not movie_show_data:
        return render_template("details.html", error="Movie/Show not found")

    title = ""
    critic_score = "N/A"
    audience_score = "N/A"
    synopsis = "No synopsis available"
    platforms = []
    critic_consensus = "No critics consensus available"
    aud_consensus = "No audience consensus available"
    img_url = ""
    seasons = 0

    try:
        hero = movie_show_data.find("media-hero")
        if hero:
            img_element = hero.find("rt-img", {"slot": "iconic"})
            if img_element and img_element.has_attr("src"):
                src_value = img_element["src"]
                img_urls = [url.strip() for url in src_value.split(",")]
                img_url = img_urls[-1]

        if movie_show_data.find("sr-text"):
            title = movie_show_data.find("sr-text").text.strip()

        if movie_show_data.find("rt-text", {"slot": "criticsScore"}):
            critic_score = movie_show_data.find("rt-text", {"slot": "criticsScore"}).text.strip()

        if movie_show_data.find("rt-text", {"slot": "audienceScore"}):
            audience_score = movie_show_data.find("rt-text", {"slot": "audienceScore"}).text.strip()

        synopsis_div = movie_show_data.find("div", {"slot": "description"})
        if synopsis_div:
            synopsis = synopsis_div.text.strip()

        where_to_watch_data = movie_show_data.find_all("where-to-watch-meta")
        if where_to_watch_data:
            platforms = [platform.find("span").text.strip() for platform in where_to_watch_data if platform.find("span")]

        critic_consensus_section = movie_show_data.find("div", id="critics-consensus")
        if critic_consensus_section and critic_consensus_section.find("p"):
            critic_consensus = critic_consensus_section.find("p").text.strip()

        aud_consensus_section = movie_show_data.find("div", id="audience-consensus")
        if aud_consensus_section and aud_consensus_section.find("p"):
            aud_consensus = aud_consensus_section.find("p").text.strip()

        seasons_section = movie_show_data.find_all("tile-season", {"slot":"tile"})
        seasons = len(seasons_section)

    except AttributeError as e:
        print(f"Error processing movie data: {e}")


    return render_template("details.html",
                         title=title,
                         critic_score=critic_score,
                         audience_score=audience_score,
                         synopsis=synopsis,
                         platforms=platforms,
                         critic_consensus=critic_consensus,
                         aud_consensus=aud_consensus,
                         img_url=img_url,
                           seasons=seasons)



@app.route('/shows/export_csv')
def export_shows_csv():
    response = requests.get(POPULAR_SHOWS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    show_grid = soup.find("div", {"class": "discovery-tiles__wrap"})
    if not show_grid:
        return render_template('shows.html', movies=[])

    shows_data = []
    shows = show_grid.find_all("div", {"class": "flex-container"})

    for show in shows:
        try:
            show_title = show.find("span", {"class": "p--small"})
            critics_score = show.find("rt-text", {"slot": "criticsScore"})
            audience_score = show.find("rt-text", {"slot": "audienceScore"})
            img_element = show.find("rt-img", {"class": "posterImage"})
            show_link = show.find("a", {"data-qa": "discovery-media-list-item-caption"})

            if all([show_title, critics_score, audience_score, img_element, show_link]):
                shows_data.append({
                    'show_title': show_title.text.strip(),
                    'critics_score': critics_score.text.strip(),
                    'audience_score': audience_score.text.strip(),
                    'img_url': img_element.get("src", ""),
                    'show_url': URL_ORIGIN + show_link.get("href", "")
                })
        except AttributeError:
            continue

    with open('show_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['show_title', 'critics_score', 'audience_score', 'img_url', 'show_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(shows_data)

    return render_template('shows.html', shows=shows_data)


@app.route('/movies/export_csv')
def export_movies_csv():
    response = requests.get(POPULAR_MOVIES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_grid = soup.find("div", {"class": "discovery-tiles__wrap"})
    if not movie_grid:
        return render_template('movies.html', movies=[])

    movies_data = []
    movies = movie_grid.find_all("div", {"class": "flex-container"})

    for movie in movies:
        try:
            title = movie.find("span", {"class": "p--small"})
            critics_score = movie.find("rt-text", {"slot": "criticsScore"})
            audience_score = movie.find("rt-text", {"slot": "audienceScore"})
            img_element = movie.find("rt-img", {"class": "posterImage"})
            link = movie.find("a", {"data-qa": "discovery-media-list-item-caption"})

            if all([title, critics_score, audience_score, img_element, link]):
                movies_data.append({
                    'title': title.text.strip(),
                    'critics_score': critics_score.text.strip(),
                    'audience_score': audience_score.text.strip(),
                    'img_url': img_element.get("src", ""),
                    'url': URL_ORIGIN + link.get("href", "")
                })
        except AttributeError:
            continue

    with open('movie_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'critics_score', 'audience_score', 'img_url', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies_data)

    return render_template('movies.html', movies=movies_data)

if __name__ == '__main__':
    app.run(debug=True)