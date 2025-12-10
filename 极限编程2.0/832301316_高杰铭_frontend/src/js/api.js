// API基础地址（后端服务地址）
const API_BASE_URL = 'http://8.138.190.252:5000/api';

// 封装fetch请求
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        mode: 'cors'  // 允许跨域请求
    };

    // 如果有数据，添加到请求体
    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${url}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || `请求失败: ${response.status}`);
        }

        return result;
    } catch (error) {
        showAlert(error.message, 'danger');
        throw error;
    }
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    // 添加动画效果
    alertDiv.style.opacity = '0';
    alertDiv.style.transform = 'translateY(-10px)';
    alertDiv.style.transition = 'opacity 0.3s ease, transform 0.3s ease';

    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.appendChild(alertDiv);
        // 触发动画
        setTimeout(() => {
            alertDiv.style.opacity = '1';
            alertDiv.style.transform = 'translateY(0)';
        }, 10);

        // 3秒后自动关闭（带动画）
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            alertDiv.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }, 300);
        }, 3000);
    }
}

// 获取URL参数
function getUrlParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

// 获取路径参数
function getPathParam(index) {
    const path = window.location.pathname.split('/');
    return path[index] || null;
}