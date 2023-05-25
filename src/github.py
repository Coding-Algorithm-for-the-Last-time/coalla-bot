import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()
env = os.environ.get

# GitHub 액세스 토큰 설정
TOKEN = env("GITHUB_ACCESS_TOKEN")

# 파일을 푸시할 저장소 정보
owner = "Coding-Algorithm-for-the-Last-time"
repo = "Today-I-solved"


def make_commit(path, title, content, commit_msg):
    # 푸시할 파일 경로 및 내용
    file_path = f"{path}/{title}.md"
    file_content = content

    # 커밋을 생성하기 위한 API 엔드포인트
    commit_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    # 파일 내용을 Base64로 인코딩
    file_content_encoded = base64.b64encode(file_content.encode()).decode()

    # 커밋 생성 요청 헤더
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # 커밋 생성 요청 데이터
    data = {
        "message": commit_msg,
        "content": file_content_encoded
    }

    # 커밋 생성 요청
    response = requests.put(commit_url, headers=headers, json=data)

    # 응답 확인
    if response.status_code == 201:
        print("File pushed successfully.")
    else:
        print("Failed to push file.")
        print("Response:", response.json())