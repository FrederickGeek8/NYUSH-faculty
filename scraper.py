import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = "https://shanghai.nyu.edu/academics/faculty-directory"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
a = soup.findAll("a", {"class": "exposed-filter-button",
                       "data-referenceid": "edit-discipline-wrapper"})
for _class in a:
    discipline = _class.text
    discipline_code = _class["data-filterid"]
    f = open(discipline, "w")

    ctr = 0
    while True:
        url = "https://shanghai.nyu.edu/academics/faculty-directory?discipline=" + discipline_code + \
            "&preferred_name=&rank=All&flagged=0&sort_by=field_last_name_value_1&sort_order=ASC&last=dis&page=" + \
            str(ctr)
        response = requests.get(url)
        d_soup = BeautifulSoup(response.text, "html.parser")
        if d_soup.find("div", {"class": "view-empty"}) is None:
            raw_titles = d_soup.findAll("div", {"class": "views-field-title"})
            for title in raw_titles:
                info = title.find("a")
                name = " ".join(info.text.strip().split())
                prof_url = info.get("href")
                prof_resp = requests.get("https://shanghai.nyu.edu" + prof_url)
                prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
                raw_email = prof_soup.find(
                    "div", {"class": "field-name-field-email-address"})
                if raw_email is not None:
                    email_field = raw_email.find(
                        "div", {"class": "field-items"}, recursive=False)
                    email = email_field.find(
                        "div", {"class": "field-item"}).text
                    print(name, email)
                    f.write(name + "\t" + email + "\n")
            ctr += 1
        else:
            break
    print("Finished", discipline)
    f.close()
