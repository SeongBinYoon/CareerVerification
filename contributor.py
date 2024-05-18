from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

def contributor_ver(webdriver_path, github_url, id):

    # Chrome WebDriver 서비스 설정
    service = webdriver.chrome.service.Service(executable_path=webdriver_path)

    # # 웹 드라이버 초기화
    driver = webdriver.Chrome(service=service)

    # 해당 URL에 요청 보내기
    driver.get(github_url + "/graphs/contributors")
    time.sleep(5)  # 페이지가 로드될 때까지 대기

    contributor_names = driver.find_elements(By.CSS_SELECTOR, ".text-normal")
    for i in contributor_names:
        ids = i.get_attribute("outerHTML") # 해당 클래스의 바깥쪽 HTML을 가져다줌
        if id in ids:
            found = True
            break
    else:
        # 요청이 실패한 경우 None 반환
        found = False
    if found:
        print("해당 지원자의 정보가 있습니다.")
    else:
        print("해당 지원자의 정보가 없습니다.")

    print(id) # 이름이 정상적으로 담기는지 확인

contributor_ver(r"C:\Users\minji\Downloads\chromedriver_win32 (1)\chromedriver.exe","https://github.com/midday2612/aix-deep-learning", "midday2612")