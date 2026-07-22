document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('nav-links');

    if (!hamburger || !navLinks) return;

    hamburger.addEventListener('click', function () {
        navLinks.classList.toggle('nav-open');
        hamburger.classList.toggle('hamburger-active');
    });

    navLinks.querySelectorAll('.nav-link').forEach(function (link) {
        link.addEventListener('click', function () {
            navLinks.classList.remove('nav-open');
            hamburger.classList.remove('hamburger-active');
        });
    });
});