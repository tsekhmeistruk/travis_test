import urllib
import json
import shutil
from selenium import webdriver

repo_base_url = 'https://tsekhmeistruk.github.io/travis_test/'


def run_script():
    driver = webdriver.PhantomJS()
    base_url = "https://moscowshow.com/"
    article_xpath = "//*[@id='main']//article"
    driver.get(base_url)
    articles = driver.find_elements_by_xpath(article_xpath)

    data = []

    for article in articles:
        event_id = article.get_attribute("id")
        img_elements = article.find_elements_by_tag_name("img")
        if len(img_elements) > 0:
            img_link = img_elements[0].get_attribute("src")
            img_link_new = event_id + ".jpg"
            download_img(img_link, img_link_new)
            img_url = repo_base_url + event_id + ".jpg"

        title_elements = article.find_elements_by_xpath(".//h5/a")
        if len(title_elements) > 0:
            title_text = title_elements[0].text
            # TODO use this link to fetch the details
            details_link = title_elements[0].get_attribute("href")

        date_elements = article.find_elements_by_xpath(".//*[contains(@class,'entry-title')][contains(@class,'date')]")
        if len(date_elements) > 0:
            date_text = date_elements[0].text

        event_object = {"id": event_id, "img": img_url, "title": title_text, "date": date_text}
        data.append(event_object)
        break
    write_json_output(data)
    driver.close()


def download_img(url, file):
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request) as response, open(file, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def write_json_output(data):
    filename = 'results.json'
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    run_script()
