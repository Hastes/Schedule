__author__ = 'Rom54'

import bleach
from bs4 import BeautifulSoup
from string import whitespace

class ParserTable:
    def data_tr(file):
        page = open(file)
        page_parse = bleach.clean(page.read(),tags=['head','meta','td','font','b','i','p','title','table','body','html','tr','br'])
        soup = BeautifulSoup(page_parse, "html.parser")
        tr_mas = []
        td_mas = []
        for tr in soup('tr'):
            for td in tr('td'):
                td_text = td.text.strip(whitespace)
                td_mas.append(td_text if td_text else "_")
            tr_mas.append(td_mas)
            td_mas=[]
        return tr_mas

    def name_group(file):
        soup = BeautifulSoup(file, "html.parser")
        try:
            group = str(soup.find_all('font',color='#ff00ff')[0].text).strip(whitespace)
        except IndexError:
            return "unknown"
        return group
