document.addEventListener('DOMContentLoaded', function () {
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach(function (toast) {
        const message = toast.getAttribute('data-message');
        toast.textContent = message;
        toast.classList.add('toast-show');

        setTimeout(function () {
            toast.classList.remove('toast-show');
            toast.classList.add('toast-hide');
            setTimeout(function () {
                toast.remove();
            }, 400);
        }, 4000);
    });
});