__author__ = 'Rom54'

import bleach
from bs4 import BeautifulSoup
from pprint import pprint
from string import whitespace


class ParserTable:

    def __init__(self, page: str):
        self.page = bleach.clean(
            page,
            tags=['head','meta','td','font','b','i','p','title','table','body','html','tr','br'],
            attributes=('color', )
        )
        self.soup = BeautifulSoup(self.page, "html.parser")

    def data_tr(self):
        tr_mas = []
        td_mas = []
        for tr in self.soup('tr'):
            for td in tr('td'):
                td_text = td.text.strip(whitespace)
                td_mas.append(td_text if td_text else "_")
            tr_mas.append(td_mas)
            td_mas = []
        return tr_mas

    def name_group(self):
        group = str(self.soup.find_all('font', color='#ff00ff')[0].text).strip(whitespace)  # если не находит имя - исключение
        return group

# table = ParserTable.name_group('7.html')
# pprint(table)
# assert len(table) == 9, "Слишком мало строк"
# assert all(len(r) == 10 for r in table), "Слишком мало столбцов"

# with open('tables/wada.htm') as f:
#     s = f.read()
#     p = ParserTable(s)
#     print(p.data_tr())
#     # assert p.name_group() == 'ИВТ-15'
