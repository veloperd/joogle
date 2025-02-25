from flask import Flask, request, jsonify, render_template
import requests
import getpass  # 사용자 이름 가져오기
import platform  # 운영 체제 정보 가져오기

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['GET'])
def get_info():
    # 클라이언트의 실제 IP 확인 (X-Forwarded-For 우선 사용)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # IP 기반 위치 조회
    ip_info = requests.get(f"https://ipinfo.io/{ip}/json").json()

    # 사용자 기기 정보
    user_agent = request.headers.get('User-Agent', 'Unknown')

    # 서버에서 실행 중인 사용자 계정 이름
    username = getpass.getuser()

    return jsonify({
        "client_ip": ip,
        "location": ip_info.get("loc", "Unknown"),
        "city": ip_info.get("city", "Unknown"),
        "region": ip_info.get("region", "Unknown"),
        "country": ip_info.get("country", "Unknown"),
        "isp": ip_info.get("org", "Unknown"),
        "user_agent": user_agent,
        "server_user": username,
        "os": platform.system(),
        "os_version": platform.version()
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
