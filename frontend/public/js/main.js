document.addEventListener('DOMContentLoaded', () => {
    console.log('Initialisation de main.js');
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    console.log('État initial', { token, role });

    if (!token || !role) {
        console.log('Utilisateur non connecté');
        const authStatus = document.getElementById('authStatus');
        if (authStatus) {
            authStatus.innerHTML = '<a href="login.html" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Se connecter</a>';
        } else {
            console.error('Élément authStatus non trouvé');
        }
    } else {
        if (role === 'editor') {
            document.getElementById('editorPanel')?.classList.remove('hidden');
        } else if (role === 'admin') {
            document.getElementById('editorPanel')?.classList.remove('hidden');
            document.getElementById('adminPanel')?.classList.remove('hidden');
        }
    }

    loadCategories();
    loadArticles();

    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', (e) => {
            const categoryId = e.target.value;
            loadArticles(categoryId);
        });
    } else {
        console.error('Élément category non trouvé');
    }
});

async function loadCategories() {
    console.log('Chargement des catégories');
    try {
        const response = await fetch('http://192.168.1.13:5000/categories', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('Réponse fetch /categories', response.status);
        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}: ${await response.text()}`);
        }
        const categories = await response.json();
        console.log('Catégories chargées', categories);
        const categorySelect = document.getElementById('category');
        if (categorySelect) {
            categorySelect.innerHTML = '<option value="">Toutes</option>';
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        } else {
            console.error('Élément category non trouvé pour le remplissage');
        }
    } catch (error) {
        console.error('Erreur chargement catégories:', error);
    }
}

async function loadArticles(categoryId = null) {
    console.log('Chargement des articles', { categoryId });
    try {
        const url = categoryId ? `http://192.168.1.13:5000/articles?category_id=${categoryId}` : 'http://192.168.1.13:5000/articles';
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('Réponse fetch /articles', response.status);
        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}: ${await response.text()}`);
        }
        const articles = await response.json();
        console.log('Articles chargés', articles);
        const articleList = document.getElementById('articles');
        if (articleList) {
            articleList.innerHTML = '';
            articles.forEach(article => {
                const div = document.createElement('div');
                div.className = 'border p-4 mb-4 rounded-lg bg-white shadow';
                div.innerHTML = `
                    <h2 class="text-xl font-bold">${article.title}</h2>
                    <p class="text-gray-600">${article.summary}</p>
                    <button onclick="openArticleModal(${article.id})" class="bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700">Voir détails</button>
                `;
                articleList.appendChild(div);
            });
        } else {
            console.error('Élément articles non trouvé');
        }
    } catch (error) {
        console.error('Erreur chargement articles:', error);
    }
}

async function openArticleModal(articleId) {
    console.log('Ouverture modale article', { articleId });
    try {
        const response = await fetch(`http://192.168.1.13:5000/articles/${articleId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('Réponse fetch /articles/' + articleId, response.status);
        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}: ${await response.text()}`);
        }
        const article = await response.json();
        console.log('Article chargé', article);
        const modal = document.getElementById('articleModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalSummary = document.getElementById('modalSummary');
        const modalCategory = document.getElementById('modalCategory');
        if (modal && modalTitle && modalSummary && modalCategory) {
            modalTitle.textContent = article.title;
            modalSummary.textContent = article.summary;
            modalCategory.textContent = `Catégorie ID: ${article.category_id}`;
            modal.classList.remove('hidden');
        } else {
            console.error('Éléments articleModal, modalTitle, modalSummary ou modalCategory non trouvés');
        }
    } catch (error) {
        console.error('Erreur chargement article:', error);
    }
}

function closeModal() {
    const modal = document.getElementById('articleModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}