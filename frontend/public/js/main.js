// frontend/public/js/main.js
let currentPage = 1;
let token = localStorage.getItem('token');
let role = localStorage.getItem('role');

function loadArticles(direction) {
    if (direction === 'next') currentPage++;
    if (direction === 'previous' && currentPage > 1) currentPage--;
    const category = document.getElementById('category').value;
    let url = `http://localhost:5000/articles?page=${currentPage}`;
    if (category) url += `&category=${category}`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
            return response.json();
        })
        .then(data => {
            const articlesDiv = document.getElementById('articles');
            articlesDiv.innerHTML = '';
            data.forEach(article => {
                const articleElement = document.createElement('div');
                articleElement.className = 'bg-white p-4 rounded-lg shadow';
                articleElement.innerHTML = `<h2 class="text-lg font-semibold">${article.title}</h2><p class="text-gray-600">${article.summary}</p>`;
                if (token && (role === 'editor' || role === 'admin')) {
                    articleElement.innerHTML += `
                        <div class="mt-2">
                            <button onclick="updateArticle(${article.id}, '${article.title}', '${article.summary}', ${article.category_id})" class="bg-blue-500 text-white px-3 py-1 rounded-md hover:bg-blue-600 transition duration-200">Modifier</button>
                            <button onclick="deleteArticle(${article.id})" class="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 transition duration-200">Supprimer</button>
                        </div>
                    `;
                }
                articlesDiv.appendChild(articleElement);
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
            document.getElementById('articles').innerHTML = '<p class="text-red-500">Erreur lors du chargement des articles</p>';
        });
}

function loadCategories() {
    fetch('http://localhost:5000/categories')
        .then(response => {
            if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
            return response.json();
        })
        .then(data => {
            const categorySelect = document.getElementById('category');
            const articleCategorySelect = document.getElementById('category_id');
            categorySelect.innerHTML = '<option value="">Toutes</option>';
            data.forEach(category => {
                categorySelect.innerHTML += `<option value="${category.id}">${category.name}</option>`;
                articleCategorySelect.innerHTML += `<option value="${category.id}">${category.name}</option>`;
            });
        })
        .catch(error => console.error('Erreur:', error));
}

function addArticle(title, summary, category_id) {
    fetch('http://localhost:5000/articles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title, summary, category_id })
    })
        .then(response => {
            if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
            return response.json();
        })
        .then(data => loadArticles())
        .catch(error => console.error('Erreur:', error));
}

function updateArticle(id, title, summary, category_id) {
    const newTitle = prompt('Nouveau titre :', title);
    const newSummary = prompt('Nouveau résumé :', summary);
    const newCategory = prompt('Nouvelle catégorie ID :', category_id);
    if (newTitle && newSummary && newCategory) {
        fetch(`http://localhost:5000/articles/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title: newTitle, summary: newSummary, category_id: newCategory })
        })
            .then(response => {
                if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
                return response.json();
            })
            .then(data => loadArticles())
            .catch(error => console.error('Erreur:', error));
    }
}

function deleteArticle(id) {
    if (confirm('Supprimer cet article ?')) {
        fetch(`http://localhost:5000/articles/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(response => {
                if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
                return response.json();
            })
            .then(data => loadArticles())
            .catch(error => console.error('Erreur:', error));
    }
}

function loadUsers() {
    if (role !== 'admin') return;
    fetch('http://localhost:5000/users', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    })
        .then(response => {
            if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
            return response.json();
        })
        .then(data => {
            const userList = document.getElementById('userList');
            userList.innerHTML = '<h3 class="text-lg font-semibold mb-2">Liste des utilisateurs</h3>';
            data.forEach(user => {
                userList.innerHTML += `
                    <div class="flex justify-between items-center p-2 border-b">
                        <span>${user.username} (${user.role})</span>
                        <button onclick="deleteUser('${user.username}')" class="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 transition duration-200">Supprimer</button>
                    </div>
                `;
            });
        })
        .catch(error => console.error('Erreur:', error));
}

function addUser(username, password, role) {
    fetch('http://localhost:5000/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ username, password, role })
    })
        .then(response => {
            if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
            return response.json();
        })
        .then(data => loadUsers())
        .catch(error => console.error('Erreur:', error));
}

function deleteUser(username) {
    if (confirm(`Supprimer l'utilisateur ${username} ?`)) {
        fetch(`http://localhost:5000/users/${username}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(response => {
                if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
                return response.json();
            })
            .then(data => loadUsers())
            .catch(error => console.error('Erreur:', error));
    }
}

document.getElementById('articleForm').addEventListener('submit', (event) => {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const summary = document.getElementById('summary').value;
    const category_id = document.getElementById('category_id').value;
    addArticle(title, summary, category_id);
});

document.getElementById('userForm').addEventListener('submit', (event) => {
    event.preventDefault();
    const username = document.getElementById('newUsername').value;
    const password = document.getElementById('newPassword').value;
    const role = document.getElementById('newRole').value;
    addUser(username, password, role);
});

if (token) {
    document.getElementById('authStatus').innerHTML = `
        <p class="text-green-600">Connecté en tant que ${role} | <a href="login.html" onclick="localStorage.clear()" class="text-blue-500 hover:underline">Déconnexion</a></p>
    `;
    if (role === 'editor' || role === 'admin') {
        document.getElementById('editorPanel').classList.remove('hidden');
    }
    if (role === 'admin') {
        document.getElementById('adminPanel').classList.remove('hidden');
        loadUsers();
    }
} else {
    window.location.href = 'login.html';
}

loadCategories();
loadArticles();