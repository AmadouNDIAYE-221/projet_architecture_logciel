let state = {
    token: localStorage.getItem('token'),
    role: localStorage.getItem('role'),
    currentPage: 1,
    articlesPerPage: 2,
    categories: [],
    totalArticles: 0
};

document.addEventListener('DOMContentLoaded', () => {
    console.log('Initialisation de main.js, page:', window.location.pathname);
    console.log('État initial:', state);

    if (window.location.pathname !== '/' && !window.location.pathname.includes('index.html')) {
        console.error('main.js chargé sur une page incorrecte:', window.location.pathname);
        return;
    }

    const categorySelect = document.getElementById('category');
    const articlesDiv = document.getElementById('articles');
    const authStatus = document.getElementById('authStatus');
    const pageInfo = document.getElementById('pageInfo');

    if (!categorySelect || !articlesDiv || !authStatus) {
        console.error('Éléments DOM manquants essentiels:', {
            category: !!categorySelect,
            articles: !!articlesDiv,
            authStatus: !!authStatus
        });
        return;
    }

    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            console.log('Clic sur Précédent');
            loadArticles('previous');
        });
    } else {
        console.error('Bouton Précédent non trouvé');
    }
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            console.log('Clic sur Suivant');
            loadArticles('next');
        });
    } else {
        console.error('Bouton Suivant non trouvé');
    }

    updateAuthStatus();
    loadCategories();
    loadArticles();
});

function updateAuthStatus() {
    const authStatus = document.getElementById('authStatus');
    if (!authStatus) {
        console.error('authStatus non trouvé dans le DOM');
        return;
    }
    if (state.token && state.role) {
        console.log('Utilisateur connecté, rôle:', state.role);
        authStatus.innerHTML = `<a href="#" onclick="logout()" class="bg-red-600 text-white border-4 border-red-700 rounded-lg px-4 py-2 text-lg font-semibold hover:bg-red-700">Se déconnecter</a>`;
    } else {
        console.log('Utilisateur non connecté');
        authStatus.innerHTML = `<a href="login.html" class="bg-blue-600 text-white border-4 border-blue-700 rounded-lg px-4 py-2 text-lg font-semibold hover:bg-blue-700">Se connecter</a>`;
    }
}

function logout() {
    console.log('Déconnexion');
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    state.token = null;
    state.role = null;
    window.location.replace('/index.html');
}

async function loadCategories() {
    console.log('Chargement des catégories');
    const categorySelect = document.getElementById('category');
    if (!categorySelect) {
        console.error('category non trouvé dans le DOM');
        return;
    }
    try {
        const response = await fetch('http://192.168.1.13:5000/categories');
        console.log('Réponse fetch /categories:', response.status, response.statusText);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        state.categories = await response.json();
        console.log('Catégories reçues:', state.categories);
        categorySelect.innerHTML = '<option value="">Toutes</option>';
        if (state.categories.length === 0) {
            console.log('Aucune catégorie trouvée');
            categorySelect.innerHTML += '<option value="">Aucune catégorie</option>';
        } else {
            state.categories.forEach(category => {
                console.log('Ajout catégorie:', category);
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Erreur chargement catégories:', error);
        categorySelect.parentElement.appendChild(
            document.createTextNode('Erreur lors du chargement des catégories')
        );
    }
}





// Modifiez la fonction loadArticles comme suit :
async function loadArticles(direction) {
    console.log('Chargement des articles, direction:', direction, 'page:', state.currentPage);
    
    // Sauvegarder l'ancienne page pour revenir en arrière si nécessaire
    const oldPage = state.currentPage;

    // Gérer le changement de page
    if (direction === 'next') {
        state.currentPage++;
    } else if (direction === 'previous') {
        state.currentPage--;
    }

    const categorySelect = document.getElementById('category');
    const articlesDiv = document.getElementById('articles');
    const pageInfo = document.getElementById('pageInfo');
    
    if (!categorySelect || !articlesDiv) {
        console.error('Éléments DOM manquants pour articles:', {
            category: !!categorySelect,
            articles: !!articlesDiv,
            pageInfo: !!pageInfo
        });
        return;
    }

    const categoryId = categorySelect.value;
    const url = `http://192.168.1.13:5000/articles?page=${state.currentPage}&per_page=${state.articlesPerPage}${categoryId ? `&category_id=${categoryId}` : ''}`;
    console.log('URL articles:', url);

    try {
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        console.log('Réponse fetch /articles:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const articles = await response.json();
        console.log('Articles reçus:', articles);

        // Mettre à jour le nombre total d'articles
        const totalCount = parseInt(response.headers.get('X-Total-Count')) || 0;
        state.totalArticles = totalCount;
        
        // Calculer le nombre total de pages
        const totalPages = Math.max(1, Math.ceil(state.totalArticles / state.articlesPerPage));
        console.log('Total articles:', state.totalArticles, 'Total pages:', totalPages);


        // Corriger la page courante si nécessaire
        if (state.currentPage > totalPages) {
            state.currentPage = totalPages;
        }
        if (state.currentPage < 1) {
            state.currentPage = 1;
        }

        // Si la page corrigée est différente de ce qu'on voulait, recharger
        //if (state.currentPage !== (direction === 'next' ? oldPage + 1 : direction === 'previous' ? oldPage - 1 : oldPage)) {
          //  return loadArticles(); // Recharger sans direction
        //}

        // Mettre à jour l'affichage de la pagination
        if (pageInfo) {
            pageInfo.textContent = `Page : ${state.currentPage} / ${totalPages}`;
        }

        // Gérer l'affichage des articles
        if (articles.length === 0) {
            console.log('Aucun article trouvé');
            articlesDiv.innerHTML = '<p class="text-center text-gray-600">Aucun article trouvé</p>';
            return;
        }

        articlesDiv.innerHTML = '';
        articles.forEach(article => {
            const category = state.categories.find(cat => cat.id === article.category_id);
            const categoryName = category ? category.name : 'Inconnue';
            const articleDiv = document.createElement('div');
            articleDiv.className = 'bg-white p-6 rounded-xl shadow-lg';
            articleDiv.innerHTML = `
                <h3 class="text-xl font-semibold text-gray-800 overflow-hidden text-ellipsis" 
                    style="max-height: 1.5em; white-space: nowrap; text-overflow: ellipsis;">${article.title}</h3>
                <p class="text-gray-600 mt-2 overflow-hidden text-ellipsis" 
                    style="max-height: 3em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                    ${article.summary}
                </p>
                <p class="text-gray-500 mt-2 overflow-hidden text-ellipsis" 
                    style="max-height: 1.5em; white-space: nowrap; text-overflow: ellipsis;">Catégorie: ${categoryName}</p>
                <button onclick="showArticleDetails(${article.id})" class="mt-2 bg-blue-600 text-white hover:underline border-2 border-blue-600 rounded-lg px-3 py-1">Voir détails</button>
            `;
            articlesDiv.appendChild(articleDiv);
        });

        // Mettre à jour l'état des boutons
        const prevButton = document.getElementById('prevButton');
        const nextButton = document.getElementById('nextButton');
        if (prevButton) prevButton.disabled = state.currentPage <= 1;
        if (nextButton) nextButton.disabled = state.currentPage >= totalPages;

    } catch (error) {
        console.error('Erreur chargement articles:', error);
        articlesDiv.innerHTML = '<p class="text-center text-gray-600">Erreur lors du chargement des articles</p>';
        // Revenir à l'ancienne page en cas d'erreur
        state.currentPage = oldPage;
    }
}



async function showArticleDetails(id) {
    console.log('Chargement détails article:', id);
    try {
        const response = await fetch(`http://192.168.1.13:5000/articles/${id}`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        console.log('Réponse fetch /articles/' + id + ':', response.status, response.statusText);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const article = await response.json();
        console.log('Détails article:', article);
        const modalTitle = document.getElementById('modalTitle');
        const modalSummary = document.getElementById('modalSummary');
        const modalCategory = document.getElementById('modalCategory');
        const articleModal = document.getElementById('articleModal');
        if (!modalTitle || !modalSummary || !modalCategory || !articleModal) {
            console.error('Éléments modale manquants:', {
                modalTitle: !!modalTitle,
                modalSummary: !!modalSummary,
                modalCategory: !!modalCategory,
                articleModal: !!articleModal
            });
            return;
        }
        const category = state.categories.find(cat => cat.id === article.category_id);
        const categoryName = category ? category.name : 'Inconnue';
        modalTitle.textContent = article.title;
        modalSummary.textContent = article.summary;
        modalCategory.textContent = `Catégorie: ${categoryName}`;
        articleModal.classList.remove('hidden');
    } catch (error) {
        console.error('Erreur chargement détails article:', error);
    }
}

function closeModal() {
    const articleModal = document.getElementById('articleModal');
    if (articleModal) {
        articleModal.classList.add('hidden');
    } else {
        console.error('articleModal non trouvé dans le DOM');
    }
}