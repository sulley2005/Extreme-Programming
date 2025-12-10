document.addEventListener('DOMContentLoaded', () => {
    const addCard = document.querySelector('.add-contact');
    const viewCard = document.querySelector('.view-contacts');

    // 基础位置参数
    let offset = 100; // 偏移量
    let hoverScale = 1.1; // 悬停缩放比例
    let normalScale = 1;  // 正常缩放比例

    // 响应式调整参数
    function adjustParameters() {
        if (window.innerWidth <= 768) {
            offset = 60;
            hoverScale = 1.05;
        } else {
            offset = 100;
            hoverScale = 1.1;
        }
        resetCards();
    }

    // 重置卡片到初始位置
    function resetCards() {
        // 添加联系人向左偏移
        addCard.style.transform = `translateX(-${offset}px) scale(${normalScale})`;
        addCard.style.zIndex = 1;

        // 查看联系人向右偏移
        viewCard.style.transform = `translateX(${offset}px) scale(${normalScale})`;
        viewCard.style.zIndex = 1;
    }

    // 当鼠标悬停在添加联系人卡片上
    addCard.addEventListener('mouseenter', () => {
        addCard.style.transform = `translateX(-${offset/1.2}px) scale(${hoverScale})`;
        addCard.style.zIndex = 10;
        viewCard.style.transform = `translateX(${offset*1.2}px) scale(${normalScale*0.95})`;
        viewCard.style.zIndex = 1;
    });

    // 当鼠标悬停在查看联系人卡片上
    viewCard.addEventListener('mouseenter', () => {
        viewCard.style.transform = `translateX(${offset/1.2}px) scale(${hoverScale})`;
        viewCard.style.zIndex = 10;
        addCard.style.transform = `translateX(-${offset*1.2}px) scale(${normalScale*0.95})`;
        addCard.style.zIndex = 1;
    });

    // 当鼠标离开卡片区域
    document.querySelector('.card-container').addEventListener('mouseleave', () => {
        resetCards();
    });

    // 窗口大小改变时重新调整
    window.addEventListener('resize', adjustParameters);

    // 初始化
    adjustParameters();
});