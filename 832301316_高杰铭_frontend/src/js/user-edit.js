const userId = getUrlParam('id');

async function loadUserInfo() {
    if (!userId) {
        showAlert('用户ID不存在', 'danger');
        return;
    }

    try {
        const result = await apiRequest(`/user/${userId}`, 'GET');
        const user = result.data;

        document.getElementById('username').value = user.username;
        document.getElementById('phone').value = user.phone || '';
        document.getElementById('email').value = user.email || '';
        document.getElementById('address').value = user.address || '';
        document.getElementById('social_media').value = user.social_media || '';
        document.getElementById('notes').value = user.notes || '';
        document.getElementById('operator').value = user.operator || 'system';
        document.getElementById('is_favorite').checked = user.is_favorite || false;

        const detailUrl = `user-detail.html?id=${userId}`;
        document.getElementById('detail-btn').href = detailUrl;
        document.getElementById('cancel-btn').href = detailUrl;

    } catch (error) {
        console.error('加载用户信息失败:', error);
    }
}

async function submitEditForm(e) {
    e.preventDefault();

    const formData = {
        username: document.getElementById('username').value.trim(),
        phone: document.getElementById('phone').value.trim() || null,
        email: document.getElementById('email').value.trim() || null,
        address: document.getElementById('address').value.trim() || null,
        social_media: document.getElementById('social_media').value.trim() || null,
        notes: document.getElementById('notes').value.trim() || null,
        operator: document.getElementById('operator').value.trim() || 'system',
        is_favorite: document.getElementById('is_favorite').checked
    };

    try {
        const result = await apiRequest(`/user/edit/${userId}`, 'PUT', formData);
        showAlert(result.message, 'success');

        setTimeout(() => {
            window.location.href = `user-detail.html?id=${userId}`;
        }, 2000);
    } catch (error) {
        console.error('更新用户失败:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!userId) {
        showAlert('缺少用户ID参数', 'danger');
        return;
    }

    loadUserInfo();
    document.getElementById('edit-user-form').addEventListener('submit', submitEditForm);
});