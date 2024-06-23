from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import source.ext_career as ext2
import requests

def contributor_ver(webdriver_path, github_url, id):
    service = webdriver.chrome.service.Service(executable_path=webdriver_path)
    # GitHub API URL 생성
    owner_repo = github_url.split('github.com/')[-1]
    api_url = f'https://api.github.com/repos/{owner_repo}/contributors'

    # GitHub API 요청 보내기
    response = requests.get(api_url)
    
    if response.status_code == 200:
        contributors = response.json()
        found = any(contributor['login'] == id for contributor in contributors)
        
        if found:
            ext2.vres['contributor'].append("참여 내역이 있습니다.")
        else:
            ext2.vres['contributor'].append("참여 내역이 없습니다.")
        
        print(ext2.vres)
    else:
        print(f"Error: Unable to fetch contributors. Status code {response.status_code}")