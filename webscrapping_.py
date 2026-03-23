import requests
from bs4 import BeautifulSoup as soup # parsing library to help navgiate html


class WebScraper:
    def __init__(self, website_url, page_url):
        self.website_url = website_url
        self.page_url = page_url
        self.all_info_dict_ = []
        self.html_content = ""
        self.the_soup_ = None
        self.scrape()

    def extract_html_data_to_dict_(self):
        print(self.the_soup_.title)
        page_title = self.the_soup_.title.text.strip() if self.the_soup_.title else "No title found"
        print(f"Page Title: {page_title}")
        headings = self.the_soup_.find_all('h3')
        for h3_tag in headings:
            info_dict_ = {
            "page_title": page_title,
            "heading": [],
            "paragraph": [],
            "paragraph_article_": [],
            "link": []
            }
            info_dict_["heading"].append(h3_tag.text.strip())
            the_para_in_h3_ = h3_tag.find_next('p')
            the_link_in_h3_ = h3_tag.find_next('a', href=True)
            info_dict_["paragraph"].append(the_para_in_h3_.text.strip() if the_para_in_h3_ else "No paragraph found")
            info_dict_["link"].append(the_website_url+the_link_in_h3_['href'] if the_link_in_h3_ else "No link found")
            self.all_info_dict_.append(info_dict_)

    def requests_get_page_content_(self):
        try:
            response = requests.get(self.website_url + self.page_url)
            response.raise_for_status()  # Check if the request was successful
            if response.status_code == 200:
                self.html_content = response.text
                print(f"Successfully fetched the page: {self.website_url + self.page_url}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            
    def get_articles_info(self):
            # an_element_ = self.all_info_dict_[2]
        for an_element_ in self.all_info_dict_:
            this_link_ =  an_element_['link'][0]
            print(f"Fetching article from link: {this_link_}")
            response = requests.get(this_link_)
            if response.status_code == 200: 
                article_soup = soup(response.text, 'html.parser')
                article_title = article_soup.title.text.strip() if article_soup.title else "No title found"
                print(f"Article Title: {article_title}")
                article_paragraphs = article_soup.find_all('p')
                for para in article_paragraphs:
                    print(f"Paragraph: {para.text.strip()}")
                    an_element_["paragraph_article_"].append(para.text.strip())

    def scrape(self):
        self.requests_get_page_content_()
        soup_page = soup(self.html_content, 'html.parser')
        self.the_soup_ = soup_page
        self.extract_html_data_to_dict_()    
        self.get_articles_info()
        print(f"All extracted information: {self.all_info_dict_[3].keys()}")       

# _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-.   
the_website_url = "https://www.nationalww2museum.org"
the_page_url = "/war/articles"
wbscrpr_ = WebScraper(the_website_url, the_page_url)
print(f"Extracted information from the webpage: {wbscrpr_.all_info_dict_[0]['paragraph_article_']}")
from db_operations_postgre_ import insert_data_into_postgre_, create_table_in_postgre_, fetch_data_from_postgre_
create_table_in_postgre_()
insert_data_into_postgre_(wbscrpr_.all_info_dict_)
fetch_data_from_postgre_()
