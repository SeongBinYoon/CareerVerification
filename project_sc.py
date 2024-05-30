import requests
import extract2 as ext2

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from gpt_verification import verify_html_usingGPT


# google 뉴스로부터 html 가져오는 함수
def get_google_results(base_url, search_query):
        # 검색어에 대한 URL 인코딩
        url = f"{base_url}/search?q={search_query}&hl=ko&gl=KR&ceid=KR%3Ako"

        # 해당 URL에 요청 보내기
        response = requests.get(url)
        hrefs = []

        # 응답 확인
        if response.status_code == 200:
            # BeautifulSoup를 사용하여 HTML 파싱
            soup = BeautifulSoup(response.content, 'html.parser')
            article = soup.find('div', class_='T4LgNb')
            a_tags = article.find_all('a')
    
            # 상위 10개의 "a" 태그의 href 속성 값 출력 - 상위 10개의 기사 링크 추출 후 hrefs 리스트에 append 
            for index, a_tag in enumerate(a_tags):
                if index < 10:
                    href = a_tag.get('href')
                    hrefs.append(href)
                    print(href)
                else:
                    break
        
            return hrefs
        else:
            # 요청이 실패한 경우 None 반환
            return None


# 가져온 html로부터 정적 1차 검증 함수
def proj_ver(search_query, verification_list, mode="award", base_url= "https://news.google.com", gpt_api_key=None):
        
    # Google 뉴스 결과 가져오기
    results = get_google_results(base_url,search_query)

    # 결과 출력
    if results:
        print("검색어를 성공적으로 검색하였습니다.\n")
    else:
        print("검색어 입력 과정에서 오류가 발생했습니다.\n")

    for i in range(10):
        # full_url 생성
        relative_url = results[i]
        full_url = base_url + relative_url
        response = requests.get(full_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.text
        text = ' '.join(str(text).split())

        # 지원자 프로젝트 경력 검증
        verification_count_list = [0] * len(verification_list)
    
        # verification_list의 각 단어에 대해 count를 하여 중복을 피함
        for word in verification_list:
            if word in text:
                word_index = verification_list.index(word)
                verification_count_list[word_index] += 1

        count = sum(1 for count in verification_count_list if count > 0)

        print(full_url)
        print(verification_count_list)
        print(f"해당 지원자의 정보가 {count}/{len(verification_list)} 개 있습니다.")

        if all(count > 0 for count in verification_count_list):
            if gpt_api_key != "":
                keyword = search_query

                if mode == 'award':
                    query = ('아래의 웹에서 크롤링한 내용을 토대로' + verification_list[0] + '이(가)' + keyword + '에서' + 
                            verification_list[1] + '수상성적을 거뒀는지 알려줘.' + text)
                if mode == 'project':
                    query = ('아래의 웹에서 크롤링한 내용을 토대로' + verification_list[0] + verification_list[1] + 
                             '이(가)' + keyword + '에서' + '프로젝트 경험이 있는지 알려줘.' + text)
                    
                answer = verify_html_usingGPT(query, gpt_api_key)
            if mode == 'project':
                # 검증 결과 딕셔너리에 추가
                ext2.vres['project'].append("프로젝트 내역이 있습니다.")
                ext2.gpt_res['proj'].append(answer)
            else:
                # 검증 결과 딕셔너리에 추가
                ext2.vres['award'].append("수상 내역이 있습니다.")
                ext2.gpt_res['award'].append(answer)
            
            print("검증에 성공하였습니다. 검증을 종료합니다.")
            break
    if mode == 'project':
        # 검증 결과 딕셔너리에 추가
        ext2.vres['project'].append("프로젝트 내역이 없습니다.")
    else:
        # 검증 결과 딕셔너리에 추가
        ext2.vres['award'].append("수상 내역이 없습니다.")