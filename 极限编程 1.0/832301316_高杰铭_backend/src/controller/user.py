from flask import Blueprint, request, jsonify
from exts import db
from models import User, UserVersion
from datetime import datetime
import traceback

bp = Blueprint('user', __name__, url_prefix='/api/user')

# 创建用户
@bp.route('/create', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        phone = data.get('phone', '').strip() or None
        email = data.get('email', '').strip() or None
        address = data.get('address', '').strip() or None
        social_media = data.get('social_media', '').strip() or None
        notes = data.get('notes', '').strip() or None
        is_favorite = data.get('is_favorite', False)

        if not username:
            return jsonify({'code': 400, 'message': '用户名不能为空！'})

        if User.query.filter_by(username=username).first():
            return jsonify({'code': 400, 'message': f'用户名「{username}」已存在！'})

        if email and User.query.filter_by(email=email).first():
            return jsonify({'code': 400, 'message': f'邮箱「{email}」已被使用！'})

        new_user = User(
            username=username,
            phone=phone,
            email=email,
            address=address,
            social_media=social_media,
            notes=notes,
            is_favorite=is_favorite
        )
        db.session.add(new_user)
        db.session.flush()

        initial_version = UserVersion(
            user_id=new_user.id,
            username=username,
            phone=phone,
            email=email,
            address=address,
            social_media=social_media,
            notes=notes,
            is_favorite=is_favorite
        )
        db.session.add(initial_version)
        db.session.commit()

        return jsonify({
            'code': 200,
            'message': f'用户「{username}」创建成功',
            'data': new_user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'code': 500, 'message': f'创建失败：{str(e)}'})

# 获取所有用户（收藏的排在前面）
@bp.route('/all', methods=['GET'])
def get_all_users():
    users = User.query.order_by(User.is_favorite.desc(), User.create_time.desc()).all()
    return jsonify({
        'code': 200,
        'data': [user.to_dict() for user in users]
    })

# 获取单个用户
@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'code': 200,
        'data': user.to_dict()
    })

# 更新用户
@bp.route('/edit/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        data = request.get_json()
        new_username = data.get('username', '').strip()
        new_phone = data.get('phone', '').strip() or None
        new_email = data.get('email', '').strip() or None
        new_address = data.get('address', '').strip() or None
        new_social_media = data.get('social_media', '').strip() or None
        new_notes = data.get('notes', '').strip() or None
        new_is_favorite = data.get('is_favorite', False)

        if not new_username:
            return jsonify({'code': 400, 'message': '用户名不能为空！'})

        if User.query.filter(User.username == new_username, User.id != user_id).first():
            return jsonify({'code': 400, 'message': f'用户名「{new_username}」已被使用！'})

        if new_email and User.query.filter(User.email == new_email, User.id != user_id).first():
            return jsonify({'code': 400, 'message': f'邮箱「{new_email}」已被使用！'})

        old_username = user.username
        old_phone = user.phone
        old_email = user.email
        old_address = user.address
        old_social_media = user.social_media
        old_notes = user.notes
        old_is_favorite = user.is_favorite

        user.username = new_username
        user.phone = new_phone
        user.email = new_email
        user.address = new_address
        user.social_media = new_social_media
        user.notes = new_notes
        user.is_favorite = new_is_favorite
        user.update_time = datetime.now()

        if (old_username != new_username) or (old_phone != new_phone) or (old_email != new_email) or \
           (old_address != new_address) or (old_social_media != new_social_media) or \
           (old_notes != new_notes) or (old_is_favorite != new_is_favorite):
            new_version = UserVersion(
                user_id=user.id,
                username=new_username,
                phone=new_phone,
                email=new_email,
                address=new_address,
                social_media=new_social_media,
                notes=new_notes,
                is_favorite=new_is_favorite
            )
            db.session.add(new_version)

        db.session.commit()
        return jsonify({
            'code': 200,
            'message': f'用户「{new_username}」更新成功！',
            'data': user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'code': 500, 'message': f'更新失败：{str(e)}'})

# 删除用户
@bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': f'用户「{user.username}」已成功删除！'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'删除失败：{str(e)}'})

# 获取版本历史
@bp.route('/versions/<int:user_id>', methods=['GET'])
def user_versions(user_id):
    User.query.get_or_404(user_id)  # 验证用户存在
    versions = UserVersion.query.filter_by(user_id=user_id).order_by(UserVersion.update_time.desc()).all()
    return jsonify({
        'code': 200,
        'data': [version.to_dict() for version in versions]
    })

# 切换收藏状态
@bp.route('/toggle-favorite/<int:user_id>', methods=['POST'])
def toggle_favorite(user_id):
    user = User.query.get_or_404(user_id)
    try:
        user.is_favorite = not user.is_favorite
        user.update_time = datetime.now()
        
        # 记录版本
        new_version = UserVersion(
            user_id=user.id,
            username=user.username,
            phone=user.phone,
            email=user.email,
            address=user.address,
            social_media=user.social_media,
            notes=user.notes,
            is_favorite=user.is_favorite
        )
        db.session.add(new_version)
        db.session.commit()
        
        status = '已收藏' if user.is_favorite else '已取消收藏'
        return jsonify({
            'code': 200,
            'message': f'用户「{user.username}」{status}！',
            'data': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'操作失败：{str(e)}'})