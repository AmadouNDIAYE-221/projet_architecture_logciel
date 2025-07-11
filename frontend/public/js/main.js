// frontend/public/js/main.js
let currentPage = 1;

function loadArticles(direction) {
    if (direction === 'next') currentPage++;
    if (direction === 'previous' && currentPage > 1) currentPage--;
    fetch(`http://localhost:5000/articles?page=${currentPage}`)
        .then(response => {
            if (!response.ok) throw new Error('Erreur HTTP : ' + response.status);
            return response.json();
        })
        .then(data => {
            const articlesDiv = document.getElementById('articles');
            articlesDiv.innerHTML = '';
            data.forEach(article => {
                const articleElement = document.createElement('div');
                articleElement.innerHTML = `<h2>${article.title}</h2><p>${article.summary}</p>`;
                articlesDiv.appendChild(articleElement);
            });
        })
        .catch(error => console.error('Erreur:', error));
}

loadArticles();