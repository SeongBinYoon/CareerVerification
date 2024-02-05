# The copyright of this code belongs to Jeong U, Han

from selenium import webdriver #동적페이지(js등)를 처리하기 위한 크롤링 라이브러리
from bs4 import BeautifulSoup
import time
import openai
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

openai.api_key="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"

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

# 가져올 웹 페이지의 URL
url = 'https://www.google.com/' # 카프리스 특허정보검색서비스

# 웹 페이지 열기
driver.get(url)
# time.sleep(2) #결과값확인 > 창이 뜨는지 확인하기 위함

input_xpath = '//*[@id="APjFqb"]'

#검색창에 텍스트 입력
input_element = driver.find_element("xpath", input_xpath)
input_element.send_keys("codegate 2020 본선")
input_element.submit()

verification_list = ["앙진모띠","2등"]

for i in range(1,11):
    button_xpath = f'//*[@id="rso"]/div[{i}]/div/div/div[1]/div/div/span/a'
    button_element = driver.find_element("xpath", button_xpath)
    button_link = button_element.get_attribute('href')
    driver.get(button_link)

    # 웹 페이지의 HTML 내용 가져오기
    html_content = driver.page_source

    #html처리를 위해 beautifulsoup 사용
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    text_without_extra_spaces = ' '.join(str(text).split())


    found = False
    if verification_list[0] in soup.text:
        found = True
        break
    
    # 이전 탭 전환 및 닫기
    if found:
        break
    else:
        driver.back()

# 웹 드라이버 종료
driver.quit()

if found:
    # 모델 - GPT 3.5 Turbo 선택
    model = "gpt-3.5-turbo"
    name = verification_list[0]
    score = verification_list[1]

    # 질문 작성하기
    query = "아래의 웹에서 크롤링한 내용을 토대로 " + name + "이(가) " + "어떤 수상 성적을 거뒀는지 알려줘.\n" + str(text_without_extra_spaces)
    print(query)

    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    print('-'*50)
    print(answer)
else:
    print("해당 지원자의 정보가 없습니다.")