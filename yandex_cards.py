import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
binary_yandex_driver_file = 'yandexdriver.exe'
driver = webdriver.Chrome(f"C:/users/lolpo/Downloads/{binary_yandex_driver_file}", options=options)
driver.get("https://yandex.ru/")

driver.add_cookie({'name': '_mygtm_utm_yclid', 'value': 'undefined'})
driver.add_cookie({'name': '_mygtm_utm_fbclid', 'value': 'undefined'})
driver.add_cookie({'name': 'BITRIX_SM_COOKIE_ACCEPTION', 'value': 'true'})
driver.add_cookie({'name': 'clientid', 'value': '1657034149548.6593574739'})
driver.add_cookie({'name': '_mygtm_utm_wbraid', 'value': 'undefined'})
driver.add_cookie({'name': 'tmr_reqNum', 'value': '82'})
driver.add_cookie({'name': '_ym_isad', 'value': '2'})
driver.add_cookie({'name': '_ym_uid', 'value': '1657034150783971670'})
driver.add_cookie({'name': '_ym_d', 'value': '1657034150'})
driver.add_cookie({'name': '_gcl_au', 'value': '1.1.419134432.1657034150'})
driver.add_cookie({'name': '_mygtm_gpb_own_cookie', 'value': '1657034149548.6593574739'})
driver.add_cookie({'name': '_mygtm_utm_pb_clickid', 'value': 'undefined'})
driver.add_cookie({'name': '_mygtm_utm_gbraid', 'value': 'undefined'})
driver.add_cookie({'name': 'tmr_lvidTS', 'value': '1657034149875'})
driver.add_cookie({'name': 'tmr_lvid', 'value': '5a784389a8b58039ed7d55452f9b871d'})
driver.add_cookie({'name': '_mygtm_utm_gclid', 'value': 'undefined'})
driver.add_cookie({'name': '_mygtm_utm_ymclid', 'value': 'undefined'})
driver.add_cookie({'name': '_ym_visorc', 'value': 'b'})
driver.add_cookie({'name': 'ab_version', 'value': 'original'})
driver.add_cookie({'name': 'BITRIX_SM_CITY_REAL_ID', 'value': '693'})
driver.add_cookie({'name': 'BITRIX_SM_USER_CITY', 'value': '%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80'})
driver.add_cookie({'name': 'consumer_credit_calculator', 'value': '{%22sumIn%22:5000000%2C%22term%22:84}'})
driver.add_cookie({'name': 'flocktory-uuid', 'value': '9b520c78-de3b-41db-901e-2b13f7540947-2'})
driver.add_cookie({'name': 'ga_all_param', 'value': ''})
driver.add_cookie({'name': 'PHPSESSID', 'value': 'fnyDoAORp2R1YX1QdlALNFccPJD2rnQd'})
driver.add_cookie({'name': 'st_uid', 'value': '24a2781933998c5c916e6f06c5b03e77'})
driver.add_cookie({'name': 'tmr_detect', 'value': '0%7C1657093858364'})

driver.get(
    "https://yandex.ru/maps/?display-text=Сбербанк%20России%2C%20отделения&ll=144.462854%2C40.904234&mode=search&sctx=ZAAAAAgBEAAaKAoSCYnQCDauz0JAEabtX1lp4EtAEhIJA137Anqh8j8RmPxP%2Fu4d7D8iBgABAgMEBSgAOABAkE5IAWIXc291cmNlPWJ1c2luZXNzOmV4cF9yZWZqAnJ1nQHNzEw9oAEAqAEAvQHLe6nKwgF957enhAT7kbilBsSImpwE4fqP8AOgseyMBP6c2q8EjIz1mwSNiqeQBLXOjocE7JOL4gOcuI3nBI7fgIcE3rLc5APxufjcA6btn%2B4D8fajnQXbqZOcBMOPx%2FIDx%2BOBnATkvZGaBJ3v7e0DvJyjogThxciNBPry%2FowExPvN3wPqAQDyAQD4AQCCAhJjaGFpbl9pZDooNjAwMzYxMimKAgCSAgCaAgxkZXNrdG9wLW1hcHM%3D&sll=144.462854%2C40.904234&sspn=369.843750%2C137.610782&text=chain_id%3A%286003612%29&z=2")
def get_main_page():
    for i in range(500):
        element = driver.find_elements(By.CLASS_NAME, "search-snippet-view__placeholder")
        if not element:
            break

        ActionChains(driver).scroll_to_element(element[-1]).perform()
        time.sleep(2)

    html = driver.execute_script("return document.body.outerHTML;")
    with open("sber.html", "w", encoding="UTF-8") as file:
        file.write(html)
    return html


def generate_cookie():
    with open("../cookie.json", "r") as f:
        fd = json.load(f)
    for i in fd:
        print("driver.add_cookie({" + f"'name': '{i['name']}', 'value': '{i['value']}'" + "})")


# generate_cookie()

org_ids = []
list_new = {}


def get_file_page():
    with open("sber.html", encoding='utf-8') as f:
        html = f.read()
    return html


html = get_file_page()

count = 0
for i in BeautifulSoup(html, "lxml").find_all("a", {"class": "search-snippet-view__link-overlay"}):
    org_id = i["href"].split("/")[-2]
    driver.get(f"https://yandex.ru/maps/org/gazprombank/{org_id}/reviews/")
    for _ in range(15):
        time.sleep(2)
        element = driver.find_elements(By.CLASS_NAME, "business-tab-wrapper")
        if not element:
            break

        ActionChains(driver).scroll_to_element(element[-1]).perform()
    soup = BeautifulSoup(driver.execute_script("return document.body.outerHTML;"), "lxml")
    reviews = soup.find_all("div", {"class": "business-reviews-card-view__review"})
    driver.get(f"https://yandex.ru/maps/org/gazprombank/{org_id}/")
    soup = BeautifulSoup(driver.execute_script("return document.body.outerHTML;"), "lxml")

    for review in reviews:
        try:
            json_data = {"name": review.find("span", {"itemprop": "name"}).text,
                         "date": review.find("span", {"class": "business-review-view__date"}).text,
                         "text": review.find("span", {"class": "business-review-view__body-text"}).text,
                         "address": soup.find("div", {"class": "business-contacts-view__address"}).text,
                         "rating": len(review.find_all("span", {"class": "_full"})),
                         }
        except Exception:
            print("DROPPED")
            time.sleep(100)
            continue
        if review.find("div", {"class": "cmnt-item-header__officiality-text"}):
            json_data.update(reply_date=review.find("span", {"class": "cmnt-item-header__date"}),
                             reply_text=review.find("span", {"class": "cmnt-item__message"}))
        count += 1
        if count % 50 == 0:
            with open("yandex.json", "w") as file:
                json.dump(org_ids, file)
        org_ids.append(json_data)

with open("yandex.json", "w") as file:
    json.dump(org_ids, file)
