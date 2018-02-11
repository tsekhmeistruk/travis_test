import urllib
import json
import shutil
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

repo_base_url = 'https://tsekhmeistruk.github.io/travis_test/'


def run_script():
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(60)
    base_url = "https://moscowshow.com/"
    article_xpath = "//*[@id='main']//article"
    driver.get(base_url)
    articles = driver.find_elements_by_xpath(article_xpath)

    data = []

    for article_number in range(1, len(articles)):
        try:
            driver.get(base_url)
            article = driver.find_element_by_xpath("//*[@id='main']//article[%d]" % article_number)
            event_id = article.get_attribute("id")
            print(event_id)
            img_elements = article.find_elements_by_tag_name("img")
            if len(img_elements) > 0:
                img_link = img_elements[0].get_attribute("src")
                img_link_new = event_id + ".jpg"
                download_img(img_link, img_link_new)
                img_url = repo_base_url + event_id + ".jpg"

            title_elements = article.find_elements_by_xpath(".//h5/a")
            if len(title_elements) > 0:
                title_text = title_elements[0].text
                details_link = title_elements[0].get_attribute("href")

            date_elements = article.find_elements_by_xpath(".//*[contains(@class,'entry-title')][contains(@class,'date')]")
            if len(date_elements) > 0:
                date_text = date_elements[0].text

            details = get_event_details(details_link, driver, date_text, img_url)

            event_object = {"id": event_id, "img": img_url, "title": title_text, "date": date_text, "details": details}
            data.append(event_object)
        except IndexError:
            continue
        except NoSuchElementException:
            continue

    write_json_output(data)
    driver.close()
    driver.quit()


def get_event_details(url, driver, date_text, poster_img_link):
    details_event_title_xpath = "//h1"
    details_event_place_xpath = "//p[contains(@class,'hallAddress')]"
    details_event_price_xpath = "//td[.//p[contains(@class,'hallAddress')]]/following-sibling::td/div[2]"
    details_event_age_constraints_xpath = "//em"
    details_event_main_text_xpath = "//div[contains(@class,'dkpdf')]/following-sibling::p"

    driver.get(url)
    details_event_title = get_text_from_element(driver, details_event_title_xpath)
    details_event_time = date_text
    details_event_place = get_text_from_elements(driver, details_event_place_xpath)
    details_event_price = get_text_from_element(driver, details_event_price_xpath)
    details_event_age_constraints = get_text_from_element(driver, details_event_age_constraints_xpath)
    details_event_main_text = get_text_from_elements(driver, details_event_main_text_xpath)

    event_details = {"details_event_poster_img_link": poster_img_link,
                     "details_event_title": details_event_title,
                     "details_event_time": details_event_time,
                     "details_event_place": details_event_place,
                     "details_event_price": details_event_price,
                     "details_event_age_constraints": details_event_age_constraints,
                     "details_event_main_text": details_event_main_text}

    return event_details


def get_text_from_elements(driver, xpath):
    try:
        elements = driver.find_elements_by_xpath(xpath)

        main_text_paragraphs = []
        for element in elements:
            main_text_paragraphs.append(element.text)

        final_list = []
        for paragraph in main_text_paragraphs:
            list_of_sub_paragraphs = paragraph.split('\n')
            final_list.extend(list_of_sub_paragraphs)

        return final_list

    except Exception:
        return []


def get_text_from_element(driver, xpath):
    try:
        elements = driver.find_elements_by_xpath(xpath)
        return elements[0].text
    except Exception:
        return ""


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
