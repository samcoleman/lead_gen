import os

from api.Request import Request
from utils.TableManager import TableManger
from utils.const import __CUR_DIR__


import pandas as pd
import re
from bs4 import BeautifulSoup




class WebsiteScrape(object):

    web_scrape_log = TableManger(os.path.join(__CUR_DIR__, "logs\webscrape_log.json"))
    web_scrape_log.load_df(".json")

    @staticmethod
    def scrape(domain: str):
        try:
            base_domain = re.findall(r"^.+?[^\/:](?=[?\/]|$)", domain)[0]
        except:
            base_domain = domain

        if WebsiteScrape.web_scrape_log.check_duplicate('base_domain', base_domain):
            print("Scrape: " + base_domain + " already complete")
            return

        def get_page(domain):
            print("Visiting: "+domain)
            r = Request.get(domain)
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup

        soup = get_page(base_domain)
        crawl_links = WebsiteScrape.scrape_domain_links(soup, base_domain)


        emails = WebsiteScrape.scrape_emails(soup)
        facebook = WebsiteScrape.scrape_social_links(soup, "facebook")
        instagram = WebsiteScrape.scrape_social_links(soup, "instagram")
        twitter = WebsiteScrape.scrape_social_links(soup, "twitter")
        linkedin = WebsiteScrape.scrape_social_links(soup, "linkedin")

        linked_keywords = {}
        linked_keywords[base_domain] = WebsiteScrape.scrape_keywords(soup)

        linked_price = {}
        linked_price[base_domain] = WebsiteScrape.scrape_price(soup)

        crawl_links = [x for x in crawl_links if base_domain + "/" != x]
        crawl_links = [x for x in crawl_links if base_domain != x]
        pages = len(crawl_links)

        for link in crawl_links:
            soup = get_page(link)

            if len(emails) == 0:
                emails = WebsiteScrape.scrape_emails(soup)
            if len(facebook) == 0:
                facebook = WebsiteScrape.scrape_social_links(soup, "facebook")
            if len(instagram) == 0:
                instagram = WebsiteScrape.scrape_social_links(soup, "instagram")
            linked_keywords[link] = WebsiteScrape.scrape_keywords(soup)
            linked_price[link] = WebsiteScrape.scrape_price(soup)

        result = {
            "emails": emails,
            "facebook": facebook,
            "instagram": instagram,
            "twitter": twitter,
            "linkedin": linkedin,
            "keywords": linked_keywords,
            "prices": linked_price,
            "pages": pages
        }

        d = {'base_domain': base_domain, 'result': [result]}
        df = pd.DataFrame(d)
        WebsiteScrape.web_scrape_log.save_df_append(df, ".json")

        return result

    @staticmethod
    def scrape_emails(soup):
        emails = soup.find_all(text=re.compile("[\w\.-]+@[\w\.-]+"))

        return list(set(emails))

    @staticmethod
    def scrape_social_links(soup, social_str: str):
        social_links = []

        links = soup.find_all('a', href=True)
        for a_link in soup.find_all(attrs={'href': re.compile("http")}):
            if social_str in a_link.get('href'):
                social_links.append(a_link.get('href'))

        return list(set(social_links))

    @staticmethod
    def scrape_domain_links(soup, base_domain: str):
        domain_links = []

        for a_link in soup.find_all('a', href=True):
            if base_domain in a_link['href']:
                domain_links.append(a_link['href'])
            elif a_link['href'][0] == "/":
                domain_links.append(base_domain + a_link['href'])

        return list(set(domain_links))

    @staticmethod
    def scrape_keywords(soup):
        empty_keywords = {
            "eyelash": [],
            "lash": [],
            "classic": [],
            "classic lash": [],
            "classic eyelash": [],
            "volume": [],
            "volume lash": [],
            "volume eyelash": [],
            "russian": [],
            "russian lash": [],
            "russian eyelash": [],
        }

        for key in empty_keywords:
            nodes = soup.find_all(text=lambda x: x and key in x)
            empty_keywords[key].append({"count": len(nodes), "nodes": nodes})

        return empty_keywords

    @staticmethod
    def scrape_price(soup):
        nodes = soup.find_all(text=lambda x: x and "£" in x)
        return {"count": len(nodes), "nodes": nodes}












