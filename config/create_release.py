import requests
import json
import os
from dotenv import load_dotenv

# .env 파일 로드 (로컬 환경에서만 사용)
load_dotenv()

# GitHub Token 설정
# GitHub Actions에서는 DURI_TOKEN을 사용하고, 로컬에서는 .env 파일에서 로드된 값을 사용합니다.
GITHUB_TOKEN = os.getenv("DURI_TOKEN")
username = 'durikang'
repository = 'Test'

if not GITHUB_TOKEN:
    print("[ERROR] GitHub 토큰이 설정되지 않았습니다. 환경 변수 'DURI_TOKEN'을 확인하세요.")
    exit(1)

def create_release():
    try:
        # 릴리즈 생성하기
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "User-Agent": "MyApp"
        }
        release_data = {
            "tag_name": os.getenv("NEW_TAG"),
            "name": f"Release {os.getenv('NEW_TAG')}",
            "body": f"This is the release for {os.getenv('NEW_TAG')}",
            "draft": False,
            "prerelease": False
        }

        response = requests.post(f"https://api.github.com/repos/{username}/{repository}/releases",
                                 headers=headers, data=json.dumps(release_data))
        response.raise_for_status()

        # 릴리즈 생성이 성공하면 출력
        data = response.json()
        upload_url = data.get("upload_url")

        # GitHub Actions 환경 변수로 설정 (GITHUB_ENV로 저장)
        if upload_url:
            github_env_path = os.getenv('GITHUB_ENV')
            if github_env_path:
                with open(github_env_path, 'a') as github_env:
                    github_env.write(f'upload_url={upload_url}\n')
                print(f"::set-output name=upload_url::{upload_url}")
            else:
                # 로컬 환경에서의 출력을 위해 처리
                print(f"Upload URL: {upload_url}")
        else:
            print("업로드 URL을 찾을 수 없습니다.")

        print("Release created successfully!")

    except requests.exceptions.RequestException as req_err:
        print(f"릴리즈 생성 중 요청 오류가 발생했습니다: {req_err}")
    except Exception as e:
        print(f"릴리즈 생성 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    create_release()
