document.addEventListener('DOMContentLoaded', function () {

    const bookingId = window.CHAT_BOOKING_ID;
    const messagesEl = document.getElementById('chat-messages');
    const form = document.getElementById('chat-form');
    const input = document.getElementById('chat-input');

    if (!bookingId || !messagesEl || !form) return;

    function getCookie(name) {
        const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return match ? match.pop() : '';
    }

    function loadMessages() {
        fetch(`/api/booking/${bookingId}/chat/`)
            .then(res => res.json())
            .then(data => {
                if (!data.messages) return;
                messagesEl.innerHTML = data.messages.map(function (m) {
                    const align = m.is_me ? 'flex-end' : 'flex-start';
                    const bg = m.is_me ? 'var(--navy)' : 'var(--light-grey)';
                    const color = m.is_me ? 'var(--white)' : 'var(--text-main)';
                    const deleteBtn = m.is_me
                        ? `<button class="chat-delete-btn" data-message-id="${m.id}" title="Delete message" style="background:none; border:none; color:var(--text-muted); font-size:.75rem; cursor:pointer; margin-top:2px; padding:0;">🗑 Delete</button>`
                        : '';
                    return `
                        <div style="display:flex; flex-direction:column; align-items:${align};">
                            <div style="background:${bg}; color:${color}; padding:8px 14px; border-radius:14px; max-width:75%; font-size:.9rem;">
                                ${m.text}
                            </div>
                            <span style="font-size:.72rem; color:var(--text-muted); margin-top:2px;">${m.sender} · ${m.timestamp}</span>
                            ${deleteBtn}
                        </div>
                    `;
                }).join('');
                messagesEl.scrollTop = messagesEl.scrollHeight;
            });
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;

        fetch(`/api/booking/${bookingId}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: `text=${encodeURIComponent(text)}`,
        }).then(function () {
            input.value = '';
            loadMessages();
        });
    });

    // Event delegation: handles delete clicks even after messages re-render
    messagesEl.addEventListener('click', function (e) {
        const btn = e.target.closest('.chat-delete-btn');
        if (!btn) return;

        const messageId = btn.dataset.messageId;
        if (!confirm('Delete this message?')) return;

        fetch(`/chat/message/${messageId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(res => res.json())
            .then(function (data) {
                if (data.ok) {
                    loadMessages();
                } else {
                    alert(data.error || 'Could not delete message.');
                }
            });
    });

    loadMessages();
    setInterval(loadMessages, 4000);
});