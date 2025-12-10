from exts import db
from datetime import datetime

# 用户主表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(200))  # 新增：地址（可选）
    social_media = db.Column(db.String(200))  # 新增：社交媒体账号（可选）
    notes = db.Column(db.Text)  # 新增：备注（可选）
    is_favorite = db.Column(db.Boolean, default=False)  # 新增：是否收藏
    operator = db.Column(db.String(50), default="system")  # 新增：操作人
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    versions = db.relationship('UserVersion', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'social_media': self.social_media,
            'notes': self.notes,
            'is_favorite': self.is_favorite,
            'operator': self.operator,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

# 用户版本记录表
class UserVersion(db.Model):
    __tablename__ = "user_version"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))  # 新增：地址
    social_media = db.Column(db.String(200))  # 新增：社交媒体账号
    notes = db.Column(db.Text)  # 新增：备注
    is_favorite = db.Column(db.Boolean, default=False)  # 新增：是否收藏
    update_time = db.Column(db.DateTime, default=datetime.now)
    operator = db.Column(db.String(50), default="system")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'social_media': self.social_media,
            'notes': self.notes,
            'is_favorite': self.is_favorite,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'operator': self.operator
        }
