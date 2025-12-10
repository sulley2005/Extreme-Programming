"""
代码版本验证工具
用于检查服务器上的代码是否是最新版本

运行：python verify_code.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("检查后端代码版本")
print("=" * 60)

# 1. 检查 models.py
print("\n检查 models.py:")
try:
    from models import User, UserVersion
    
    # 检查User模型是否有operator字段
    user_columns = [c.name for c in User.__table__.columns]
    print(f"User表字段: {', '.join(user_columns)}")
    
    required = ['address', 'social_media', 'notes', 'is_favorite', 'operator']
    missing = [f for f in required if f not in user_columns]
    
    if missing:
        print(f"❌ User模型缺少字段: {', '.join(missing)}")
        print("   → models.py 未更新！")
    else:
        print("✅ User模型包含所有新字段")
    
    # 检查UserVersion
    version_columns = [c.name for c in UserVersion.__table__.columns]
    v_missing = [f for f in required if f not in version_columns]
    
    if v_missing:
        print(f"❌ UserVersion模型缺少字段: {', '.join(v_missing)}")
    else:
        print("✅ UserVersion模型包含所有新字段")
        
except Exception as e:
    print(f"❌ 无法加载models.py: {str(e)}")

# 2. 检查 controller/user.py
print("\n检查 controller/user.py:")
try:
    from controller.user import bp
    
    # 获取所有路由
    routes = []
    for rule in bp.url_map.iter_rules():
        if rule.endpoint.startswith('user.'):
            routes.append(rule.rule)
    
    print(f"已注册的路由: {len(routes)}个")
    
    # 检查toggle-favorite路由
    toggle_route = '/toggle-favorite/<int:user_id>'
    has_toggle = any(toggle_route in r for r in routes)
    
    if has_toggle:
        print("✅ toggle-favorite 路由已注册")
    else:
        print("❌ toggle-favorite 路由未找到")
        print("   → controller/user.py 未更新！")
    
    # 尝试读取源代码检查operator参数
    controller_path = os.path.join(os.path.dirname(__file__), 'src', 'controller', 'user.py')
    with open(controller_path, 'r', encoding='utf-8') as f:
        code = f.read()
        
    if 'operator' in code and "data.get('operator'" in code:
        print("✅ controller/user.py 包含operator处理逻辑")
    else:
        print("❌ controller/user.py 缺少operator处理")
        print("   → controller/user.py 未更新！")
        
    # 检查是否总是记录版本
    if '# 总是记录版本' in code or '总是记录版本' in code:
        print("✅ edit_user 已改为总是记录版本")
    else:
        print("⚠️  edit_user 可能仍在检查变化才记录版本")
        
except Exception as e:
    print(f"❌ 无法检查controller/user.py: {str(e)}")

# 3. 检查Flask应用是否运行
print("\n检查Flask应用状态:")
try:
    from app import app
    print(f"✅ Flask应用已加载")
    print(f"   Debug模式: {app.debug}")
    print(f"   配置: {app.config.get('ENV', 'unknown')}")
except Exception as e:
    print(f"❌ 无法加载Flask应用: {str(e)}")

print("\n" + "=" * 60)
print("建议操作")
print("=" * 60)

print("""
如果看到任何❌标记，说明代码未正确更新，请：

1. 确认已上传最新的文件：
   - src/models.py
   - src/controller/user.py
   
2. 重启Flask应用：
   ps aux | grep gunicorn
   kill -9 <PID>
   cd src
   nohup gunicorn -c gunicorn_conf.py app:app > /dev/null 2>&1 &

3. 验证进程已启动：
   ps aux | grep gunicorn
   
4. 清除浏览器缓存（Ctrl+Shift+Delete）

5. 使用无痕模式测试（Ctrl+Shift+N）
""")
