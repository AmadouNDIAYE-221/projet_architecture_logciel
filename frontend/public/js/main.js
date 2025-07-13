let currentPage = 1;
let token = localStorage.getItem('token');
let role = localStorage.getItem('role');
let categories = [];

console.log('Initialisation de main.js', { token, role });

function loadArticles(direction) {
    console.log('Chargement des articles', { direction, currentPage });
    if (direction === 'next') currentPage++;
    if (direction === 'previous' && currentPage > 1) currentPage--;
    const categoryId = document.getElementById('category').value;
    let url = `http://localhost:5000/articles?page=${currentPage}`;
    if (categoryId) url += `&category_id=${categoryId}`;
    
    console.log('Requête envoyée :', url);
    fetch(url)
        .then(response => {
            console.log('Réponse fetch /articles', response.status);
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(`Erreur HTTP ${response.status}: ${err.error || 'Unknown error'}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Articles chargés', data);
            const articlesDiv = document.getElementById('articles');
            articlesDiv.innerHTML = '';
            if (data.length === 0) {
                articlesDiv.innerHTML = '<p class="text-gray-600">Aucun article trouvé.</p>';
                return;
            }
            data.forEach(article => {
                const articleElement = document.createElement('div');
                articleElement.className = 'bg-white p-4 rounded-lg shadow cursor-pointer hover:shadow-xl transition duration-200';
                articleElement.innerHTML = `<h2 class="text-lg font-semibold">${article.title}</h2><p class="text-gray-600">${article.summary}</p>`;
                articleElement.addEventListener('click', () => openModal(article.id));
                articlesDiv.appendChild(articleElement);
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement des articles:', error);
            document.getElementById('articles').innerHTML = `<p class="text-red-500">${error.message}</p>`;
        });
}

function loadCategories() {
    console.log('Chargement des catégories');
    fetch('http://localhost:5000/categories')
        .then(response => {
            console.log('Réponse fetch /categories', response.status);
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(`Erreur HTTP ${response.status}: ${err.error || 'Unknown error'}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Catégories chargées', data);
            categories = data;
            const categorySelect = document.getElementById('category');
            categorySelect.innerHTML = '<option value="">Toutes</option>';
            data.forEach(category => {
                categorySelect.innerHTML += `<option value="${category.id}">${category.name}</option>`;
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement des catégories:', error);
            document.getElementById('category').innerHTML = `<option value="">Erreur: ${error.message}</option>`;
        });
}

function openModal(articleId) {
    console.log('Ouverture modale pour article', articleId);
    fetch(`http://localhost:5000/articles/${articleId}`)
        .then(response => {
            console.log('Réponse fetch /articles/' + articleId, response.status);
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(`Erreur HTTP ${response.status}: ${err.error || 'Unknown error'}`);
                });
            }
            return response.json();
        })
        .then(article => {
            console.log('Article chargé', article);
            const category = categories.find(cat => cat.id === article.category_id);
            document.getElementById('modalTitle').textContent = article.title;
            document.getElementById('modalSummary').textContent = article.summary;
            document.getElementById('modalCategory').textContent = `Catégorie : ${category ? category.name : 'Inconnue'}`;
            document.getElementById('articleModal').classList.remove('hidden');
        })
        .catch(error => {
            console.error('Erreur lors du chargement de l\'article:', error);
            document.getElementById('articles').innerHTML = `<p class="text-red-500">${error.message}</p>`;
        });
}

function closeModal() {
    console.log('Fermeture modale');
    document.getElementById('articleModal').classList.add('hidden');
}

if (token) {
    console.log('Utilisateur connecté', { role });
    document.getElementById('authStatus').innerHTML = `
        <p class="text-green-600">Connecté en tant que ${role} | <a href="login.html" onclick="localStorage.clear()" class="text-blue-500 hover:underline">Déconnexion</a></p>
    `;
    if (role === 'editeur') {
        document.getElementById('editorPanel').classList.remove('hidden');
    } else if (role === 'administrateur') {
        document.getElementById('adminPanel').classList.remove('hidden');
        document.getElementById('editorPanel').classList.remove('hidden');
    }
} else {
    console.log('Utilisateur non connecté');
    document.getElementById('authStatus').innerHTML = `
        <a href="login.html" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-200">Se connecter</a>
    `;
}

console.log('Lancement des fonctions initiales');
loadCategories();
loadArticles();