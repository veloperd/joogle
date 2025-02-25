from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/get_info', methods=['GET'])
def get_info():
    # IP 정보와 위치 정보 요청 코드
    public_ip = requests.get('https://api64.ipify.org?format=json').json()['ip']
    ip_api = requests.get(f"http://ip-api.com/json/{public_ip}?fields=query,isp,country,city,lat,lon,status,message").json()
    
    ip = ip_api.get("query")
    isp = ip_api.get("isp", "Unknown ISP")
    country = ip_api.get("country", "Unknown Country")
    city = ip_api.get("city", "Unknown City")
    latitude = ip_api.get("lat", "Unknown Latitude")
    longitude = ip_api.get("lon", "Unknown Longitude")
    
    return jsonify({
        "ip": ip,
        "isp": isp,
        "country": country,
        "city": city,
        "latitude": latitude,
        "longitude": longitude
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
