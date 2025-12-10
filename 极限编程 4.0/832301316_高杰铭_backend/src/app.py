from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from exts import db
from controller.user import bp as user_bp
import config
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(config.Config)

# 初始化扩展
db.init_app(app)
migrate = Migrate(app, db)
# 关键修复：允许前端实际地址跨域（8000端口）
CORS(app, resources={r"/api/*": {
    "origins": [
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "http://8.138.190.252"  # 服务器前端的公网地址（若前端用了端口，需加端口，如:8080）
    ]
}})

# 注册蓝图
app.register_blueprint(user_bp)

# 数据库初始化检查
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("数据库连接成功！")

        from models import User
        old_users = User.query.filter(User.update_time.is_(None)).all()
        for user in old_users:
            user.update_time = user.create_time
        if old_users:
            db.session.commit()
            print(f"修复了 {len(old_users)} 条update_time为空的数据")
    except Exception as e:
        print(f"数据库连接失败：{str(e)}")

# 健康检查接口
@app.route("/api/health")
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)