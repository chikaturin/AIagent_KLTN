from flask import Flask, request
from routes.time_management import timeplan_bp
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

app.register_blueprint(timeplan_bp, url_prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Chat Server!"}


@app.before_request
def log_request_info():
    print("📥 Request:", request.method, request.url)
    print("🔧 Headers:", dict(request.headers))
    print("🧾 Body:", request.get_data().decode("utf-8"))


def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "127.0.0.1"


if __name__ == "__main__":
    ip = get_local_ip()
    print(f"🚀 Server đang chạy tại: http://{ip}:5000")
    print("🌐 Bạn có thể truy cập API trên thiết bị khác cùng Wi-Fi bằng IP này.")
    app.run(host="0.0.0.0", port=5000, debug=True)
