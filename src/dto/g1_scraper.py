import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import random
from fake_useragent import UserAgent
from service.save_database import Database


ua = UserAgent()
headers = {"User-Agent": ua.random}


class G1Scraper():
    def get_news(self, period):
        last_page = 1
        news_list = []
        for pagina in range(1, self.get_pages_news(period)):
            try:
                res = requests.get(f"https://g1.globo.com/ultimas-noticias/index/feed/pagina-{pagina}.ghtml", timeout = 20)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina}: {e}")
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="feed-post-body")
            for article in articles:
                last_page = pagina
                title_tag = article.find("a", class_="feed-post-link")
                title = title_tag.text.strip() if title_tag else "Sem título"
                link = title_tag["href"] if title_tag else None
                if Database().verify_news("g1", title, link): # Verifica se a notícia já foi coletada
                    continue
                timestamp = article.find("span", class_="feed-post-datetime")
                time_text = timestamp.text.strip() if timestamp else "Horário não encontrado"


                news_list.append({
                    "title": title,
                    "link": link,
                    "time": time_text,
                    "current_page": pagina
                })


        return news_list, last_page

    # Conta o número de páginas com notícias recentes
    def get_pages_news(self, period):
        paginas = 2
        while True:
            res = requests.get(f"https://g1.globo.com/ultimas-noticias/index/feed/pagina-{paginas}.ghtml")
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="feed-post-body")
            time.sleep(random.uniform(0.1, 0.3))
            stop = False
            print(f"Verificando página {paginas - 1}...")
            for article in articles:
                timestamp = article.find("span", class_="feed-post-datetime")
                time_text = timestamp.text.strip() if timestamp else "Horário não encontrado"


                if not any(p in time_text.lower() for p in period):
                    stop = True
                    break
            if stop:
                break    
            paginas += 1
        return paginas
    
    # Retorna o texto completo do artigo. Essa função é usada quando trabalhamos com MySQL
    def get_full_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find("article")
            if full_article is None:
                return None, None # artigo e data não encontrados
            all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
            text = " ".join([p.get_text(separator=" ", strip=True) for p in all_paragraphs])
            timestamp = soup.find("time", itemprop="datePublished")
            time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
            match = re.search(r'\d{2}/\d{2}/\d{4} \d{2}h\d{2}', time_text)
            date_str = match.group().replace("h", ":") 
            date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            return text, date_obj
        except Exception as e:
            return e