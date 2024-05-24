import re
from tika import parser


# 검증 항목 및 검증 결과 딕셔너리 선언 및 초기화
global vcat
global vres
vcat = {'patent': [],
        'project': [],
        'contributor': [],
        'award': []}

vres = {'patent': [],
        'project': [],
        'contributor': [],
        'award': []}


def ext_career(pdf_path2):

    ##### 전역 변수 #####
    global patent_name
    global patent_org
    global github_id
    global github_repo
    global proj_name
    global proj_org


    text_all = parser.from_file(pdf_path2)['content']
    text = re.sub(r'[\n(),]', '', text_all)
    #print(text) # 정규표현식 수정용

    ##### 회사 소개 #####

    #회사명 추출
    #comp_name_pat = r'회사명\s*([가-힣\s]{1,12}㈜)'
    comp_name_pat = r"회 사 명\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s주요사업)"
    comp_name = re.findall(comp_name_pat, text)

    #주요사업 추출
    #business_pattern = r'주요사업\s*([가-힣]{1,12})'
    business_pat = r"주요사업\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s회사규모)"
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
    maintask = re.findall(maintask_pat, text)

    # 업무 내용 추출
    #detailtask_pat = re.compile(r'업무 내용(.*?)■', re.DOTALL)
    #detailtask = detailtask_pat.search(text)
    detailtask_pat = r'업무 내용\s*(.*?)\s*업무 성과'
    detailtask = re.findall(detailtask_pat, text)

    #업무 성과 추출
    #perf_pat = re.compile(r'업무 성과(.*?)■', re.DOTALL)
    #perf = perf_pat.search(text)
    perf_pat = r'업무 성과\s*(.*?)\s*(?=경력[2-9]|업무 관련 사항)'
    perf = re.findall(perf_pat, text)

    ##### 업무 관련 사항 #####

    # 프로젝트 내역 추출
    # 프로젝트명 추출
    proj_name_pat = r"프로젝트명\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s기관명)"
    proj_name = re.findall(proj_name_pat, text)

    # 기관명 추출
    proj_org_pat = r"기관명\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s프로젝트 상세)"
    proj_org = re.findall(proj_org_pat, text)

    # 프로젝트 상세 추출
    proj_detail_pat = r"프로젝트 상세\s*-?\s?([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\sGithub ID)"
    proj_detail = re.findall(proj_detail_pat, text)

    # Github ID 추출
    github_id_pat = r"Github ID\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\sGithub Repository URL)"
    github_id = re.findall(github_id_pat, text)

    # Github Repo URL 추출
    #github_repo_pat = r'(((http(s?))\:\/\/)?)([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?'
    #github_repo = re.search(github_repo_pat, text)
    github_repo_pat = r"Github Repository URL\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s\s■)"
    github_repo = re.findall(github_repo_pat, text)


    
    # 수상 내역 추출
    # 상훈명 추출
    award_name_pat = r"상훈명\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s수여기관)"
    award_name = re.findall(award_name_pat, text)
    
    # 수여기관 추출
    award_org_pat = r"수여기관\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s수상일자)"
    award_org = re.findall(award_org_pat, text)

    # 수상일자 추출
    award_date_pat = r"수상일자\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s팀명성명)"
    award_date = re.findall(award_date_pat, text)

    # 팀명(성명) 추출
    award_team_pat = r"팀명성명\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s수상내역)"
    award_team = re.findall(award_team_pat, text)

    # 수상내역 추출
    award_detail_pat = r"수상내역\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s\s■\s특허 사항)"
    award_detail = re.findall(award_detail_pat, text)


    # 특허 사항 추출
    # 특허명 추출
    patent_name_pat = r"특허명\d+\s(.*?)(?=\s특허 출원인|$)"
    patent_name = re.findall(patent_name_pat, text)

    # 특허 출원인 추출
    patent_org_pat = r"특허 출원인\s(.*?)(?=\s특허명|\s\s■)"
    patent_org = re.findall(patent_org_pat, text)


    # 자격 사항 추출
    # 보유지식/능력 추출
    skill_pat = r"보유지식/능력\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s자 격 증)"
    skill = re.findall(skill_pat, text)

    # 자격증 추출
    qual_pat = r"자 격 증\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)(?=\s교육/연수)"
    qual = re.findall(qual_pat, text)

    # 교육/연수 추출
    edu_pat = r"교육/연수\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)\s\s■"
    edu = re.findall(edu_pat, text)

    ##### 이직 사유 #####
    # 이직 사유 추출
    switjob_pat = r"이직사유\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)\s\s■"
    switjob = re.findall(switjob_pat, text)

    ##### 자기 PR #####
    # 자기 PR 추출
    pr_career_pat = r"자기PR\s*([가-힣a-zA-Z0-9\s\(\)\[\]㈜{}.,!?;:\"'`\-_+=@#$%^&*~<>\/\\|]*)"
    pr_career = re.findall(pr_career_pat, text, re.DOTALL)


    ##### 결과 출력 #####
    # 결과 출력_회사명
    if comp_name:
        print(comp_name) 
    else:
        print("회사명을 찾을 수 없습니다.")

    # 결과 출력_주요 사업
    if comp_name:
        print(business) 
    else:
        print("사업을 찾을 수 없습니다.")

    # 결과 출력_자본금
    if capstock:
        print(capstock)
    else:
        print("자본금을 찾을 수 없습니다.")
    
    # 결과 출력_연매출
    if annrev:
        print(annrev)
    else:
        print("연매출을 찾을 수 없습니다.")

    # 결과 출력_직원수
    if empcnt:
        print(empcnt)
    else:
        print("직원 수를 찾을 수 없습니다.")

    # 결과 출력_근무 기간
    if period:
        print(period) 
    else:
        print("근무기간을 찾을 수 없습니다.")
    
    # 결과 출력_근무 부서
    if dep:
        print(dep)
    else:
        print("근무 부서를 찾을 수 없습니다.")

    # 결과 출력_직책(직급)
    if pos:
        print(pos)
    else:
        print("직책(직급)을 찾을 수 없습니다.")

    # 결과 출력_주요 업무
    if maintask:
        print(maintask)
    else:
        print("주요 업무를 찾을 수 없습니다.")

    # 결과 출력_업무 내용
    #if detailtask:
    #    extracted_text = detailtask.group(1).strip()
    #    formatted_text = re.sub(r'(\d+)\.', r'\n\1.', extracted_text)
    #    print("업무 내용:" + formatted_text)
    #else:
    #    print("매칭되는 텍스트가 없습니다.")
    if detailtask:
        print(detailtask)
    else:
        print("업무 내용을 찾을 수 없습니다.")

    # 결과 출력_업무 성과
    #if perf:
    #    extracted_text = perf.group(1).strip()
    #    formatted_text = re.sub(r'(\d+)\.', r'\n\1.', extracted_text)
    #    print("업무 성과:" + formatted_text)
    #else:
    #    print("매칭되는 텍스트가 없습니다.")
    if perf:
        print(perf)
    else:
        print("업무 내용을 찾을 수 없습니다.")

    # 결과 출력_프로젝트명
    if proj_name:
        for i in range(len(proj_name)):
            vcat['project'].append(proj_name[i])
        print(proj_name)
    else:
        print("프로젝트명을 찾을 수 없습니다.")

    # 결과 출력_기관명
    if proj_org:
        print(proj_org)
    else:
        print("기관명을 찾을 수 없습니다.")

    # 결과 출력_프로젝트 상세
    if proj_detail:
        print(proj_detail)
    else:
        print("프로젝트 상세를 찾을 수 없습니다.")

    # 결과 출력_Github ID
    if github_id:
        print(github_id)
    else:
        print("github id를 찾을 수 없습니다.")

    # 결과 출력_Github repository URL
    if github_repo:
        for i in range(len(github_repo)):
            vcat['contributor'].append(github_repo[i])
        print(github_repo)
    else:
        print("github repository URL을 찾을 수 없습니다.")

    # 결과 출력_상훈명
    if award_name:
        for i in range(len(award_name)):
            vcat['award'].append(award_name[i])
        print(award_name)
    else:
        print("상훈명을 찾을 수 없습니다.")

    # 결과 출력_수여기관
    if award_org:
        print(award_org)
    else:
        print("수여기관을 찾을 수 없습니다.")

    # 결과 출력_수상일자
    if award_date:
        print(award_date)
    else:
        print("수상일자를 찾을 수 없습니다.")

    # 결과 출력_팀명(성명)
    if award_team:
        print(award_team)
    else:
        print("팀명(성명)을 찾을 수 없습니다.")

    # 결과 출력_수상내역
    if award_detail:
        print(award_detail)
    else:
        print("수상내역을 찾을 수 없습니다.")

    # 결과 출력_특허명
    if patent_name:
        for i in range(len(patent_name)):
            vcat['patent'].append(patent_name[i])
        print(patent_name)
    else:
        print("특허명을 찾을 수 없습니다.")

    # 결과 출력_특허 출원인
    if patent_org:
        print(patent_org)
    else:
        print("특허 출원인을 찾을 수 없습니다.")

    # 결과 출력_보유지식/능력
    if skill:
        print(skill)
    else:
        print("보유지식/능력을 찾을 수 없습니다.")
    
    # 결과 출력_자격증
    if qual:
        print(qual)
    else:
        print("자격증을 찾을 수 없습니다.")

    # 결과 출력_교육/연수
    if edu:
        print(edu)
    else:
        print("교육/연수를 찾을 수 없습니다.")

    # 결과 출력_이직 사유
    if switjob:
        print(switjob)
    else:
        print("이직 사유를 찾을 수 없습니다.")

    # 결과 출력_자기 PR
    if pr_career:
        print(pr_career)
    else:
        print("자기PR을 찾을 수 없습니다.")