import re
from tika import parser


def ext_resume(pdf_path1):
    # pdf 파일 경로 및 텍스트 추출
    text_all = parser.from_file(pdf_path1)['content']

    # 줄바꿈, 괄호, 콤마 문자를 대체
    text = re.sub(r'[\n(),]', '', text_all)
    #print(text)    # 추출한 pdf 내용 확인

    ##### 인적 사항 #####
    # '이름' 다음에 오는 한글 이름 패턴 2~4글자 찾기
    name_pat = r'이름\s*([가-힣]{2,4})'

    # 이름 추출
    names = re.findall(name_pat, text)

    # '생년월일(6자리)' 다음에 오는 생년월일 6자리 찾기
    birth_pat = r'생년월일6자리\s*((?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1])))'
    
    # 생년월일 추출
    birth = re.findall(birth_pat, text)

    # '주소' 다음에 오는 주소 찾기
    # ㅇㅇ도/시/군/구/면/읍/리/로
    # 11(-11)
    # 1(번)길 11-11
    # ㅇㅇ2길 11
    # 도로명 주소 = 주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*) -> 수정 완료
    # +상세 주소 = r'주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*\s?[가-힣]*\s?[가-힣]*\s?[0-9]*동?\s?[0-9]*호?)'
    #addr_pat = r'주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*\s?[가-힣]*\s?[0-9]*동?\s?[0-9]*호?)'
    addr_pat = r'주소\s*([가-힣\s]+\s?[0-9]*\s?번?길?\s?[0-9]*\s?-?\s?[0-9]*\s?[가-힣]*\s?[가-힣]*\s?[0-9]*동?\s?[0-9]*호?)(?=연락처)'

    # 주소 추출
    addr = re.findall(addr_pat, text)

    # '연락처' 다음에 오는 연락처 11자리 찾기
    phone_pat = r'연락처\s*(^02.{0}|^01.{1}|[0-9]{3}-?\s?[0-9]+-?\s?[0-9]{4})'

    # 연락처 추출
    phone = re.findall(phone_pat, text)

    ##### 학력 사항 #####
    # 학력 추출
    edu_info1_pat = r'(?<=학 력 사 항)(.*?)(?=경 력 사 항)'
    edu_info1 = re.search(edu_info1_pat, text).group(1)
    print(edu_info1)

    # 학력_기간 추출
    edu_period_pat = r'(\d{4}년 \d{1,2}월~\d{4}년 \d{1,2}월)'
    edu_period = re.findall(edu_period_pat, edu_info1)
    
    # 학력_학교명 추출
    edu_orgname_pat = r''
    edu_orgname = re.findall(edu_orgname_pat, text)

    # 학력_기타 추출
    edu_etc_pat = r''
    edu_etc = re.findall(edu_etc_pat, text)


    ##### 경력 사항 #####
    # 경력_기간 추출
    career_period_pat = r''
    career_period = re.findall(career_period_pat, text)

    # 경력_회사명 추출
    career_orgname_pat = r''
    career_orgname = re.findall(career_orgname_pat, text)

    # 경력_기타 추출
    career_etc_pat = r''
    career_etc = re.findall(career_etc_pat, text)


    ##### 자기 소개 #####
    # '자기소개' 다음에 오는 문장 찾기
    #pr_career_pat = r'자기소개\s*([가-힣\s]+)'
    pr_resume_pat = r"자기소개\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=위 기재사항)"

    # 자기소개 추출
    pr_resume = re.findall(pr_resume_pat, text, re.DOTALL)
    
    # github 프로젝트 도메인 찾기
    domain_pat = r'(((http(s?))\:\/\/)?)([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?'

    # github 프로젝트 도메인 추출
    domain = re.search(domain_pat, text)


    ##### 결과 출력 #####
    # 결과 출력_이름
    if names:
        print(names[0])  # 첫 번째 일치 항목 (보통 맨 처음 등장하는 이름이 지원자 이름이므로 -> 필요할 경우 수정)
    else:
        print("이름을 찾을 수 없습니다.")

    # 결과 출력_생년월일
    if birth:
        print(birth[0])
    else:
        print("생년월일(6자리)을 찾을 수 없습니다.")

    # 결과 출력_주소
    if addr:
        print(addr[0])
    else:
        print("주소를 찾을 수 없습니다.")

    # 결과 출력_연락처
    if phone:
        print(phone[0])
    else:
        print("연락처를 찾을 수 없습니다.")
    
    # 결과 출력_학력_기간
    if edu_period:
        print(edu_period)
    else:
        print("학력_기간을 찾을 수 없습니다.")

    # 결과 출력_학력_학교명
    if edu_orgname:
        print(edu_orgname[0])
    else:
        print("학력_학교명을 찾을 수 없습니다.")

    # 결과 출력_학력_기타
    if edu_etc:
        print(edu_etc[0])
    else:
        print("학력_기타를 찾을 수 없습니다.")

    # 결과 출력_경력_기간
    if career_period:
        print(career_period[0])
    else:
        print("경력_기간을 찾을 수 없습니다.")

    # 결과 출력_경력_회사명
    if career_orgname:
        print(career_orgname[0])
    else:
        print("경력_회사명을 찾을 수 없습니다.")
    
    # 결과 출력_경력_기타
    if career_etc:
        print(career_etc[0])
    else:
        print("경력_기타를 찾을 수 없습니다.")
        
    # 결과 출력_github 도메인
    if domain:
        print(domain[0])
    else:
        print("도메인을 찾을 수 없습니다.")

    # 결과 출력_자기소개
    if pr_resume:
        print(pr_resume[0])
    else:
        print("자기소개를 찾을 수 없습니다.")