import re
import PyPDF2
from tika import parser

#작성자: 안도형

#PDF 텍스트 추출 및 간소화
def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

path = ""
text_all = extract_text_from_pdf(path)

text = re.sub(r'[\n(),]', '', text_all)
#print(text)

#회사명 추출
name_pattern = r'회사명\s*([가-힣\s]{1,12})'

company_name = re.findall(name_pattern, text)

if company_name:
    print("회사명: " + company_name[0]) 
else:
    print("회사명을 찾을 수 없습니다.")


#주요사업 추출
business_pattern = r'주요사업\s*([가-힣/]{1,12})'

business_name = re.findall(business_pattern, text)

if company_name:
    print("주요사업: " + business_name[0]) 
else:
    print("사업을 찾을 수 없습니다.")


#근무기간 추출
period_pattern = r'\d{4}년 \d{1,2}월~\d{4}년 \d{1,2}월'

employment_period = re.findall(period_pattern,text)

if employment_period:
    print("근무기간: " + employment_period[0]) 
else:
    print("근무기간을 찾을 수 없습니다.")


#주요업무 추출
work_pattern = r'주요 업무\s*([가-힣\s]+?)\s*업무 내용'
main_work = re.findall(work_pattern,text)

if main_work:
    print("주요 업무: " + main_work[0])
else:
    print("주요 업무를 찾을 수 없습니다.")


#업무 성과 추출
# 정규식 패턴
work_performence_pattern = re.compile(r'업무 성과(.*?)■', re.DOTALL)

# 매칭된 텍스트 추출
work_performance = work_performence_pattern.search(text)

if work_performance:
    extracted_text = work_performance.group(1).strip()
    formatted_text = re.sub(r'(\d+)\.', r'\n\1.', extracted_text)
    print("업무 성과:" + formatted_text)
else:
    print("매칭되는 텍스트가 없습니다.")