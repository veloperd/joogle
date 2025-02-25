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

    # ISP 정보 조회 (ip-api 사용)
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=isp,status,message").json()
        if response["status"] == "fail":
            isp = "정보 없음"
        else:
            isp = response.get("isp", "정보 없음")
    except Exception:
        isp = "정보 없음"

    # 클라이언트 기기 정보
    user_agent = request.headers.get('User-Agent', 'Unknown')

    return jsonify({
        "client_ip": ip,
        "isp": isp,
        "user_agent": user_agent
    })


    return jsonify({
        "client_ip": ip,
        "isp": isp,
        "user_agent": user_agent
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
