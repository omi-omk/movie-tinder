import os
import requests
from bs4 import BeautifulSoup
from database import Database
from urllib.parse import urljoin
import time
import random
from imdb import IMDb
from selenium import webdriver

class IMDbScraper:
    def __init__(self):
        self.base_url = "https://www.imdb.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            "Accept-Language": "en-IN;q=0.8,en;q=0.7"
        }
        self.db = Database()
        


    def get_soup(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(random.uniform(2, 5))

    def download_poster(self, poster_url, title):
        filename = title.replace(' ', '_').lower() + '.jpg'
        poster_path = os.path.join('static', 'posters')
        os.makedirs(os.path.join('static', 'posters'), exist_ok=True)

        try:
            response = requests.get(poster_url)
            if response.status_code == 200:
                # Create a valid filename
                filename = f"{title.replace(' ', '_')}.jpg"
                filepath = os.path.join(poster_path, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath  # Return the path where the poster is saved
            else:
                print(f"Failed to download poster for {title}")
                return None
        except Exception as e:
            print(f"Error downloading poster for {title}: {e}")
            return None

    def scrape_movie_details(self, movie_url):
        try:
            print(f"Scraping movie: {movie_url}")
            soup = self.get_soup(movie_url)
            
            # Title
            title_elem = soup.find('div', class_= 'sc-70a366cc-0 bxYZmb')
            if title_elem:
                title = title_elem.find('span', class_="hero__primary-text").text.strip()

            else:
                title = None
            
            # Year
            year_div = soup.find( 'div', class_= "sc-70a366cc-0 bxYZmb" )
            if year_div:
                link_tag = year_div.find('a', class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color")

                if link_tag:
                    year = link_tag.text.strip()  # Extract the text and remove any whitespace
                else:
                    year = None
            else:
                year = None

            # Rating
            rating_elem = soup.find('span', {'class': 'sc-d541859f-1 imUuxf'})
            rating = float(rating_elem.text) if rating_elem else 7.0
            
            # Description/Plot
            plot_elem = soup.find('span', {'data-testid': 'plot-xl'})
            if not plot_elem:
                plot_elem = soup.find('div', class_='sc-16ede01-8')
            plot = plot_elem.text.strip() if plot_elem else "No description available."
            
            # Genres
            genre_elems = soup.find_all('span', {'class': 'ipc-chip__text'})
            genres = ' / '.join([g.text for g in genre_elems[:3]]) if genre_elems else "Drama"
            
            # Director
            director_elem = soup.find('a', {'class': 'ipc-metadata-list-item__list-content-item'})
            director = director_elem.text if director_elem else "Unknown Director"
            
            # Cast
            cast_elems = soup.find_all('a', {'data-testid': 'title-cast-item__actor'})
            if not cast_elems:
                cast_elems = soup.find_all('a', class_='sc-bfec09a1-1')
            cast = ', '.join([a.text for a in cast_elems[:3]]) if cast_elems else "Unknown Cast"
            
            # Keywords
            keyword_elems = soup.find_all('span', {'class': 'ipc-chip__text'})
            keywords = ', '.join([k.text for k in keyword_elems[3:6]]) if len(keyword_elems) > 3 else ""
            
            # Poster
            ia = IMDb()
            search_results = ia.search_movie(title)
            if not search_results:
                print(f"No results found for {title}")
                return
            # Get the first result
            movie = search_results[0]
            ia.update(movie)

            poster_url = movie.get('full-size cover url', '')
            poster_path = self.download_poster(poster_url, title)
            
            print(title)
            # Save to database
            self.db.add_movie(
                title=title,
                genres=genres,
                description=plot,
                rating=rating,
                year=year,
                director=director,
                cast=cast,
                keywords=keywords,
                poster=poster_path
            )
            
            print(f"Successfully scraped: {title}")
            return True
            
        except Exception as e:
            print(f"Error scraping movie: {str(e)}")
            return False

    def scrape_movies(self):
        try:
            # List of IMDb URLs to scrape from
            urls = [
                "https://www.imdb.com/list/ls004221468/",  # Most Popular Bollywood movies
                "https://www.imdb.com/chart/top-english-movies/",  # Most Popular Hollywood movies
            ]
            
            movies_scraped = 0
            max_movies = 550
            
            driver = webdriver.Chrome()
            for url in urls:

                if movies_scraped >= max_movies:
                    break
                
                print(f"\nScraping from: {url}")
                driver.get(url)
                time.sleep(5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                
                movie_links = soup.find_all('a', {'class': 'ipc-title-link-wrapper'})

                for link in movie_links:
                    if movies_scraped >= max_movies:
                        break 

                    movie_url = urljoin(self.base_url, link['href'])
                    print(movie_url)
                    success = self.scrape_movie_details(movie_url)
                    
                    if success:
                        movies_scraped += 1
                        print(f"Progress: {movies_scraped}/{max_movies} movies")
                        # Random delay between requests
                        time.sleep(random.uniform(2, 4))

            driver.quit()    
            print(f"\nFinished scraping! Total movies: {movies_scraped}")
            
        except Exception as e:
            print(f"Error in scrape_movies: {str(e)}")

if __name__ == "__main__":
    scraper = IMDbScraper()
    scraper.scrape_movies()
    