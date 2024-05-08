from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By


def contributor_ver(webdriver_path, github_url, id):

    # Chrome WebDriver 서비스 설정
    service = webdriver.chrome.service.Service(executable_path=webdriver_path)

    # 웹 드라이버 초기화
    driver = webdriver.Chrome(service=service)

    # 웹 페이지 열기
    driver.get(github_url)
    time.sleep(2) # 결과값확인 -> 창이 뜨는지 확인

    # insights 버튼 클릭
    insights_xpath = '//*[@id="insights-tab"]'
    insights_element = driver.find_element("xpath", insights_xpath)
    insights_element.click()
    time.sleep(2) # 결과값 확인 -> 버튼이 클릭되는지 확인

    # Contributors 버튼 클릭
    find = "Contributors"
    category_elements = driver.find_elements(By.CSS_SELECTOR, ".js-selected-navigation-item.menu-item")
    for i in category_elements:
        categories = i.get_attribute("outerHTML")
        if find in categories:
            i.click()
    time.sleep(2) # 결과값 확인 -> 버튼이 클릭되는지 확인


    contributor_names = driver.find_elements(By.CSS_SELECTOR, ".text-normal")

    found = False
    for i in contributor_names:
        names = i.get_attribute("outerHTML") # 해당 클래스의 바깥쪽 HTML을 가져다줌
        if id in names:
            found = True
            break

    if found:
        print("해당 지원자의 정보가 있습니다.")
    else:
        print("해당 지원자의 정보가 없습니다.")

    print(id) # 이름이 정상적으로 담기는지 확인