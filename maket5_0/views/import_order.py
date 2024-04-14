from bs4 import BeautifulSoup


def parse_order_html():
    with open('maket5_0/files/tmp_file', 'r', encoding="utf-8") as tmp:
        # demo = tmp.read()
        soup_html = BeautifulSoup(tmp, "html.parser")
        soup_tr = soup_html.find_all("tr")
        tr_strings = []
        for tr in soup_tr:
            tmp_tr = tr.contents
            tmp_strings = []
            for td in tmp_tr:
                try:
                    tmp_td = td.contents[0]
                    if tmp_td != '':
                        tmp_strings.append(tmp_td)
                except:
                    pass
            if tmp_strings:
                tr_strings.append(tmp_strings)
    return tr_strings
