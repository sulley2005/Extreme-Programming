const userId = getUrlParam('id');

async function loadVersions() {
    if (!userId) {
        showAlert('用户ID不存在', 'danger');
        return;
    }

    document.getElementById('detail-btn').href = `user-detail.html?id=${userId}`;

    try {
        const result = await apiRequest(`/user/versions/${userId}`, 'GET');
        const versions = result.data;
        const tableBody = document.getElementById('versions-table-body');
        const versionCount = document.getElementById('version-count');

        versionCount.textContent = `共 ${versions.length} 次修改记录（含初始创建）`;

        if (versions.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="10" class="text-center">暂无版本记录</td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = versions.map((version, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${version.username}</td>
                <td>${version.phone || '未填写'}</td>
                <td>${version.email || '未填写'}</td>
                <td>${version.address || '未填写'}</td>
                <td>${version.social_media || '未填写'}</td>
                <td>${version.notes || '未填写'}</td>
                <td>${version.update_time}</td>
                <td>${version.operator}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="deleteVersion(${version.id})">删除</button>
                </td>
            </tr>
        `).join('');

    } catch (error) {
        console.error('加载版本历史失败:', error);
        document.getElementById('versions-table-body').innerHTML = `
            <tr>
                <td colspan="10" class="text-center text-danger">加载失败，请刷新页面重试</td>
            </tr>
        `;
    }
}

// 删除版本记录
async function deleteVersion(versionId) {
    if (!confirm('确定要删除这条版本记录吗？此操作不可恢复！')) {
        return;
    }

    try {
        const result = await apiRequest(`/user/versions/delete/${versionId}`, 'DELETE');
        showAlert(result.message, 'success');
        // 重新加载版本列表
        loadVersions();
    } catch (error) {
        console.error('删除版本失败:', error);
        showAlert('删除版本失败，请重试', 'danger');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!userId) {
        showAlert('缺少用户ID参数', 'danger');
        return;
    }

    loadVersions();
});