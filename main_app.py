from selenium import webdriver


def run_script():
    driver = webdriver.PhantomJS()
    base_url = "https://moscowshow.com/"
    article_xpath = "//*[@id='main']//article"
    driver.get(base_url)
    articles = driver.find_elements_by_xpath(article_xpath)
    number_of_articles = str(len(articles))

    with open('num.json', 'w') as file:
            file.write(number_of_articles)

    driver.close()


if __name__ == "__main__":
    run_script()
