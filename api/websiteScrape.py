import os

from api.Request import Request
from utils.TableManager import TableManger
from utils.const import __CUR_DIR__
import time
import re

from selenium.webdriver import Chrome, ChromeOptions




class WebsiteScrape(object):

    requests_made = 0

    web_scrape_log = TableManger(os.path.join(__CUR_DIR__, "logs\webscrape_log.json"))
    web_scrape_log.load_df(".json")

    opts = ChromeOptions()
    opts.add_argument('--disable-extensions')
    browser = Chrome("webdriver/chromedriver.exe", chrome_options=opts)

    @staticmethod
    def request(url: str):

        r = WebsiteScrape.browser.get(url)

        WebsiteScrape.requests_made = WebsiteScrape.requests_made + 1

        if WebsiteScrape.requests_made % 20:
            print("Requests Made: " + str(WebsiteScrape.requests_made))
        return r

    @staticmethod
    def scrape(domain: str):
        try:
            base_domain = re.findall(r"^.+?[^\/:](?=[?\/]|$)", domain)[0]
        except:
            base_domain = domain

        keywords = {
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

        def get_page(domain):
            WebsiteScrape.request(domain)
            g_elems = WebsiteScrape.browser.find_elements_by_xpath("//a[@href]")
            g_doc = WebsiteScrape.browser.page_source

            return g_elems, g_doc

        elems,doc = get_page(base_domain)
        crawl_links = WebsiteScrape.scrape_domain_links(elems, base_domain)

        emails = WebsiteScrape.scrape_emails(doc)
        facebook = WebsiteScrape.scrape_social_links(elems, "facebook")
        instagram = WebsiteScrape.scrape_social_links(elems, "instagram")
        keywords = WebsiteScrape.scrape_keywords(doc, keywords, base_domain)
        pages = len(crawl_links)

        for link in crawl_links:
            elems, doc = get_page(link)

            if len(emails) == 0:
                emails = WebsiteScrape.scrape_emails(doc)
            if len(facebook) == 0:
                facebook = WebsiteScrape.scrape_social_links(elems, "facebook")
            if len(instagram) == 0:
                instagram = WebsiteScrape.scrape_social_links(elems, "instagram")

            keywords = WebsiteScrape.scrape_keywords(doc, keywords, base_domain)

        return {
            "emails": emails,
            "facebook": facebook,
            "instagram": instagram,
            "keywords": keywords,
            "pages": pages
        }

    @staticmethod
    def scrape_emails(doc):

        emails = re.findall(r'[\w\.-]+@[\w\.-]+', doc)

        return list(set(emails))

    @staticmethod
    def scrape_social_links(elems, social_str: str):
        social_links = []

        for elem in elems:
            link = elem.get_attribute("href")
            if social_str in link.lower():
                social_links.append(link)

        return social_links

    @staticmethod
    def scrape_domain_links(elems, base_domain: str):
        domain_links = []


        for elem in elems:
            link = elem.get_attribute("href")
            if base_domain in link:
                domain_links.append(link)

        return list(set(domain_links))

    @staticmethod
    def scrape_keywords(doc, keywords, cur_link):
        for key in keywords:
            inst = doc.count(key)

            keywords[key].append({"count": inst, "link": cur_link})

        return keywords












