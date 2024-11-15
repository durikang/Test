import requests
import json
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # 환경 변수로부터 GitHub 토큰 가져오기
username = 'durikang'
repository = 'Test'

def update_version_json(latest_version=None):
    try:
        if not latest_version:
            # 최신 릴리즈 정보 가져오기
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "User-Agent": "MyApp"
            }
            response = requests.get(f"https://api.github.com/repos/{username}/{repository}/releases/latest", headers=headers)
            response.raise_for_status()

            # 최신 태그 이름 가져오기
            data = response.json()
            latest_version = data.get("tag_name", "N/A")

            if latest_version == "N/A":
                print("릴리즈 정보를 가져올 수 없습니다.")
                return

        # version.json 파일 업데이트
        version_data = {
            "version": latest_version
        }

        with open('config/version.json', 'w') as version_file:
            json.dump(version_data, version_file, indent=4)

        print(f"version.json 파일이 {latest_version}로 업데이트되었습니다.")

    except Exception as e:
        print(f"버전 업데이트 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    update_version_json()
