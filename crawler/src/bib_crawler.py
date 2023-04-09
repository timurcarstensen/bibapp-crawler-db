# standard library imports
import os

# third party imports
from datetime import datetime
import mysql.connector
from bs4 import BeautifulSoup as soup

cnx = mysql.connector.connect(
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_ROOT_PASSWORD"),
    host="dm-1-db",
    port=os.getenv("MYSQL_PORT"),
    database=os.getenv("MYSQL_DATABASE"),
)

cursor = cnx.cursor()

user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
headers = {"User-Agent": user_agent}


def downloadWebsite(link: str, hdr: dict) -> str:
    import urllib.request as uReq

    website = uReq.Request(link, headers=hdr)
    uClient = uReq.urlopen(website)  # downloading the website
    page_html = uClient.read()
    uClient.close()
    return page_html


p = soup(
    downloadWebsite(
        "https://www.bib.uni-mannheim.de/standorte/freie-sitzplaetze", headers
    ),
    "lxml",
)

p_tag = p.body.div.table.tbody

x = p_tag.find_all("tr")

output_dict = {}


for i in x[1:]:
    bib = str(i.a.contents[0]).split()[-1]
    if i.span is not None and i.span.contents[0] is not None:
        belegung = i.span.contents[0]
    else:
        belegung = 0
    output_dict[bib] = int(str(belegung).split()[0])

date = datetime.now().replace(second=0, microsecond=0)
string_date = str(date).replace(":", "-")

query = (
    "INSERT INTO bib_data " "(timestamp, area, free_seats_int) " "VALUES (%s, %s, %s)"
)

for x, y in output_dict.items():
    data = (string_date, x, int(y))
    cursor.execute(query, data)
    cnx.commit()


cursor.close()
cnx.close()
