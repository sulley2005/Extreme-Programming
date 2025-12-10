let allUsers = []; // 存储所有用户数据用于搜索过滤

async function loadUsers() {
    try {
        const result = await apiRequest('/user/all', 'GET');
        allUsers = result.data;
        displayUsers(allUsers);
    } catch (error) {
        console.error('加载用户失败:', error);
        document.getElementById('user-table-body').innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-danger">加载失败,请刷新页面重试</td>
            </tr>
        `;
    }
}

function displayUsers(users) {
    const tableBody = document.getElementById('user-table-body');

    if (users.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center">
                    暂无用户数据,<a href="user-add.html" class="text-primary">去创建用户</a>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = users.map((user, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>
                <span class="star-icon ${user.is_favorite ? 'favorited' : ''}" 
                      onclick="toggleFavorite(${user.id}, event)"
                      title="${user.is_favorite ? '取消收藏' : '收藏'}">
                    ${user.is_favorite ? '★' : '☆'}
                </span>
            </td>
            <td>${user.username}</td>
            <td>${user.phone || '未填写'}</td>
            <td>${user.email || '未填写'}</td>
            <td>${user.create_time.split(' ')[0]}</td>
            <td>${user.update_time}</td>
            <td>
                <a href="user-detail.html?id=${user.id}" class="btn btn-sm btn-info btn-margin">详情</a>
                <a href="user-edit.html?id=${user.id}" class="btn btn-sm btn-warning btn-margin">编辑</a>
                <a href="user-versions.html?id=${user.id}" class="btn btn-sm btn-secondary btn-margin">版本</a>
                <button class="btn btn-sm btn-danger" onclick="deleteUser(${user.id}, '${user.username}')">删除</button>
            </td>
        </tr>
    `).join('');
}

async function toggleFavorite(userId, event) {
    event.preventDefault();
    event.stopPropagation();

    try {
        const result = await apiRequest(`/user/toggle-favorite/${userId}`, 'POST');
        showAlert(result.message, 'success');
        loadUsers(); // 重新加载用户列表
    } catch (error) {
        console.error('切换收藏状态失败:', error);
    }
}

async function deleteUser(userId, username) {
    if (!confirm(`确定要删除用户「${username}」吗？`)) {
        return;
    }

    try {
        const result = await apiRequest(`/user/delete/${userId}`, 'DELETE');
        showAlert(result.message, 'success');
        loadUsers();
    } catch (error) {
        console.error('删除用户失败:', error);
    }
}

// 搜索功能
function searchUsers() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();

    if (!searchTerm) {
        displayUsers(allUsers);
        return;
    }

    const filteredUsers = allUsers.filter(user => {
        return (
            user.username.toLowerCase().includes(searchTerm) ||
            (user.phone && user.phone.toLowerCase().includes(searchTerm)) ||
            (user.email && user.email.toLowerCase().includes(searchTerm)) ||
            (user.address && user.address.toLowerCase().includes(searchTerm)) ||
            (user.social_media && user.social_media.toLowerCase().includes(searchTerm)) ||
            (user.notes && user.notes.toLowerCase().includes(searchTerm))
        );
    });

    displayUsers(filteredUsers);
}

// 导出Excel功能
function exportToExcel() {
    if (allUsers.length === 0) {
        showAlert('没有数据可以导出', 'warning');
        return;
    }

    // 准备导出数据
    const exportData = allUsers.map((user, index) => ({
        'ID': index + 1,
        '姓名': user.username,
        '电话': user.phone || '',
        '邮箱': user.email || '',
        '地址': user.address || '',
        '社交媒体': user.social_media || '',
        '备注': user.notes || '',
        '收藏': user.is_favorite ? '是' : '否',
        '创建时间': user.create_time,
        '最后更新': user.update_time
    }));

    // 创建工作簿
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(exportData);

    // 设置列宽
    ws['!cols'] = [
        { wch: 5 },  // ID
        { wch: 15 }, // 姓名
        { wch: 15 }, // 电话
        { wch: 25 }, // 邮箱
        { wch: 30 }, // 地址
        { wch: 20 }, // 社交媒体
        { wch: 30 }, // 备注
        { wch: 8 },  // 收藏
        { wch: 20 }, // 创建时间
        { wch: 20 }  // 最后更新
    ];

    XLSX.utils.book_append_sheet(wb, ws, '联系人列表');

    // 生成文件名
    const filename = `联系人列表_${new Date().toISOString().split('T')[0]}.xlsx`;

    // 下载文件
    XLSX.writeFile(wb, filename);
    showAlert('导出成功！', 'success');
}

// 导入Excel功能
function importFromExcel(file) {
    const reader = new FileReader();

    reader.onload = async function (e) {
        try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });

            // 读取第一个工作表
            const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
            const jsonData = XLSX.utils.sheet_to_json(firstSheet);

            if (jsonData.length === 0) {
                showAlert('Excel文件中没有数据', 'warning');
                return;
            }

            let successCount = 0;
            let failCount = 0;

            // 逐个创建用户
            for (const row of jsonData) {
                try {
                    const userData = {
                        username: row['姓名'] || row['用户名'] || '',
                        phone: row['电话'] || '',
                        email: row['邮箱'] || '',
                        address: row['地址'] || '',
                        social_media: row['社交媒体'] || '',
                        notes: row['备注'] || '',
                        is_favorite: row['收藏'] === '是' || row['收藏'] === true
                    };

                    if (!userData.username) {
                        failCount++;
                        continue;
                    }

                    await apiRequest('/user/create', 'POST', userData);
                    successCount++;
                } catch (error) {
                    failCount++;
                    console.error('导入用户失败:', error);
                }
            }

            showAlert(`导入完成！成功: ${successCount}, 失败: ${failCount}`, 'info');
            loadUsers(); // 重新加载用户列表

        } catch (error) {
            console.error('读取Excel文件失败:', error);
            showAlert('读取Excel文件失败，请确保文件格式正确', 'danger');
        }
    };

    reader.readAsArrayBuffer(file);
}

// 事件监听器
document.addEventListener('DOMContentLoaded', function () {
    loadUsers();

    // 搜索输入事件
    document.getElementById('search-input').addEventListener('input', searchUsers);

    // 清空搜索按钮
    document.getElementById('clear-search-btn').addEventListener('click', function () {
        document.getElementById('search-input').value = '';
        displayUsers(allUsers);
    });

    // 导出Excel按钮
    document.getElementById('export-excel-btn').addEventListener('click', exportToExcel);

    // 导入Excel按钮
    document.getElementById('import-excel-btn').addEventListener('click', function () {
        document.getElementById('import-file-input').click();
    });

    // 文件选择事件
    document.getElementById('import-file-input').addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            importFromExcel(file);
            // 清空文件选择，允许重复导入同一文件
            e.target.value = '';
        }
    });
});