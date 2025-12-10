const userId = getUrlParam('id');

async function loadUserDetail() {
    if (!userId) {
        showAlert('用户ID不存在', 'danger');
        return;
    }

    try {
        const result = await apiRequest(`/user/${userId}`, 'GET');
        const user = result.data;

        document.getElementById('user-id').textContent = user.id;
        document.getElementById('user-username').textContent = user.username;
        document.getElementById('user-phone').textContent = user.phone || '未填写';
        document.getElementById('user-email').textContent = user.email || '未填写';
        document.getElementById('user-address').textContent = user.address || '未填写';
        document.getElementById('user-social-media').textContent = user.social_media || '未填写';
        document.getElementById('user-notes').textContent = user.notes || '未填写';
        document.getElementById('user-favorite').innerHTML = user.is_favorite ?
            '<span class="star-icon favorited">★</span> 已收藏' :
            '<span class="star-icon">☆</span> 未收藏';
        document.getElementById('user-create-time').textContent = user.create_time;
        document.getElementById('user-update-time').textContent = user.update_time;

        document.getElementById('edit-btn').href = `user-edit.html?id=${userId}`;
        document.getElementById('versions-btn').href = `user-versions.html?id=${userId}`;

    } catch (error) {
        console.error('加载用户详情失败:', error);
    }
}

async function deleteUser() {
    if (!confirm('确定要删除该用户吗？')) {
        return;
    }

    try {
        const result = await apiRequest(`/user/delete/${userId}`, 'DELETE');
        showAlert(result.message, 'success');

        setTimeout(() => {
            window.location.href = 'user-list.html';
        }, 2000);
    } catch (error) {
        console.error('删除用户失败:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!userId) {
        showAlert('缺少用户ID参数', 'danger');
        return;
    }

    loadUserDetail();
    document.getElementById('delete-btn').addEventListener('click', deleteUser);
});