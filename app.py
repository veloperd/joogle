from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['GET'])
def get_info():
    # 클라이언트 IP 확인
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # ISP 정보 조회 (Unknown 방지)
    try:
        ip_info = requests.get(f"https://ipinfo.io/{ip}/json").json()
        isp = ip_info.get("org", "정보 없음")  # ISP 정보 없을 경우 기본값 설정
    except Exception:
        isp = "정보 없음"

    # 클라이언트 기기 정보
    user_agent = request.headers.get('User-Agent', 'Unknown')

    return jsonify({
        "client_ip": ip,
        "isp": isp,
        "user_agent": user_agent
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
