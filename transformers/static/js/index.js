document.addEventListener('DOMContentLoaded', ()=> {
    const apiUrl = '/api/transformers';
    let currentPage = 1;

    // Debounce function to limit the rate of API calls
    function debounce(func, wait) {
        let timeout;
        return function(...args){
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait)
        };
    }

    // Display and fetch transformers
    function loadTransformers(page = 1, name='', affiliation=''){
        const url = `${apiUrl}?page=${page}&name=${encodeURIComponent(name)}&affiliation=${affiliation}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('#transformers-table tbody');
                tbody.innerHTML = '';

                data.transformers.forEach(transformer => {
                    const row = `
                        <tr>
                            <td>${transformer.name}</td>
                            <td>${transformer.affiliation}</td>
                            <td>${transformer.transformation_mode || 'N/A'}</td>

                            <td>
                                <a href="/transformers/${encodeURIComponent(transformer.name)}?page=${page}" >| View</a> |
                                <a href="/transformers/edit/${transformer.id}?page=${page}">Edit</a> |
                                
                            </td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                });

                document.getElementById('page-info').textContent = `Page ${data.page} of ${data.total_pages}`;
                currentPage = data.page;
            });
    }

    // Event Listener for search by name field
    const debouncedLoadTransformers = debounce(() => {
        const name = document.getElementById('name').value;
        const affiliation = document.getElementById('affiliation').value;
        loadTransformers(1, name, affiliation);
    }, 300);

    document.getElementById('name').addEventListener('input', debouncedLoadTransformers);
    document.getElementById('affiliation').addEventListener('input', debouncedLoadTransformers);

    // Search form event lister
    document.getElementById('search-form').addEventListener('submit', event => {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const affiliation = document.getElementById('affiliation').value;
        loadTransformers(1, name, affiliation);
    });

    // Clear button event listener
    document.getElementById('clear-button').addEventListener('click', ()=>{
        document.getElementById('name').value = '';
        document.getElementById('affiliation').value = '';
    });

    // Pagination control
    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            const newUrl = new URL(window.location);
            newUrl.searchParams.set('page', currentPage - 1);
            window.history.pushState({}, '', newUrl);
            loadTransformers(currentPage - 1);

        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        loadTransformers(currentPage + 1);
        // update page in address bar
        const newUrl = new URL(window.location);
        newUrl.searchParams.set('page', currentPage + 1);
        window.history.pushState({}, '', newUrl);
    });

    // Load first page on load or the page from the URL parameter
    const urlParams = new URLSearchParams(window.location.search)
    const page = urlParams.get('page') || 1;
    loadTransformers(page);
});