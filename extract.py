import re
from tika import parser

#
# 작성자: 컴퓨터학부 윤성빈
#

# pdf 파일 경로 및 텍스트 추출
path = ""
text_all = parser.from_file(path)['content']

# 줄바꿈, 괄호, 콤마 문자를 대체
text = re.sub(r'[\n(),]', '', text_all)
#print(text)    # 추출한 pdf 내용 확인

# 이력서 양식에 따라 유연한 수정 예정
# '이름' 다음에 오는 한글 이름 패턴 2~4글자 찾기
name_pat = r'이름\s*([가-힣]{2,4})'

# 이름 추출
names = re.findall(name_pat, text)

# '생년월일' 다음에 오는 주민등록번호 13자리 찾기
regnum_pat = r'생년월일\s*((?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-?\s?[1-4][0-9]{6})'

# 주민등록번호 추출
regnum = re.findall(regnum_pat, text)

# '주소' 다음에 오는 주소 찾기
# ㅇㅇ도/시/군/구/면/읍/리/로
# 11(-11)
# 1(번)길 11-11
# ㅇㅇ2길 11
# 도로명 주소 = 주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*) -> 수정 완료
# +상세 주소 = r'주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*\s?[가-힣]*\s?[가-힣]*\s?[0-9]*동?\s?[0-9]*호?)'
#addr_pat = r'주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*\s?[가-힣]*\s?[0-9]*동?\s?[0-9]*호?)'
addr_pat = r'주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*\s?[가-힣]*\s?[가-힣]*\s?[0-9]*동?\s?[0-9]*호?)'

# 주소 추출
addr = re.findall(addr_pat, text)

# '연락처' 다음에 오는 전화번호 11자리 찾기
phone_pat = r'연락처\s*(^02.{0}|^01.{1}|[0-9]{3}-?\s?[0-9]+-?\s?[0-9]{4})'

# 전화번호 추출
phone = re.findall(phone_pat, text)

# github 프로젝트 도메인 찾기
domain_pat = r'(((http(s?))\:\/\/)?)([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?'

# github 프로젝트 도메인 추출
domain = re.search(domain_pat, text)


# 결과 출력_이름
if names:
    print(names[0])  # 첫 번째 일치 항목 (보통 맨 처음 등장하는 이름이 지원자 이름이므로 -> 필요할 경우 수정)
else:
    print("이름을 찾을 수 없습니다.")

# 결과 출력_주민등록번호
if regnum:
    print(regnum[0])
else:
    print("주민등록번호를 찾을 수 없습니다.")

# 결과 출력_주소
if addr:
    print(addr[0])
else:
    print("주소를 찾을 수 없습니다.")

# 결과 출력_전화번호
if phone:
    print(phone[0])
else:
    print("연락처를 찾을 수 없습니다.")

# 결과 출력_github 도메인
if domain:
    print(domain[0])
else:
    print("도메인을 찾을 수 없습니다.")