document.addEventListener('DOMContentLoaded', function () {

    let overlay = document.getElementById('avatar-lightbox-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'avatar-lightbox-overlay';
        overlay.className = 'avatar-lightbox-overlay';
        overlay.innerHTML =
            '<button type="button" class="avatar-lightbox-close" aria-label="Close">&times;</button>' +
            '<img src="" alt="Profile picture">';
        document.body.appendChild(overlay);
    }

    const overlayImg = overlay.querySelector('img');
    const closeBtn = overlay.querySelector('.avatar-lightbox-close');

    function openLightbox(src, alt) {
        overlayImg.src = src;
        overlayImg.alt = alt || 'Profile picture';
        overlay.classList.add('active');
    }

    function closeLightbox() {
        overlay.classList.remove('active');
        overlayImg.src = '';
    }

    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeLightbox();
    });

    closeBtn.addEventListener('click', closeLightbox);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeLightbox();
    });

    // Event delegation: works for images already on the page AND
    // ones injected later (e.g. AJAX-refreshed tutor cards).
    document.addEventListener('click', function (e) {
        const img = e.target.closest('.clickable-avatar');
        if (img && img.tagName === 'IMG') {
            openLightbox(img.src, img.alt);
        }
    });
});
