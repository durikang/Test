import requests
import json
import os

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

        # upload_url을 GitHub Actions 환경 변수로 설정
        if upload_url:
            print(f"::set-output name=upload_url::{upload_url}")
        else:
            print("업로드 URL을 찾을 수 없습니다.")

        print("Release created successfully!")

    except Exception as e:
        print(f"릴리즈 생성 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    create_release()
