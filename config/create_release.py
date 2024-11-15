# config/create_release.py
import requests
import json
import os

GITHUB_TOKEN = os.getenv("DURI_TOKEN")
username = 'durikang'
repository = 'Test'


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
        print(f"::set-output name=upload_url::{upload_url}")

        print("Release created successfully!")

    except Exception as e:
        print(f"릴리즈 생성 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    create_release()
