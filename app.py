from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['GET'])
def get_info():
    # 클라이언트의 실제 IP 가져오기
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # IP 기반 위치 조회
    ip_info = requests.get(f"https://ipinfo.io/{ip}/json").json()

    return jsonify({
        "client_ip": ip,
        "location": ip_info.get("loc", "Unknown"),
        "city": ip_info.get("city", "Unknown"),
        "region": ip_info.get("region", "Unknown"),
        "country": ip_info.get("country", "Unknown"),
        "isp": ip_info.get("org", "Unknown"),
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
