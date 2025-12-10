# 后端网址是否运行
- 你可以直接在浏览器中访问 http://127.0.0.1:5000/api/health
- 如果显示 {"status":"ok"}，说明后端服务正常运行

# 地址簿管理系统 - 后端

这是一个简单的地址簿管理系统后端API服务，提供用户信息的CRUD操作和版本历史记录功能。

## 功能

- 用户创建、查询、更新、删除
- 用户版本历史记录
- 数据验证和错误处理

## 技术栈

- Python 3.8+
- Flask 2.0+
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (数据库迁移)
- Flask-CORS (跨域支持)
- MySQL (数据库)

## 目录结构
- src/
- ├── app.py # 应用入口
- ├── config.py # 配置文件
- ├── exts.py # 扩展初始化
- ├── models.py # 数据模型
- └── controller/
- ................└── user.py # 用户相关控制器
