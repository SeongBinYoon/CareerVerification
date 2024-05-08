import re
from tika import parser


def ext_career(pdf_path2):

    text_all = parser.from_file(pdf_path2)['content']
    text = re.sub(r'[\n(),]', '', text_all)

    ##### 회사 소개 #####
    #회사명 추출
    #comp_name_pat = r'회사명\s*([가-힣\s]{1,12}㈜)'
    comp_name_pat = r"회 사 명\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=주요사업)"
    comp_name = re.findall(comp_name_pat, text)

    #주요사업 추출
    #business_pattern = r'주요사업\s*([가-힣]{1,12})'
    business_pat = r"주요사업\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=회사규모)"
    business = re.findall(business_pat, text)

    # 자본금 추출
    capstock_pat = r'자 본 금\s*([가-힣a-zA-Z0-9]+)'
    capstock = re.findall(capstock_pat, text)

    # 연매출 추출
    annrev_pat = r'연 매 출\s*([가-힣a-zA-Z0-9]+)'
    annrev = re.findall(annrev_pat, text)

    # 직원수 추출
    empcnt_pat = r'직 원 수\s*([가-힣a-zA-Z0-9]+)'
    empcnt = re.findall(empcnt_pat, text)

    ##### 업무 개요 #####
    #근무 기간 추출
    period_pat = r'\d{4}년 \d{1,2}월~\d{4}년 \d{1,2}월'
    period = re.findall(period_pat,text)
    
    # 근무 부서 추출
    dep_pat = r'근무 부서\s*([가-힣a-zA-Z0-9]+)'
    dep = re.findall(dep_pat, text)

    # 직책(직급) 추출
    pos_pat = r'직책직급\s*([가-힣a-zA-Z0-9]+)'
    pos = re.findall(pos_pat, text)

    #주요 업무 추출
    maintask_pat = r'주요 업무\s*([가-힣\s]+?)\s*업무 내용'
    maintask = re.findall(maintask_pat,text)

    # 업무 내용 추출
    detailtask_pat = re.compile(r'업무 내용(.*?)■', re.DOTALL)
    detailtask = detailtask_pat.search(text)

    #업무 성과 추출
    perf_pat = re.compile(r'업무 성과(.*?)■', re.DOTALL)
    perf = perf_pat.search(text)

    ##### 업무 관련 자격 사항 #####
    # 보유지식/능력 추출
    skill_pat = r"보유지식/능력\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=자 격 증)"
    skill = re.findall(skill_pat, text)

    # 자격증 추출
    qual_pat = r"자 격 증\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=교육/연수)"
    qual = re.findall(qual_pat, text)

    # 교육/연수 추출
    edu_pat = r"교육/연수\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)"
    edu = re.findall(edu_pat, text)

    ##### 이직 사유 #####
    # 이직 사유 추출
    switjob_pat = r"이직사유\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)"
    switjob = re.findall(switjob_pat, text)

    ##### 자기 PR #####
    # 자기 PR 추출
    pr_career_pat = r"자기PR\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)"
    pr_career = re.findall(pr_career_pat, text, re.DOTALL)


    ##### 결과 출력 #####
    # 결과 출력_회사명
    if comp_name:
        print("회사명: " + comp_name[0]) 
    else:
        print("회사명을 찾을 수 없습니다.")

    # 결과 출력_주요 사업
    if comp_name:
        print("주요사업: " + business[0]) 
    else:
        print("사업을 찾을 수 없습니다.")

    # 결과 출력_자본금
    if capstock:
        print("자본금: ", capstock[0])
    else:
        print("자본금을 찾을 수 없습니다.")
    
    # 결과 출력_연매출
    if annrev:
        print("연매출: ", annrev[0])
    else:
        print("연매출을 찾을 수 없습니다.")

    # 결과 출력_직원수
    if empcnt:
        print("직원 수: ", empcnt[0])
    else:
        print("직원 수를 찾을 수 없습니다.")

    # 결과 출력_근무 기간
    if period:
        print("근무기간: " + period[0]) 
    else:
        print("근무기간을 찾을 수 없습니다.")
    
    # 결과 출력_근무 부서
    if dep:
        print("근무 부서: ", dep[0])
    else:
        print("근무 부서를 찾을 수 없습니다.")

    # 결과 출력_직책(직급)
    if pos:
        print("직책(직급): ", pos[0])
    else:
        print("직책(직급)을 찾을 수 없습니다.")

    # 결과 출력_주요 업무
    if maintask:
        print("주요 업무: " + maintask[0])
    else:
        print("주요 업무를 찾을 수 없습니다.")

    # 결과 출력_업무 내용
    if detailtask:
        extracted_text = detailtask.group(1).strip()
        formatted_text = re.sub(r'(\d+)\.', r'\n\1.', extracted_text)
        print("업무 내용:" + formatted_text)
    else:
        print("매칭되는 텍스트가 없습니다.")

    # 결과 출력_업무 성과
    if perf:
        extracted_text = perf.group(1).strip()
        formatted_text = re.sub(r'(\d+)\.', r'\n\1.', extracted_text)
        print("업무 성과:" + formatted_text)
    else:
        print("매칭되는 텍스트가 없습니다.")

    # 결과 출력_보유지식/능력
    if skill:
        print("보유지식/능력: ", skill[0])
    else:
        print("보유지식/능력을 찾을 수 없습니다.")
    
    # 결과 출력_자격증
    if qual:
        print("자격증: ", qual[0])
    else:
        print("자격증을 찾을 수 없습니다.")

    # 결과 출력_교육/연수
    if edu:
        print("교육/연수: ", edu[0])
    else:
        print("교육/연수를 찾을 수 없습니다.")

    # 결과 출력_이직 사유
    if switjob:
        print("이직 사유: ", switjob[0])
    else:
        print("이직 사유를 찾을 수 없습니다.")

    # 결과 출력_자기 PR
    if pr_career:
        print("자기PR: ", pr_career[0])
    else:
        print("자기PR을 찾을 수 없습니다.")