# 前端启动命令！！！
- cd 832301316_高杰铭_frontend
- python -m http.server 8000 --bind 127.0.0.1 --directory src

# 地址簿管理系统 - 前端

这是一个简单的地址簿管理系统前端页面，用于管理联系人信息。

## 功能

- 创建新用户
- 查看用户列表
- 查看用户详情
- 编辑用户信息
- 删除用户
- 查看用户修改历史版本

## 技术栈

- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Fetch API

## 目录结构

- src/
- ├── index.html # 创建用户页面
- ├── user-list.html # 用户列表页面
- ├── user-detail.html # 用户详情页面
- ├── user-edit.html # 编辑用户页面
- ├── user-versions.html # 版本历史页面
- ├── css/
- │........ └── custom.css # 自定义样式
- └── js/
- ........├── api.js # API 请求封装
- ........├── index.js # 创建用户页面脚本
- ........├── user-list.js # 用户列表页面脚本
- ........├── user-detail.js # 用户详情页面脚本
- ........├── user-edit.js # 编辑用户页面脚本
- ........└── user-versions.js # 版本历史页面脚本