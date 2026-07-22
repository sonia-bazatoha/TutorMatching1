document.addEventListener('DOMContentLoaded', function () {

    const programmeFilter = document.getElementById('filter-programme');
    const yearFilter = document.getElementById('filter-year');
    const semesterFilter = document.getElementById('filter-semester');
    const checkboxContainer = document.getElementById('subject-checkboxes');
    const loadingMsg = document.getElementById('subject-loading');
    const addBtn = document.getElementById('add-subjects-btn');
    const savedIdsEl = document.getElementById('saved-subject-ids');

    // Exit if not on the edit tutor profile page
    if (!programmeFilter || !yearFilter || !semesterFilter || !savedIdsEl) return;

    const savedSubjectIds = JSON.parse(savedIdsEl.textContent);

    function loadSubjects() {
        const programme = programmeFilter.value;
        const year = yearFilter.value;
        const semester = semesterFilter.value;

        if (!programme || !year || !semester) return;

        loadingMsg.style.display = 'block';
        checkboxContainer.innerHTML = '';
        addBtn.style.display = 'none';

        fetch(`/api/subjects/filter/?programme=${programme}&year=${year}&semester=${semester}`)
            .then(res => res.json())
            .then(data => {
                loadingMsg.style.display = 'none';

                if (data.subjects.length === 0) {
                    checkboxContainer.innerHTML = '<p style="color:var(--text-muted); font-size:.9rem;">No subjects found for this combination.</p>';
                    return;
                }

                checkboxContainer.innerHTML = data.subjects.map(subject => {
                    const alreadySaved = savedSubjectIds.includes(subject.id);
                    return `
                        <label style="display:flex; align-items:center; gap:6px; font-size:.9rem;
                            background:${alreadySaved ? '#dcfce7' : 'var(--light-grey)'};
                            padding:6px 12px; border-radius:8px; cursor:pointer;">
                            <input type="checkbox" name="subject_ids" value="${subject.id}"
                                form="subject-form"
                                ${alreadySaved ? 'checked' : ''}>
                            ${subject.name}
                            ${alreadySaved ? '<span style="color:#16a34a; font-size:.75rem;">(saved)</span>' : ''}
                        </label>
                    `;
                }).join('');

                addBtn.style.display = 'inline-flex';
            })
            .catch(() => {
                loadingMsg.style.display = 'none';
                checkboxContainer.innerHTML = '<p style="color:red; font-size:.9rem;">Failed to load subjects. Please try again.</p>';
            });
    }

    programmeFilter.addEventListener('change', loadSubjects);
    yearFilter.addEventListener('change', loadSubjects);
    semesterFilter.addEventListener('change', loadSubjects);
});