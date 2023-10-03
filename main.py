import requests
import urllib3
import json

from fake_headers import Headers
from bs4 import BeautifulSoup

urllib3.disable_warnings()



header = Headers(os = "Win",browser="chrome") 
response = requests.get("https://spb.hh.ru/search/vacancy?area=1&area=2&ored_clusters=true&search_period=30&search_field=name&search_field=company_name&search_field=description&currency_code=USD&text=python&enable_snippets=false&only_with_salary=true&L_save_area=true",verify=False,headers=header.generate())

data = response.text

main_soup = BeautifulSoup(data,"lxml")

vac_item = main_soup.find_all("div",class_="vacancy-serp-item__layout")

parsed_data = []

for vac in vac_item:
    zp = vac.find("span",class_="bloko-header-section-2")
    name_company = vac.find("a",class_="bloko-link bloko-link_kind-tertiary").text
    name_city_item = vac.find("div",attrs = {"class":"bloko-text","data-qa":"vacancy-serp__vacancy-address"})
    name_city = name_city_item.text.split("<!-- -->")[0]
    
    if zp is None:
        continue
    zp_vac = zp.text
    zp_absolut = zp_vac.split("<!-- -->")[0]
    print(zp_vac)
    if "$" in zp_vac:
        tag_a = vac.find("a",class_= "serp-item__title")
        absolut_link = tag_a["href"]
        opis_vac = requests.get(absolut_link,verify=False,headers=header.generate())
        opis_vac_html = opis_vac.text
        opis_vac_soup = BeautifulSoup(opis_vac_html,"lxml")
        opis_vac_item = opis_vac_soup.find("div",class_="g-user-content")
        for vac_item in opis_vac_item:
            if "Django" in vac_item.text or "Flask" in vac_item.text:
                parsed_data.append({
                    "link":absolut_link,
                    "salary":zp_absolut,
                    "company":name_company,
                    "city":name_city
                }
                )        
print(parsed_data)

with open ("vacancy.json","w",encoding="utf-8") as f:
    json.dump(parsed_data,f,ensure_ascii=False,indent=2)        