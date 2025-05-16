# import requests
# from bs4 import BeautifulSoup
#
#
# url = 'https://www.rottentomatoes.com/m/nonnas'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# movie_data= soup.find("div", {"id": "movie-overview"})
# hero = movie_data.find("media-hero")
# img_url = hero.find("img").get("src", "")
# movie_title = movie_data.find("sr-text").text.strip()
# critic_score = movie_data.find("rt-text", {"slot":"criticsScore"}).text.strip()
# audience_score = movie_data.find("rt-text", {"slot":"audienceScore"}).text.strip()
# synopsis = movie_data.find("div", {"slot": "description"}).text.strip()
# where_to_watch_data = movie_data.find_all("where-to-watch-meta")
# platforms = [platform.find("span").text.strip() for platform in where_to_watch_data]
# census_section = movie_data.find("div", id="critics-consensus")
# critic_census = census_section.find("p").text.strip()
# print(critic_score)
# print(audience_score)
# print(img_url)
# print(hero)

url = '/m/nonnas'
slug = url.split("/m/")[1] if "/m/" in url else ""

print(slug)
