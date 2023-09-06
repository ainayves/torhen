from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from utils import ten_maximum_seeders

class Scrapper:

    def __init__(self, search_key) -> None:
        self.search_key = search_key
        options = Options()
        options.add_argument("-headless") 
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(f"https://www.limetorrents.lol/search/all/{self.search_key}/")


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
        
        all_filtered_links= [item for item in links if not item.startswith('/')]

        # Get best seeder torrent links
        result = []
        for link in all_filtered_links:
            for b in best_torrent:
                if b in link:
                    result.append(link)

        for x, y in enumerate(result):
            print(f'{x+1}- {y}')

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()
    
    def best_seeded(self):
        pass


with Scrapper(search_key="oppenheimer") as scrap:
    print("traitement ...")


        


