from pandas._config.config import options
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas 

driver_path = ChromeDriverManager().install()
options = ChromeOptions()
options.add_argument("--headless")
driver = Chrome(driver_path, options=options)
#driver = Chrome(ChromeDriverManager().install()) # これでもOK

driver.get("https://gyoumu-kouritsuka-pro.site/")

df = pandas.DataFrame()
while True:
    article_elms = driver.find_elements_by_css_selector(".entry-card-wrap.a-wrap.border-element.cf")
    for article_elm in article_elms:
        article_link = article_elm.get_attribute("href")
        title = article_elm.find_element_by_css_selector("h2").text
        post_date = article_elm.find_element_by_css_selector(".post-date").text
        print(article_link, title, post_date)
        df = df.append({
            "リンク": article_link,
            "タイトル": title,
            "投稿日": post_date
        }, ignore_index=True)
    
    try:
        driver.find_element_by_css_selector(".pagination-next-link.key-btn").click()
    except:
        print("次のページなし")
        break
    

df.to_csv("記事の一覧.csv", encoding="utf-8_sig")



