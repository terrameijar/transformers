document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page') || 1;
    document.getElementById('back-to-list').href = `/?page=${page}`
})