# main.py
# 작성자: 윤성빈

##### import #####
# 이력서 추출 파일
import extract as ext1

# 경력기술서 추출 파일
import extract2 as ext2

# 특허 검증 파일
import patent as pat

# contributor 검증 파일
import contributor as con

# 프로젝트 검증 파일
import project_sc as proj

# 수상내역 검증 파일
import gpt_verification as gpt

############################# 이 부분은 commit 주의 ###############################
##### selenium/추출 경로 #####
# Chrome WebDriver의 경로
webdriver_path = ""

# 이력서 경로
pdf_path1 = ""

# 경력기술서 경로
pdf_path2 = ""

##### patent 검증 #####
#입사자 개인정보리스트
pat_keyword = ""
pat_verification_list = [""]

##### contributor 검증 #####
# github url
github_url = '' # github 프로젝트 메인 화면

# 지원자의 github 아이디
id = ""

##### award 검증 #####
# gpt api key
api_key=""
award_keyword = ""
award_verification_list = ["",""]

##### project 검증 #####
news_url = '' # 구글 뉴스
proj_keyword = ""
proj_verification_list = ["", ""]

#################################################################################


##### 함수 호출 #####

# 이력서 추출
ext1.ext_resume(pdf_path1)
print()

# 경력기술서 추출
ext2.ext_career(pdf_path2)
print()

# 특허 검증 (path, keyword, pinfo_list)
pat.patent_ver(webdriver_path, pat_keyword, pat_verification_list)

# contributor 검증
con.contributor_ver(webdriver_path, github_url)

# 수상내역 검증
gpt.award_ver(api_key, award_keyword, award_verification_list)

# 프로젝트 검증
proj.proj_ver(news_url, proj_keyword, proj_verification_list)