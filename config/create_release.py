import requests
import json
import os

# GitHub Token 설정 (GitHub Actions에서는 시크릿으로 주입됨)
GITHUB_TOKEN = os.getenv("DURI_TOKEN")  # GitHub Actions에서 사용되는 DURI_TOKEN 시크릿 가져오기

username = 'durikang'
repository = 'Test'

def create_release(new_tag):
    if not GITHUB_TOKEN:
        print("[ERROR] GitHub 토큰이 설정되지 않았습니다. GitHub Actions 환경에서 실행해야 합니다.")
        return

    try:
        # 릴리즈 생성하기
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "User-Agent": "MyApp"
        }
        release_data = {
            "tag_name": new_tag,
            "name": f"Release {new_tag}",
            "body": f"This is the release for {new_tag}",
            "draft": False,
            "prerelease": False
        }

        response = requests.post(f"https://api.github.com/repos/{username}/{repository}/releases",
                                 headers=headers, data=json.dumps(release_data))
        response.raise_for_status()

        # 릴리즈 생성이 성공하면 출력
        data = response.json()
        upload_url = data.get("upload_url")

        if upload_url:
            print(f"Upload URL: {upload_url}")
        else:
            print("업로드 URL을 찾을 수 없습니다.")

        print("Release created successfully!")

    except requests.exceptions.RequestException as req_err:
        print(f"릴리즈 생성 중 요청 오류가 발생했습니다: {req_err}")
    except Exception as e:
        print(f"릴리즈 생성 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    new_tag = os.getenv("NEW_TAG", "v1.0.0")  # 기본값을 제공하여 로컬 테스트도 가능하게 함
    create_release(new_tag)
