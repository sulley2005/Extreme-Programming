class Config:
    # 数据库配置
    HOSTNAME = "127.0.0.1"
    PORT = 3306
    USERNAME = "gaodashuai"
    PASSWORD = "Gaojieming123."  # 你的数据库密码
    DATABASE = "database_address_book"  # 数据库名称（确保已创建）

    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4&collation=utf8mb4_general_ci"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭追踪修改
    SQLALCHEMY_ECHO = False  # 关闭SQL语句打印（减少日志干扰）

    # Flask配置
    DEBUG = True  # 开发模式
    SECRET_KEY = "123456"  # 会话密钥（生产环境需修改）