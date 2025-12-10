// 显示提示信息（使用api.js中统一的showAlert方法，保持一致性）
// 移除重复的showAlert定义，避免冲突

// 创建用户表单提交
document.getElementById('create-user-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    // 获取表单数据
    const username = document.getElementById('username').value.trim();
    const phone = document.getElementById('phone').value.trim() || null;
    const email = document.getElementById('email').value.trim() || null;
    const address = document.getElementById('address').value.trim() || null;
    const social_media = document.getElementById('social_media').value.trim() || null;
    const notes = document.getElementById('notes').value.trim() || null;
    const is_favorite = document.getElementById('is_favorite').checked;

    // 客户端简单验证
    if (!username) {
        showAlert('用户名不能为空', 'danger');
        return;
    }

    const formData = { username, phone, email, address, social_media, notes, is_favorite };

    try {
        // 发送创建用户请求
        const result = await apiRequest('/user/create', 'POST', formData);

        // 显示成功提示
        showAlert(result.message, 'success');

        // 2秒后跳转到用户列表
        setTimeout(() => {
            window.location.href = 'user-list.html';
        }, 2000);
    } catch (error) {
        console.error('创建用户失败:', error);
        // 显示错误提示（api.js中已处理基础错误提示，这里可补充特定处理）
    }
});