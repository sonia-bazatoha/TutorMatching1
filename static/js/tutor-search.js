document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.getElementById('tutor-search-input');
    const subjectFilter = document.getElementById('tutor-subject-filter');
    const resultsContainer = document.getElementById('tutor-results');
    const loading = document.getElementById('tutor-loading');

    if (!resultsContainer) return;

    const urlParams = new URLSearchParams(window.location.search);
    const semester = urlParams.get('semester') || '';

    let debounceTimer = null;

    function getCurrentSubjectId() {
        return subjectFilter ? subjectFilter.value : '';
    }

    function buildTutorCard(tutor) {
        const subjects = tutor.subjects.map(s =>
            `<span class="tutor-tag">${s}</span>`
        ).join('');

        const subjectId = getCurrentSubjectId();

        const viewProfileUrl = subjectId
            ? `/tutor/${tutor.id}/?subject=${subjectId}`
            : `/tutor/${tutor.id}/`;

        const bookingUrl = subjectId
            ? `/book/${tutor.id}/?subject=${subjectId}`
            : '';

        const bookBtn = subjectId
            ? `<a href="${bookingUrl}" class="btn btn-outline btn-sm">Book Session</a>`
            : '';

        const avatarHtml = tutor.profile_picture
            ? `<img src="${tutor.profile_picture}" style="width:100%; height:100%; object-fit:cover; border-radius:50%;">`
            : '👤';

        return `
            <div class="tutor-card">
                <div class="tutor-avatar">${avatarHtml}</div>
                <div class="tutor-info">
                    <h3>${tutor.name}</h3>
                    <p class="tutor-meta">🎓 ${tutor.qualification} &nbsp;·&nbsp; ${tutor.years_of_experience} years experience</p>
                    <p style="font-size:.88rem; color:var(--text-muted);">UGX ${tutor.hourly_rate} / hour</p>
                    <div class="tutor-tags">${subjects}</div>
                    <div class="action-row" style="margin-top:10px;">
                        <a href="${viewProfileUrl}" class="btn btn-primary btn-sm">View Profile</a>
                        ${bookBtn}
                    </div>
                </div>
            </div>
        `;
    }

    function search() {
        if (!semester) return;

        const q = searchInput ? searchInput.value.trim() : '';
        const subjectId = getCurrentSubjectId();

        const url = new URL(window.location.href);
        url.searchParams.set('semester', semester);
        if (subjectId) {
            url.searchParams.set('subject', subjectId);
        } else {
            url.searchParams.delete('subject');
        }
        window.history.replaceState({}, '', url);

        loading.style.display = 'block';
        resultsContainer.style.display = 'none';

        fetch(`/api/tutors/?q=${encodeURIComponent(q)}&subject=${encodeURIComponent(subjectId)}&semester=${encodeURIComponent(semester)}`)
            .then(res => res.json())
            .then(data => {
                loading.style.display = 'none';
                resultsContainer.style.display = 'flex';

                if (data.tutors.length === 0) {
                    resultsContainer.innerHTML = `
                        <div class="ct-card" style="text-align:center; padding:30px; color:var(--text-muted);">
                            <p>No tutors found for your selection.</p>
                        </div>
                    `;
                } else {
                    resultsContainer.innerHTML = data.tutors.map(buildTutorCard).join('');
                }
            })
            .catch(function () {
                loading.style.display = 'none';
                resultsContainer.style.display = 'flex';
                resultsContainer.innerHTML = `
                    <div class="ct-card" style="text-align:center; padding:30px; color:var(--text-muted);">
                        <p>Something went wrong. Please try again.</p>
                    </div>
                `;
            });
    }

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(search, 400);
        });
    }

    if (subjectFilter) {
        subjectFilter.addEventListener('change', search);
    }

});