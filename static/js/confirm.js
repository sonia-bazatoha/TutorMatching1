document.addEventListener('DOMContentLoaded', function () {

    // Create modal HTML
    const modal = document.createElement('div');
    modal.id = 'confirm-modal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.5);
        z-index: 9999;
        align-items: center;
        justify-content: center;
    `;

    modal.innerHTML = `
        <div style="
            background: #fff;
            border-radius: 12px;
            padding: 32px;
            max-width: 380px;
            width: 90%;
            box-shadow: 0 20px 48px rgba(0,31,84,.18);
            text-align: center;
        ">
            <p id="confirm-message" style="
                font-size: 1rem;
                font-weight: 600;
                color: #001f54;
                margin-bottom: 24px;
                line-height: 1.5;
            "></p>
            <div style="display:flex; gap:12px; justify-content:center;">
                <button id="confirm-cancel" style="
                    padding: 10px 24px;
                    border-radius: 6px;
                    border: 2px solid #001f54;
                    background: transparent;
                    color: #001f54;
                    font-weight: 700;
                    cursor: pointer;
                    font-size: .95rem;
                ">Cancel</button>
                <button id="confirm-ok" style="
                    padding: 10px 24px;
                    border-radius: 6px;
                    border: 2px solid #001f54;
                    background: #001f54;
                    color: #fff;
                    font-weight: 700;
                    cursor: pointer;
                    font-size: .95rem;
                ">Confirm</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    const message = document.getElementById('confirm-message');
    const cancelBtn = document.getElementById('confirm-cancel');
    const okBtn = document.getElementById('confirm-ok');

    let pendingHref = null;

    // Intercept all data-confirm links
    document.querySelectorAll('[data-confirm]').forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            pendingHref = link.getAttribute('href');
            message.textContent = link.getAttribute('data-confirm');
            modal.style.display = 'flex';
        });
    });

    // Cancel
    cancelBtn.addEventListener('click', function () {
        modal.style.display = 'none';
        pendingHref = null;
    });

    // Confirm
    okBtn.addEventListener('click', function () {
        if (pendingHref) {
            window.location.href = pendingHref;
        }
    });

    // Click outside to close
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            pendingHref = null;
        }
    });

});