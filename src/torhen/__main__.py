from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .utils import ten_maximum_seeders
from .save_drive import stream_upload
import argparse

class Scrapper:

    def __init__(self, search_key) -> None:
        self.search_key = search_key
        options = Options()
        options.add_argument("--headless") 
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f"https://www.limetorrents.pro/search/all/{self.search_key}")
        self.result = []
        self.magnet_link = ""


    def __enter__(self) -> None:
        
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find("table",attrs={"class":"table2"})
        data_rows = table.select("tbody tr")
        data = [[cell.text.strip() for cell in row.select("td")] for row in data_rows]
        clean_data = list(filter(None, data))
        seeder_nb = [str(seed[4].replace(",","")) for seed in clean_data ]
        maximums = ten_maximum_seeders(seeder_nb)
        max_index = [seeder_nb.index(e) for e in maximums]
        best_torrent = ["-".join(clean_data[mi][0].split()) for mi in max_index]
        links = [link.get('href') for link in table.find_all('a')]

        
        all_filtered_links= [item for item in links if item.startswith('/')]

        # Get best seeder torrent links
        for link in all_filtered_links:
            for a , b in enumerate(best_torrent):
                if b in link:

                    self.result.append(f'{link} | Size : {clean_data[a][2]} | Seeders : {clean_data[a][3]}'[1:])

        for x, y in enumerate(self.result):
            print(f'{x+1}- {y}')

    def __exit__(self, exc_type, exc_value, traceback):
        # self.driver.close()
        while True:
            user_input = input('Choose a torrent number > ')
            self.driver.get(f"https://www.limetorrents.pro/{self.result[int(user_input) - 1].split(' | ')[0]}")
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            links = soup.find_all("a")
            for link in links:
                if "magnet:" in str(link):
                    self.magnet_link = link
                    break
            
            stream_upload(str(self.magnet_link['href']))


parser = argparse.ArgumentParser()
parser.add_argument('--search', type=str, required=True)
args = parser.parse_args()

with Scrapper(search_key=args.search) as scrap:
    pass
