# main.py

##### import #####
# pymysql
import pymysql

# 이력서 추출 파일
import ext_resume as ext1

# 경력기술서 추출 파일
import ext_career as ext2

# 특허 검증 파일
import ver_patent as pat

# contributor 검증 파일
import ver_contributor as con

# 프로젝트 검증 파일
import ver_project_sc as proj

# 수상내역 검증 파일
import ver_project_gpt as gpt

############################# 이 부분은 commit 주의 ###############################
##### selenium/추출 경로/api key #####
# Chrome WebDriver의 경로
webdriver_path = ""

# 이력서 경로, main.py에서 받아올 예정
pdf_path1 = ""

# 경력기술서 경로, main.py에서 받아올 예정
pdf_path2 = ""

# GPT API key
api_key = ""

# mysql connection
conn = pymysql.connect(
    host='', 
    user='', 
    password='', 
    db='',
    charset='utf8'
    )
#################################################################################

# sql 통로
cur = conn.cursor()

# pdf path insert
sql = "INSERT INTO application (application_date, resume_pdf_addr, cv_pdf_addr) VALUES (now(), %s, %s)"
data = (pdf_path1, pdf_path2)
#data = ('a', 'b')
cur.execute(sql, data)
conn.commit()

### main.py에서 리스트 선택한 항목의 pdf path를 SELECT하도록 아래 주석 제거 후 구현

# pdf path select
#sql = "SELECT resume_pdf_addr, cv_pdf_addr FROM application WHERE "
#sql2 = "SELECT * FROM application"
#cur.execute(sql)
#res = cur.fetchall()
# 결과 출력
#for row in res:
#    print(row)
conn.close()

##### 텍스트 추출 #####
'''
# 이력서 추출
ext1.ext_resume(pdf_path1)
print()

# 경력기술서 추출
ext2.ext_career(pdf_path2)
print()


##### 검증 키워드 #####

# 특허 검증_키워드(특허명)
#pat_keyword = ext2.patent_name[0]
pat_keyword = ext2.patent_org[0]

# 특허 검증_키워드(이름, 특허 출원인)
#pat_verification_list = [ext1.names[0], ext2.patent_org[0]]
pat_verification_list = [ext1.names[0]]

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
#pat.patent_ver(webdriver_path, pat_keyword, pat_verification_list)

# contributor 검증
#con.contributor_ver(webdriver_path, github_url, id)

# 프로젝트 및 수상 내역 검증
#proj.proj_ver(proj_keyword, proj_verification_list, gpt_api_key=api_key)
'''