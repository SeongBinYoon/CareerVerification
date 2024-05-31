from flask import Flask, request, render_template, redirect, url_for, flash
import os
import extract as ext1
import extract2 as ext2
import settings as sts
import patent as pat
import contributor as con
import project_sc as proj
import summarize_text as summ_t
#from werkzeug.utils import secure_filename


# 플라스크 정의
app = Flask(__name__)
app.config["SECRET_KEY"] = sts.configkey

# pdf 저장 폴더명
UPLOAD_BASE = 'uploads'
folder_name = 'uploadfiles'
    

# 시작 페이지: main menu - 홈
@app.route('/')
def index():

    return redirect(url_for('home'))


# main menu - 홈
@app.route('/home')
def home():

    return render_template('home.html')


# main menu - 파일 업로드
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    return render_template('file_upload.html')


# main menu - 검증 결과
@app.route('/results')
def show_results():

    return render_template('view_texts.html', 
                                   files_pinfo=ext1.pinfo, 
                                   files_vres=ext2.vres, 
                                   files_vcat=ext2.vcat,
                                   zip=zip)


# 이력서 및 경력기술서 리스트 보여줌: main menu - 문서 리스트 및 검증
@app.route('/files/resume')
def file_list_resume():
    # 쿼리 실행
    conn = sts.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT applicant_id, resume_pdf_addr, cv_pdf_addr FROM application")
    files = cursor.fetchall()
    conn.close()
    #print(ext2.vres) # 검증 딕셔너리 확인용

    return render_template('resume_file_list.html', files=files)


# 이력서, 경력기술서 업로드 버튼
@app.route('/upload/resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        filename1 = file1.filename
        filename2 = file2.filename
        if (file1 and filename1.endswith('.pdf')) and (file2 and filename2.endswith('.pdf')):
            
            upload_folder = os.path.join(UPLOAD_BASE, folder_name)
            # 폴더가 존재하지 않으면 생성
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            # 파일 저장 경로 설정
            path1 = os.path.join(upload_folder, file1.filename)
            path2 = os.path.join(upload_folder, file2.filename)
            # 파일 저장
            file1.save(path1)
            file2.save(path2)
            
            # db에 pdf 경로 저장
            try:
                conn = sts.get_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO application (application_date, resume_pdf_addr, cv_pdf_addr) VALUES (now(), %s, %s)", (path1, path2))
                conn.commit()
            except Exception as e:
                conn.rollback()
                return f"Database error: {e}", 500
            finally:
                conn.close()

            # 성공적으로 업로드되면 '이력서 리스트' 탭으로 redirecting
            return redirect(url_for('file_list_resume'))
        
        return 'Invalid file', 400
    else:
        return render_template('file_upload.html')


# 리스트에서 선택 후 검증 버튼
# 리스트에서 선택한 항목에 대한 file_ids 찾아 해당 addr 받아와 path에 저장, extract, extract2 추출 함수 호출
@app.route('/action/resume', methods=['POST'])
def verify_resume():

    global path_resume
    global path_career
    file_ids = request.form.getlist('file_ids')

    # 개인 정보 딕셔너리 초기화
    ext1.pinfo = {'name': "", 
                  'birth': "", 
                  'address': "", 
                  'phone': "",
                  'career': "",
                  'edu_period': [],
                  'edu_orgname': [],
                  'career_period': [],
                  'career_orgname': []}
    
    # 검증 항목 딕셔너리 초기화
    ext2.vcat = {'patent': [],
                 'project': [],
                 'contributor': [],
                 'award': []}
    
    # 검증 결과 딕셔너리 초기화
    ext2.vres = {'patent': [], 
                 'project': [], 
                 'contributor': [], 
                 'award': []}
    
    # 요약 항목 딕셔너리 초기화
    ext2.summ_text = {'detailtask': [], 
                     'perf': [],
                     'switjob': [],
                     'pr_career': []}

    # 요약 결과 딕셔너리 초기화
    ext2.summ_res = {'text': []}

    ext2.gpt_res = {'proj': [],
                    'award': []}

    # 검증 버튼 클릭 시
    if 'verify' in request.form['action']:
        # file_ids가 존재하고, 그 크기가 1(하나의 항목만 체크)인 경우 예외처리
        if file_ids and len(file_ids) == 1:
            
            conn = sts.get_db()
            cursor = conn.cursor()
            query = "SELECT resume_pdf_addr, cv_pdf_addr FROM application WHERE applicant_id = " + file_ids[0]
            cursor.execute(query)
            # 이력서 = 0번 인덱스, 경력기술서 = 1번 인덱스
            all_paths = cursor.fetchall()
            conn.close()

            # 이력서 경로
            path_resume = all_paths[0][0]
            # 경력기술서 경로
            path_career = all_paths[0][1]
            
            # 체크한 항목의 파일이 로컬 PC에 없는 경우 예외처리
            try:
                # 추출 트리거
                ext_trigger(path_resume, path_career)
            except FileNotFoundError:
                flash("해당 파일은 현재 PC에 없습니다. 업로드해주세요.")
                return file_list_resume()
            
            # 검증 강제 종료 시 예외처리
            try:
                # 검증 트리거
                ver_trigger(sts.webdriver_path, sts.api_key)
            
            except Exception as e:
                flash("검증이 강제 종료되었습니다.")
                return file_list_resume()
            
            try:
                # 요약 트리거
                summ_triger(sts.api_key)
            
            except Exception as e:
                flash("요약이 강제 종료되었습니다.")
                return file_list_resume()

            return render_template('view_texts.html', 
                                   files_pinfo=ext1.pinfo, 
                                   files_vres=ext2.vres, 
                                   files_vcat=ext2.vcat,
                                   summ_text = ext2.summ_res,
                                   gpt_res = ext2.gpt_res, 
                                   zip=zip)
        
        # 두 개 이상 항목 체크 후 검증 클릭 시 예외처리
        elif file_ids and len(file_ids) > 1:
            flash("하나의 항목만 체크해주세요.")
            return file_list_resume()

        # 체크 없이 검증 클릭 시 예외처리
        else:
            flash("항목에 체크해주세요.")
            #return render_template('resume_file_list.html')
            return file_list_resume()
    
    # 삭제 버튼 클릭 시
    elif 'delete' in request.form['action']:
        if file_ids:
            delete_resume(file_ids[0])
        return redirect(url_for('file_list_resume'))
    else:
        return render_template('home.html')


# 추출 함수를 호출하는 추출 트리거 프로시저
def ext_trigger(path1, path2):
    ext1.ext_resume(path1)
    ext2.ext_career(path2)


# 검증 함수를 호출하는 검증 트리거 프로시저
def ver_trigger(webdriver_path, api_key):
    # 특허 검증
    for cnt in range(len(ext2.patent_name)):
        pat.patent_ver(webdriver_path, 
                       ext2.patent_name[cnt], 
                       [ext1.names[0], ext2.patent_org[cnt]])

    # 프로젝트 검증
    for cnt in range(len(ext2.proj_name)):
        proj.proj_ver(ext1.names[0], 
                      [ext2.proj_name[cnt], 
                       ext2.proj_org[cnt]], 
                       mode = "project", 
                       gpt_api_key=api_key)

    # contributor 검증
    for cnt in range(len(ext2.github_repo)):
        con.contributor_ver(webdriver_path, 
                            ext2.github_repo[cnt], 
                            ext2.github_id[cnt])

    # 수상내역 검증
    for cnt in range(len(ext2.award_name)):
        proj.proj_ver(ext2.award_name[cnt], 
                      [ext2.award_org[cnt], 
                       ext2.award_team[cnt]], 
                       mode = "award", 
                       gpt_api_key=api_key)

def summ_triger(api_key):
    answer = summ_t.summarize_text(ext2.summ_text,api_key)
    ext2.summ_res['text'].append(answer)

# 리스트에서 선택한 이력서, 경력기술서 삭제
@app.route('/action/resume', methods=['POST'])
def delete_resume(file_id):
    try:
        conn = sts.get_db()
        cursor = conn.cursor()
        # 파일 경로 가져오기
        cursor.execute("SELECT resume_pdf_addr, cv_pdf_addr FROM application WHERE applicant_id = %s", (file_id,))
        paths = cursor.fetchone()
        
        if paths:
            # 파일 삭제
            for path in paths:
                if os.path.exists(path):
                    os.remove(path)

            # DB에서 삭제
            cursor.execute("DELETE FROM application WHERE applicant_id = %s", (file_id,))
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error deleting resume: {e}")
    finally:
        conn.close()


def init_db():
    return sts.get_db()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)