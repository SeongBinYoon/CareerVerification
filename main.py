# main.py

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
##### selenium/추출 경로/api key #####
# Chrome WebDriver의 경로
webdriver_path = ""

# 이력서 경로
pdf_path1 = ""

# 경력기술서 경로
pdf_path2 = ""

# GPT API key
api_key = ""
#################################################################################


##### 텍스트 추출 #####

# 이력서 추출
ext1.ext_resume(pdf_path1)
print()

# 경력기술서 추출
ext2.ext_career(pdf_path2)
print()


##### 검증 키워드 #####

# 특허 검증_키워드(특허명)
pat_keyword = ext2.patent_name[0]
#pat_keyword = ext2.patent_org[0]

# 특허 검증_키워드(이름, 특허 출원인)
pat_verification_list = [ext1.names[0], ext2.patent_org[0]]

# contributor 검증_키워드(github url)
print(ext2.github_id[0], ext2.github_repo[0])
github_url = ext2.github_repo[0]

# contributor 검증_키워드(github id)
id = ext2.github_id[0]

# award 및 project 검증_키워드(프로젝트명)
proj_keyword = ext1.names[0]

# award 및 project 검증_키워드(이름, 기관명)
proj_verification_list = [ext2.proj_name[0], ext2.proj_org[0]]


##### 검증 함수 호출 #####

# 특허 검증 (path, keyword, pinfo_list)
pat.patent_ver(webdriver_path, pat_keyword, pat_verification_list)

# contributor 검증
con.contributor_ver(webdriver_path, github_url, id)

# 프로젝트 및 수상 내역 검증
proj.proj_ver(proj_keyword, proj_verification_list, gpt_api_key=api_key)
