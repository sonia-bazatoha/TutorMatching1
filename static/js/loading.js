document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function () {
            const btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.textContent = 'Please wait…';
                btn.style.opacity = '0.7';
                btn.style.cursor = 'not-allowed';
            }
        });
    });

});