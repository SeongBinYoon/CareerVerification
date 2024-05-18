from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import pymysql
import os
#from werkzeug.utils import secure_filename
#import subprocess

# 플라스크 정의
app = Flask(__name__)

# pdf 저장 폴더명
UPLOAD_BASE = 'uploads'
folder_name = 'uploadfiles'

# db 연결
def get_db():
    conn = pymysql.connect(
        host='',
        user='',
        password='',
        db='',
        charset=''
    )
    
    return conn


# 시작 페이지: main menu - 파일 업로드
@app.route('/')
def index():

    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

# main menu - 파일 업로드
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    return render_template('file_upload.html')
    

# 이력서 리스트 보여줌
@app.route('/files/resume')
def file_list_resume():
    # 쿼리 실행
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT applicant_id, resume_pdf_addr FROM application")
    files = cursor.fetchall()
    conn.close()

    return render_template('resume_file_list.html', files=files)


# 경력기술서 리스트 보여줌
@app.route('/files/technical')
def file_list_technical():
    # 쿼리 실행
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT applicant_id, cv_pdf_addr FROM application")
    files = cursor.fetchall()
    conn.close()
    
    return render_template('technical_file_list.html', files=files)


# 이력서, 경력기술서 업로드 버튼
@app.route('/upload/resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        filename1 = file1.filename
        filename2 = file2.filename
        if (file1 and filename1.endswith('.pdf')) and (file2 and filename2.endswith('.pdf')):
            #path1 = os.path.abspath(filename1)
            #path2 = os.path.abspath(filename2)
            
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
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO application (application_date, resume_pdf_addr, cv_pdf_addr) VALUES (now(), %s, %s)", (path1, path2))
                conn.commit()
            except Exception as e:
                conn.rollback()
                return f"Database error: {e}", 500
            finally:
                conn.close()
            return redirect(url_for('file_list_resume'))
        return 'Invalid file', 400
    else:
        return render_template('file_upload.html')


'''
def save_temp_file(filename, content):
    """임시 파일을 저장하고 경로를 반환"""
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(content)
    return file_path
'''
'''
@app.route('/verify/technical/<int:file_id>')
@app.route('/verify/resume/<int:file_id>')
def verify_file(file_id):
    """파일 검증: 파일 내용을 추출하고 결과를 보여줌"""
    table = 'technical_files' if 'technical' in request.path else 'resume_files'
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT filename, content FROM {table} WHERE id = ?", (file_id,))
    file_data = cursor.fetchone()
    conn.close()
    if file_data:
        file_path = save_temp_file(file_data[0], file_data[1])  # 바이너리 데이터 저장
        result = subprocess.run(['python', 'extract.py', file_path], capture_output=True, text=True)
        extracted_text = result.stdout
        return render_template('view_text.html', text=extracted_text)
    return 'File not found', 404
'''

# 리스트에서 선택한 이력서, 경력기술서 경로 가져오기

# 이력서, 경력기술서 추출

# 이력서, 경력기술서 verify 버튼 

# 리스트에서 선택한 이력서, 경력기술서 삭제 - 해당 id의 모든 정보 db에서 삭제 (추후 구현)
@app.route('/action/technical', methods=['POST'])
@app.route('/action/resume', methods=['POST'])
def delete_files():
    file_id = request.form.getlist('file_ids')
    if file_id:
            print(file_id)
            conn = get_db()
            cursor = conn.cursor()
            #query = f'DELETE FROM {table} WHERE id IN ({", ".join(["?"]*len(file_id))})'
            query = f'DELETE FROM application WHERE applicant_id IN ({", ".join(["?"]*len(file_id))})'
            try:
                cursor.execute(query, file_id)
                conn.commit()
            finally:
                conn.close()
    #return redirect(url_for('file_list_technical' if 'technical' in request.path else 'file_list_resume'))
'''
# 파일 삭제 및 검증 구현
@app.route('/action/technical', methods=['POST'])
@app.route('/action/resume', methods=['POST'])
def handle_files():
    """파일 삭제 및 검증 구현"""
    table = 'technical_files' if 'technical' in request.path else 'resume_files'
    file_ids = request.form.getlist('file_ids')
    if 'delete' in request.form['action']:
        if file_ids:
            conn = get_db()
            cursor = conn.cursor()
            query = f'DELETE FROM {table} WHERE id IN ({", ".join(["?"]*len(file_ids))})'
            try:
                cursor.execute(query, file_ids)
                conn.commit()
            finally:
                conn.close()
        return redirect(url_for('file_list_technical' if 'technical' in request.path else 'file_list_resume'))
    elif 'verify' in request.form['action']:
        if file_ids:
            texts = []
            for file_id in file_ids:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute(f"SELECT filename, content FROM {table} WHERE id = ?", (file_id,))
                file_data = cursor.fetchone()
                conn.close()
                if file_data:
                    file_path = save_temp_file(file_data[0], file_data[1])
                    result = subprocess.run(['python', 'extract.py', file_path], capture_output=True, text=True)
                    texts.append((file_data[0], result.stdout))
                    os.remove(file_path)
            return render_template('view_texts.html', texts=texts)
    return 'Invalid request', 400
'''
def init_db():
    """데이터베이스 초기화"""
    #with app.app_context():
    get_db()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
