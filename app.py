from flask import Flask, request, jsonify, render_template
import requests
import getpass

app = Flask(__name__)

@app.route('/')
def index():
    # 현재 사용자 이름 추출
    username = getpass.getuser()
    
    # 사용자 이름만 HTML로 전달
    return render_template('index.html', username=username)

@app.route('/get_info', methods=['GET'])
def get_info():
    # 클라이언트의 IP 주소 얻기
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    # 공용 IP를 강제로 확인 (ipify.org 사용)
    public_ip = requests.get('https://api64.ipify.org?format=json').json()['ip']

    # IP 조회 API 1 (ip-api.com)
    ip_api = requests.get(f"http://ip-api.com/json/{public_ip}?fields=query,isp,country,city,lat,lon,status,message").json()

    # IP 조회 API 2 (ipinfo.io)
    ipinfo = requests.get(f"https://ipinfo.io/{public_ip}/json").json()

    # IP 정보 정리
    ip = ip_api.get("query", client_ip)
    isp = ip_api.get("isp", "Unknown ISP")
    country = ip_api.get("country") or ipinfo.get("country", "Unknown")
    city = ip_api.get("city") or ipinfo.get("city", "Unknown")
    
    # 위도, 경도 정보 처리 (둘 중 하나라도 있으면 사용)
    latitude = ip_api.get("lat") or ipinfo.get("loc", "0,0").split(",")[0]
    longitude = ip_api.get("lon") or ipinfo.get("loc", "0,0").split(",")[1]

    return jsonify({
        "ip": ip,
        "isp": isp,
        "country": country,
        "city": city,
        "latitude": latitude,
        "longitude": longitude,
        "user_agent": user_agent
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
