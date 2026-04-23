// ===== CART =====
document.addEventListener('DOMContentLoaded', function () {

    // Кнопки "В корзину"
    document.querySelectorAll('.prod-card__add').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const original = btn.textContent;
            btn.textContent = '✓ Добавлено';
            btn.style.background = '#eaf3de';
            setTimeout(function () {
                btn.textContent = original;
                btn.style.background = '';
            }, 1500);
        });
    });

    // Фильтры
    document.querySelectorAll('.filter-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.filter-btn').forEach(function (b) {
                b.classList.remove('active');
            });
            btn.classList.add('active');
        });
    });

    // Автоскрытие сообщений Django
    document.querySelectorAll('.message').forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.4s';
            msg.style.opacity = '0';
            setTimeout(function () { msg.remove(); }, 400);
        }, 3500);
    });

});