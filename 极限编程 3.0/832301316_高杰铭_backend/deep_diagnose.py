"""
数据库深度诊断与自动修复工具
用于解决：
1. 收藏失败
2. 新字段(地址/备注/操作人等)无法保存
3. 数据库表结构不一致

使用方法：
1. 上传到 backend 目录
2. 运行：python deep_diagnose.py
"""
import sys
import os
import pymysql
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from app import app, db
from sqlalchemy import text
import traceback

def diagnose():
    print("=" * 60)
    print("开始数据库深度诊断")
    print("=" * 60)
    
    with app.app_context():
        # 1. 检查连接
        try:
            db.session.execute(text("SELECT 1"))
            print("✅ 数据库连接正常")
        except Exception as e:
            print(f"❌ 数据库连接失败: {str(e)}")
            return

        # 2. 检查User表字段
        print("\n检查 user 表字段结构:")
        try:
            # 获取表结构
            result = db.session.execute(text("DESCRIBE user"))
            columns = {row[0]: row for row in result}
            
            required_fields = {
                'address': 'varchar(200)',
                'social_media': 'varchar(200)',
                'notes': 'text',
                'is_favorite': 'tinyint(1)',
                'operator': 'varchar(50)'
            }
            
            missing_fields = []
            
            for field, type_hint in required_fields.items():
                if field in columns:
                    print(f"  ✓ {field:<15} [存在]")
                else:
                    print(f"  ❌ {field:<15} [缺失]")
                    missing_fields.append(field)
            
            # 3. 尝试自动修复缺失字段
            if missing_fields:
                print("\n⚠️ 发现缺失字段，正在尝试自动修复...")
                try:
                    if 'address' in missing_fields:
                        db.session.execute(text("ALTER TABLE user ADD COLUMN address VARCHAR(200)"))
                    if 'social_media' in missing_fields:
                        db.session.execute(text("ALTER TABLE user ADD COLUMN social_media VARCHAR(200)"))
                    if 'notes' in missing_fields:
                        db.session.execute(text("ALTER TABLE user ADD COLUMN notes TEXT"))
                    if 'is_favorite' in missing_fields:
                        db.session.execute(text("ALTER TABLE user ADD COLUMN is_favorite BOOLEAN DEFAULT 0"))
                    if 'operator' in missing_fields:
                        db.session.execute(text("ALTER TABLE user ADD COLUMN operator VARCHAR(50) DEFAULT 'system'"))
                    
                    db.session.commit()
                    print("✅ 自动修复成功！所有字段已添加。")
                except Exception as e:
                    db.session.rollback()
                    print(f"❌ 自动修复失败: {str(e)}")
            
            # 4. 检查UserVersion表字段
            print("\n检查 user_version 表字段结构:")
            try:
                result = db.session.execute(text("DESCRIBE user_version"))
                v_columns = {row[0]: row for row in result}
                
                v_missing = []
                for field in required_fields:
                    if field in v_columns:
                        print(f"  ✓ {field:<15} [存在]")
                    else:
                        print(f"  ❌ {field:<15} [缺失]")
                        v_missing.append(field)
                
                if v_missing:
                    print("\n⚠️ user_version 表缺失字段，正在修复...")
                    try:
                        if 'address' in v_missing:
                            db.session.execute(text("ALTER TABLE user_version ADD COLUMN address VARCHAR(200)"))
                        if 'social_media' in v_missing:
                            db.session.execute(text("ALTER TABLE user_version ADD COLUMN social_media VARCHAR(200)"))
                        if 'notes' in v_missing:
                            db.session.execute(text("ALTER TABLE user_version ADD COLUMN notes TEXT"))
                        if 'is_favorite' in v_missing:
                            db.session.execute(text("ALTER TABLE user_version ADD COLUMN is_favorite BOOLEAN DEFAULT 0"))
                        if 'operator' in v_missing:
                            db.session.execute(text("ALTER TABLE user_version ADD COLUMN operator VARCHAR(50) DEFAULT 'system'"))
                        
                        db.session.commit()
                        print("✅ user_version 表修复成功！")
                    except Exception as e:
                        db.session.rollback()
                        print(f"❌ user_version 修复失败: {str(e)}")
                        
            except Exception as e:
                print(f"❌ 无法读取 user_version 表: {str(e)}")

        except Exception as e:
            print(f"❌ 检查表结构失败: {str(e)}")
            traceback.print_exc()

        # 5. 写入测试
        print("\n进行数据写入测试...")
        try:
            # 查找一个用户
            result = db.session.execute(text("SELECT id, username FROM user LIMIT 1"))
            user = result.fetchone()
            
            if user:
                user_id = user[0]
                username = user[1]
                print(f"正在尝试更新用户 ID={user_id} ({username})...")
                
                # 尝试更新 is_favorite 字段
                db.session.execute(text(f"UPDATE user SET is_favorite=0 WHERE id={user_id}")) # 重置
                db.session.commit()
                
                # 再次更新为 1
                db.session.execute(text(f"UPDATE user SET is_favorite=1 WHERE id={user_id}"))
                db.session.commit()
                
                # 读取验证
                check = db.session.execute(text(f"SELECT is_favorite FROM user WHERE id={user_id}")).fetchone()
                if check and check[0] == 1:
                    print(f"✅ 写入测试成功: is_favorite 字段可读写")
                else:
                    print(f"❌ 写入测试失败: 写入后读取的值不匹配")
            else:
                print("⚠️ 数据库中没有用户，跳过写入测试")
        
        except Exception as e:
            db.session.rollback()
            print(f"❌ 写入测试发生错误: {str(e)}")

    print("\n" + "=" * 60)
    print("诊断结束")
    print("=" * 60)

if __name__ == '__main__':
    diagnose()
