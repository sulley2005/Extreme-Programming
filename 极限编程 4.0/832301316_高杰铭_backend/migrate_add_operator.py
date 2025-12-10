"""
数据库迁移脚本 - 添加operator字段
执行此脚本以添加 operator 字段到user表

使用方法:
1. 确保已经停止了Flask应用
2. 在backend目录下运行: python migrate_add_operator.py
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
            
            # 检查并添加 operator 字段到user表
            try:
                db.session.execute(text("SELECT operator FROM user LIMIT 1"))
                print("✓ user.operator 字段已存在")
            except:
                db.session.rollback()
                db.session.execute(text("ALTER TABLE user ADD COLUMN operator VARCHAR(50) DEFAULT 'system'"))
                db.session.commit()
                print("✓ 添加 user.operator 字段成功")
            
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
