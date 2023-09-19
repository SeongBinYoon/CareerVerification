from selenium import webdriver #동적페이지(js등)를 처리하기 위한 크롤링 라이브러리
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

#
# 작성자: 컴퓨터학부 윤성빈
#

# Chrome WebDriver의 경로
webdriver_path = ''

# Chrome WebDriver 서비스 설정
service = webdriver.chrome.service.Service(executable_path=webdriver_path)

# 웹 드라이버 초기화
driver = webdriver.Chrome(service=service)

# 가져올 웹 페이지의 URL
url = 'https://news.google.com/home?hl=ko&gl=KR&ceid=KR:ko' # 구글 뉴스

# 웹 페이지 열기
driver.get(url)
#time.sleep(2) # 결과값확인 > 창이 뜨는지 확인하기 위함

# 검색창에 텍스트 입력
input_xpath = '//*[@id="gb"]/div[2]/div[2]/div[2]/form/div[1]/div/div/div/div/div[1]/input[2]'
input_element = driver.find_element("xpath", input_xpath) #셀레니움 함수 변경으로 인해 find_element 사용 -> 이전 버전 find_element_by_xpath
#input_element.send_keys("최정일 AI 코딩")
input_element.send_keys("")
time.sleep(2) # 결과값 확인 > 텍스트가 입력되는지 확인

# 엔터키 입력
input_element.send_keys(Keys.RETURN)
time.sleep(2) # 결과값 확인 > 엔터키가 입력되는지 확인

# 순서대로 기사 확인 (상위 10개 검증 -> 필요 시 조정)
for i in range(1,11):
    article_xpath = f'//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[{i}]/div/article/a'
    article_element = driver.find_element("xpath", article_xpath)
    article_element.click()
    time.sleep(4) # 결과값 확인 > 엔터키가 입력되는지 확인
    
    # 웹 페이지의 HTML 내용 가져오기
    html_content = driver.page_source

    # 웹페이지 html출력확인
    #print(type(html_content))

    # html처리를 위해 beautifulsoup 사용
    soup = BeautifulSoup(html_content, 'html.parser')

    # 지원자 프로젝트 경력 검증
    count = 0
    verification_list = ["",""]
    found = False
    for verification in verification_list:
        if verification in soup.text:
            count += 1
            break
    
    # 탭 전환 및 기사 탭 닫기
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)

# 검증 결과 출력
print(count)
if count > 0:
        print("해당 지원자의 정보가 있습니다.")
else:
        print("해당 지원자의 정보가 없습니다.")

# 웹 드라이버 종료
driver.quit()