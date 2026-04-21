/**
 * filter.js
 * 負責前端即時切換任務清單的顯示狀態 (全部 / 待完成 / 已完成)
 * 增加平滑的過渡動畫 (Fade In/Out)
 */
document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const taskItems = document.querySelectorAll('.task-item');
    const emptyStateInfo = document.getElementById('emptySearchState');
    
    // 初始化動畫加上 class
    taskItems.forEach(item => {
        item.classList.add('fade-in-up');
    });

    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // 移除其他按鈕的 active 狀態
            filterBtns.forEach(b => b.classList.remove('active'));
            // 加上當下點擊的 active 狀態
            const selectedBtn = e.currentTarget;
            selectedBtn.classList.add('active');

            const filterValue = selectedBtn.getAttribute('data-filter'); // "all", "false", "true"
            let visibleCount = 0;

            taskItems.forEach(item => {
                const isDone = item.getAttribute('data-done'); // "true" or "false"
                
                // 為了重新觸發進場動畫，我們暫存並重建 class
                item.style.animation = 'none';
                void item.offsetWidth; // trigger reflow
                
                if (filterValue === 'all' || filterValue === isDone) {
                    item.classList.remove('d-none');
                    item.style.animation = 'fadeInUp 0.3s ease-out forwards';
                    visibleCount++;
                } else {
                    item.classList.add('d-none');
                }
            });
            
            // 是否要在前端顯示「篩選無資料」的提示
            if (emptyStateInfo) {
                if (visibleCount === 0 && taskItems.length > 0) {
                    emptyStateInfo.classList.remove('d-none');
                    emptyStateInfo.style.animation = 'fadeInUp 0.3s ease-out forwards';
                } else {
                    emptyStateInfo.classList.add('d-none');
                }
            }
        });
    });
});
