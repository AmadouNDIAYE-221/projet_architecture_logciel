document.addEventListener('DOMContentLoaded', () => {
         console.log('Initialisation de gestion_articles.js');
         const token = localStorage.getItem('token');
         const role = localStorage.getItem('role');
         let categories = [];

         // Vérifier l'accès
         if (!token || !['editeur', 'editor', 'administrateur'].includes(role)) {
             console.error('Accès non autorisé : token ou rôle invalide', { token, role });
             alert('Accès non autorisé. Veuillez vous connecter.');
             window.location.href = 'login.html';
             return;
         }

         // Charger les catégories
         async function loadCategories() {
             console.log('Chargement des catégories');
             const categorySelect = document.getElementById('category_id');
             if (!categorySelect) {
                 console.error('Élément category_id non trouvé dans le DOM');
                 return;
             }
             try {
                 const response = await fetch('http://192.168.1.13:5000/categories', {
                     headers: { 'Authorization': `Bearer ${token}` }
                 });
                 if (!response.ok) {
                     const errData = await response.json();
                     throw new Error(`Erreur HTTP ${response.status}: ${errData.error || 'Erreur inconnue'}`);
                 }
                 categories = await response.json();
                 console.log('Catégories chargées', categories);
                 categorySelect.innerHTML = '<option value="">Sélectionner une catégorie</option>';
                 if (categories.length === 0) {
                     console.warn('Aucune catégorie disponible');
                     categorySelect.innerHTML = '<option value="">Aucune catégorie disponible</option>';
                 } else {
                     categories.forEach(category => {
                         categorySelect.innerHTML += `<option value="${category.id}">${category.name}</option>`;
                     });
                 }
             } catch (error) {
                 console.error('Erreur lors du chargement des catégories:', error);
                 categorySelect.innerHTML = `<option value="">Erreur: ${error.message}</option>`;
             }
         }

         // Charger les articles
         async function loadArticles() {
             console.log('Chargement des articles');
             const articleList = document.getElementById('article-list');
             if (!articleList) {
                 console.error('Élément article-list non trouvé dans le DOM');
                 return;
             }
             try {
                 const response = await fetch('http://192.168.1.13:5000/articles?page=1', {
                     headers: { 'Authorization': `Bearer ${token}` }
                 });
                 if (!response.ok) {
                     const errData = await response.json();
                     throw new Error(`Erreur HTTP ${response.status}: ${errData.error || 'Erreur inconnue'}`);
                 }
                 const articles = await response.json();
                 console.log('Articles chargés', articles);
                 articleList.innerHTML = '';
                 if (articles.length === 0) {
                     articleList.innerHTML = '<tr><td colspan="5" class="text-center p-4">Aucun article trouvé</td></tr>';
                     return;
                 }
                 articles.forEach(article => {
                     const category = categories.find(cat => cat.id === article.category_id);
                     const tr = document.createElement('tr');
                     tr.innerHTML = `
                         <td class="px-4 py-2">${article.id}</td>
                         <td class="px-4 py-2">${article.title}</td>
                         <td class="px-4 py-2">${article.summary}</td>
                         <td class="px-4 py-2">${category ? category.name : 'Inconnue'}</td>
                         <td class="px-4 py-2">
                             <button onclick="editArticle(${article.id})" class="bg-gray-500 text-white p-1 rounded mr-2">Modifier</button>
                             <button onclick="deleteArticle(${article.id})" class="bg-red-600 text-white p-1 rounded">Supprimer</button>
                         </td>
                     `;
                     articleList.appendChild(tr);
                 });
             } catch (error) {
                 console.error('Erreur lors du chargement des articles:', error);
                 articleList.innerHTML = `<tr><td colspan="5" class="text-center p-4 text-red-500">${error.message}</td></tr>`;
             }
         }

         // Ouvrir la modale pour ajouter/modifier
         function openModal(mode, article = null) {
             console.log('Ouverture de la modale', { mode, article });
             const modal = document.getElementById('article-modal');
             const modalTitle = document.getElementById('article-modal-title');
             const form = document.getElementById('article-form');
             const articleIdInput = document.getElementById('article-id');
             const titleInput = document.getElementById('title');
             const summaryInput = document.getElementById('summary');
             const categorySelect = document.getElementById('category_id');

             if (!modal || !modalTitle || !form || !articleIdInput || !titleInput || !summaryInput || !categorySelect) {
                 console.error('Un ou plusieurs éléments de la modale sont manquants dans le DOM', {
                     modal, modalTitle, form, articleIdInput, titleInput, summaryInput, categorySelect
                 });
                 alert('Erreur : Éléments de la modale non trouvés.');
                 return;
             }

             modalTitle.textContent = mode === 'add' ? 'Ajouter un article' : 'Modifier un article';
             articleIdInput.value = article ? article.id : '';
             titleInput.value = article ? article.title : '';
             summaryInput.value = article ? article.summary : '';
             categorySelect.value = article && article.category_id !== null ? article.category_id : '';

             modal.classList.remove('hidden');
         }

         // Fermer la modale
         document.getElementById('article-modal-close').addEventListener('click', () => {
             console.log('Fermeture de la modale');
             document.getElementById('article-modal').classList.add('hidden');
         });

         // Ajouter/Modifier un article
         document.getElementById('article-form').addEventListener('submit', async (e) => {
             e.preventDefault();
             const articleId = document.getElementById('article-id').value;
             const title = document.getElementById('title').value;
             const summary = document.getElementById('summary').value;
             const category_id = document.getElementById('category_id').value;

             if (!category_id) {
                 alert('Veuillez sélectionner une catégorie.');
                 return;
             }

             const method = articleId ? 'PUT' : 'POST';
             const url = articleId ? `http://192.168.1.13:5000/articles/${articleId}` : 'http://192.168.1.13:5000/articles';
             console.log('Envoi de l’article', { method, url, title, summary, category_id });

             try {
                 const response = await fetch(url, {
                     method,
                     headers: {
                         'Content-Type': 'application/json',
                         'Authorization': `Bearer ${token}`
                     },
                     body: JSON.stringify({ title, summary, category_id: parseInt(category_id) })
                 });
                 if (!response.ok) {
                     const errData = await response.json();
                     throw new Error(`Erreur HTTP ${response.status}: ${errData.error || 'Erreur inconnue'}`);
                 }
                 const data = await response.json();
                 console.log('Article enregistré', data);
                 document.getElementById('article-modal').classList.add('hidden');
                 loadArticles();
             } catch (error) {
                 console.error('Erreur lors de l’enregistrement de l’article:', error);
                 alert(`Erreur: ${error.message}`);
             }
         });

         // Modifier un article
         window.editArticle = async function(id) {
             console.log('Modification article', id);
             try {
                 const response = await fetch(`http://192.168.1.13:5000/articles/${id}`, {
                     headers: { 'Authorization': `Bearer ${token}` }
                 });
                 if (!response.ok) {
                     const errData = await response.json();
                     throw new Error(`Erreur HTTP ${response.status}: ${errData.error || 'Erreur inconnue'}`);
                 }
                 const article = await response.json();
                 console.log('Article chargé pour modification', article);
                 openModal('edit', article);
             } catch (error) {
                 console.error('Erreur lors du chargement de l’article:', error);
                 alert(`Erreur: ${error.message}`);
             }
         };

         // Supprimer un article
         window.deleteArticle = async function(id) {
             if (!confirm('Voulez-vous supprimer cet article ?')) return;
             console.log('Suppression article', id);
             try {
                 const response = await fetch(`http://192.168.1.13:5000/articles/${id}`, {
                     method: 'DELETE',
                     headers: { 'Authorization': `Bearer ${token}` }
                 });
                 if (!response.ok) {
                     const errData = await response.json();
                     throw new Error(`Erreur HTTP ${response.status}: ${errData.error || 'Erreur inconnue'}`);
                 }
                 console.log('Article supprimé', id);
                 loadArticles();
             } catch (error) {
                 console.error('Erreur lors de la suppression de l’article:', error);
                 alert(`Erreur: ${error.message}`);
             }
         };

         // Bouton pour ouvrir la modale d'ajout
         const addArticleBtn = document.getElementById('add-article-btn');
         if (addArticleBtn) {
             addArticleBtn.addEventListener('click', () => {
                 console.log('Ouverture de la modale pour ajout');
                 openModal('add');
             });
         } else {
             console.error('Bouton add-article-btn non trouvé dans le DOM');
         }

         // Initialisation
         loadCategories();
         loadArticles();
     });