document.addEventListener('DOMContentLoaded', function () {

    const eyeOpen = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`;
    const eyeClosed = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>`;

    // ---- Password Toggle ----
    function addToggle(inputId) {
        const input = document.getElementById(inputId);
        if (!input) return;

        // Wrap only the input in a relative div
        const wrapper = document.createElement('div');
        wrapper.style.cssText = 'position: relative; display: block;';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        // Make sure input has right padding so text doesn't go under button
        input.style.paddingRight = '42px';

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.innerHTML = eyeOpen;
        btn.style.cssText = `
            position: absolute;
            right: 12px;
            top: 0;
            bottom: 0;
            margin: auto 0;
            height: 18px;
            background: none;
            border: none;
            cursor: pointer;
            padding: 0;
            color: #5a6a80;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        btn.addEventListener('click', function () {
            if (input.type === 'password') {
                input.type = 'text';
                btn.innerHTML = eyeClosed;
            } else {
                input.type = 'password';
                btn.innerHTML = eyeOpen;
            }
        });

        wrapper.appendChild(btn);
    }

    addToggle('id_password');
    addToggle('id_password1');
    addToggle('id_password2');

    // ---- Password Strength Meter ----
    const password1 = document.getElementById('id_password1');
    if (password1) {

        // Append strength bar AFTER the wrapper div, not inside it
        const formGroup = password1.closest('.form-group');

        const strengthWrap = document.createElement('div');
        strengthWrap.style.marginTop = '8px';

        const bar = document.createElement('div');
        bar.style.cssText = `
            height: 5px;
            border-radius: 4px;
            background: #e5e7eb;
            overflow: hidden;
            margin-bottom: 4px;
        `;

        const fill = document.createElement('div');
        fill.style.cssText = `
            height: 100%;
            width: 0%;
            border-radius: 4px;
            transition: width 0.3s ease, background-color 0.3s ease;
        `;

        const label = document.createElement('p');
        label.style.cssText = 'font-size: .8rem; color: #5a6a80; margin: 0;';

        bar.appendChild(fill);
        strengthWrap.appendChild(bar);
        strengthWrap.appendChild(label);

        // Append to form-group not to the wrapper
        if (formGroup) {
            formGroup.appendChild(strengthWrap);
        } else {
            password1.parentNode.parentNode.appendChild(strengthWrap);
        }

        password1.addEventListener('input', function () {
            const val = password1.value;
            let score = 0;

            if (val.length >= 8) score++;
            if (val.length >= 12) score++;
            if (/[A-Z]/.test(val)) score++;
            if (/[0-9]/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;

            const levels = [
                { label: '', color: '#e5e7eb', width: '0%' },
                { label: 'Very Weak', color: '#dc2626', width: '20%' },
                { label: 'Weak', color: '#f97316', width: '40%' },
                { label: 'Fair', color: '#eab308', width: '60%' },
                { label: 'Strong', color: '#22c55e', width: '80%' },
                { label: 'Very Strong', color: '#16a34a', width: '100%' },
            ];

            const level = val.length === 0 ? levels[0] : levels[Math.min(score, 5)];
            fill.style.width = level.width;
            fill.style.backgroundColor = level.color;
            label.textContent = level.label;
        });
    }

    // ---- Password Match Check ----
    const password2 = document.getElementById('id_password2');
    if (password1 && password2) {
        const formGroup = password2.closest('.form-group');

        const matchMsg = document.createElement('p');
        matchMsg.style.cssText = 'font-size: .8rem; margin-top: 4px;';

        if (formGroup) {
            formGroup.appendChild(matchMsg);
        } else {
            password2.parentNode.parentNode.appendChild(matchMsg);
        }

        password2.addEventListener('input', function () {
            if (password2.value === '') {
                matchMsg.textContent = '';
            } else if (password1.value === password2.value) {
                matchMsg.textContent = '✓ Passwords match';
                matchMsg.style.color = '#16a34a';
            } else {
                matchMsg.textContent = '✗ Passwords do not match';
                matchMsg.style.color = '#dc2626';
            }
        });
    }

});