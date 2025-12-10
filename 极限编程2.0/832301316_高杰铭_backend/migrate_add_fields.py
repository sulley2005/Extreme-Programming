"""
数据库迁移脚本 - 添加新字段
执行此脚本以添加 address, social_media, notes, is_favorite 字段到数据库

使用方法:
1. 确保已经停止了Flask应用
2. 在backend目录下运行: python migrate_add_fields.py
3. 重新启动Flask应用
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app, db
from sqlalchemy import text

def migrate_database():
    """执行数据库迁移"""
    with app.app_context():
        try:
            print("开始数据库迁移...")
            
            # 检查并添加 address 字段
            try:
                db.session.execute(text("SELECT address FROM user LIMIT 1"))
                print("✓ address 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user ADD COLUMN address VARCHAR(200)"))
                db.session.commit()
                print("✓ 添加 address 字段成功")
            
            # 检查并添加 social_media 字段
            try:
                db.session.execute(text("SELECT social_media FROM user LIMIT 1"))
                print("✓ social_media 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user ADD COLUMN social_media VARCHAR(200)"))
                db.session.commit()
                print("✓ 添加 social_media 字段成功")
            
            # 检查并添加 notes 字段
            try:
                db.session.execute(text("SELECT notes FROM user LIMIT 1"))
                print("✓ notes 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user ADD COLUMN notes TEXT"))
                db.session.commit()
                print("✓ 添加 notes 字段成功")
            
            # 检查并添加 is_favorite 字段
            try:
                db.session.execute(text("SELECT is_favorite FROM user LIMIT 1"))
                print("✓ is_favorite 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user ADD COLUMN is_favorite BOOLEAN DEFAULT 0"))
                db.session.commit()
                print("✓ 添加 is_favorite 字段成功")
            
            # 为 user_version 表添加相同字段
            print("\n更新 user_version 表...")
            
            try:
                db.session.execute(text("SELECT address FROM user_version LIMIT 1"))
                print("✓ user_version.address 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user_version ADD COLUMN address VARCHAR(200)"))
                db.session.commit()
                print("✓ 添加 user_version.address 字段成功")
            
            try:
                db.session.execute(text("SELECT social_media FROM user_version LIMIT 1"))
                print("✓ user_version.social_media 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user_version ADD COLUMN social_media VARCHAR(200)"))
                db.session.commit()
                print("✓ 添加 user_version.social_media 字段成功")
            
            try:
                db.session.execute(text("SELECT notes FROM user_version LIMIT 1"))
                print("✓ user_version.notes 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user_version ADD COLUMN notes TEXT"))
                db.session.commit()
                print("✓ 添加 user_version.notes 字段成功")
            
            try:
                db.session.execute(text("SELECT is_favorite FROM user_version LIMIT 1"))
                print("✓ user_version.is_favorite 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user_version ADD COLUMN is_favorite BOOLEAN DEFAULT 0"))
                db.session.commit()
                print("✓ 添加 user_version.is_favorite 字段成功")
            
            print("\n✅ 数据库迁移完成！")
            print("现在可以重新启动Flask应用了。")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 迁移失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        return True

if __name__ == '__main__':
    success = migrate_database()
    sys.exit(0 if success else 1)
