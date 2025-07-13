document.addEventListener('DOMContentLoaded', () => {
      console.log('Initialisation de gestion_categories.js');
      const token = localStorage.getItem('token');
      const role = localStorage.getItem('role');
      
      if (!token || !['editeur', 'administrateur'].includes(role)) {
          console.log('Accès non autorisé, redirection vers login.html');
          window.location.href = '/login.html';
          return;
      }

      const categoryList = document.getElementById('categoryTable');
      const categoryModal = document.getElementById('categoryModal');
      const categoryForm = document.getElementById('categoryForm');
      const modalTitle = document.getElementById('modalTitle');
      const modalSubmit = document.getElementById('modalSubmit');
      const categoryNameInput = document.getElementById('categoryName');
      const addCategoryBtn = document.getElementById('addCategoryBtn');
      const modalClose = document.getElementById('modalClose');

      let editingCategoryId = null;

      function loadCategories() {
          console.log('Chargement des catégories');
          fetch('http://192.168.1.13:5000/categories', {
              headers: { 'Authorization': `Bearer ${token}` }
          })
              .then(response => {
                  console.log('Réponse fetch /categories', response.status);
                  if (!response.ok) {
                      return response.text().then(text => {
                          throw new Error(`Erreur HTTP ${response.status}: ${text}`);
                      });
                  }
                  return response.json();
              })
              .then(data => {
                  console.log('Catégories chargées', data);
                  categoryList.innerHTML = '';
                  if (data.length === 0) {
                      categoryList.innerHTML = '<tr><td colspan="3" class="p-2 text-center">Aucune catégorie trouvée</td></tr>';
                      return;
                  }
                  data.forEach(category => {
                      const tr = document.createElement('tr');
                      tr.innerHTML = `
                          <td class="p-2">${category.id}</td>
                          <td class="p-2">${category.name}</td>
                          <td class="p-2">
                              <button class="bg-gray-500 text-white px-2 py-1 rounded edit-btn" data-id="${category.id}">Modifier</button>
                              <button class="bg-red-600 text-white px-2 py-1 rounded delete-btn" data-id="${category.id}">Supprimer</button>
                          </td>
                      `;
                      categoryList.appendChild(tr);
                  });

                  document.querySelectorAll('.edit-btn').forEach(btn => {
                      btn.addEventListener('click', () => editCategory(btn.dataset.id));
                  });
                  document.querySelectorAll('.delete-btn').forEach(btn => {
                      btn.addEventListener('click', () => deleteCategory(btn.dataset.id));
                  });
              })
              .catch(error => {
                  console.error('Erreur chargement catégories:', error);
                  categoryList.innerHTML = `<tr><td colspan="3" class="p-2 text-red-500">${error.message}</td></tr>`;
              });
      }

      function openModal(mode, category = null) {
          console.log('Ouverture modale', { mode, category });
          editingCategoryId = mode === 'edit' ? category.id : null;
          modalTitle.textContent = mode === 'edit' ? 'Modifier la catégorie' : 'Ajouter une catégorie';
          modalSubmit.textContent = mode === 'edit' ? 'Modifier' : 'Ajouter';
          categoryNameInput.value = category ? category.name : '';
          categoryModal.classList.remove('hidden');
      }

      function closeModal() {
          console.log('Fermeture modale');
          categoryModal.classList.add('hidden');
          categoryNameInput.value = '';
          editingCategoryId = null;
      }

      function editCategory(id) {
          console.log('Modification catégorie', id);
          fetch(`http://192.168.1.13:5000/categories/${id}`, {
              headers: { 'Authorization': `Bearer ${token}` }
          })
              .then(response => {
                  console.log('Réponse fetch /categories/' + id, response.status);
                  if (!response.ok) {
                      return response.text().then(text => {
                          throw new Error(`Erreur HTTP ${response.status}: ${text}`);
                      });
                  }
                  return response.json();
              })
              .then(category => {
                  console.log('Catégorie chargée pour modification', category);
                  openModal('edit', category);
              })
              .catch(error => {
                  console.error('Erreur chargement catégorie:', error);
                  categoryList.innerHTML = `<tr><td colspan="3" class="p-2 text-red-500">${error.message}</td></tr>`;
              });
      }

      function deleteCategory(id) {
          if (!confirm('Voulez-vous vraiment supprimer cette catégorie ?')) return;
          console.log('Suppression catégorie', id);
          fetch(`http://192.168.1.13:5000/categories/${id}`, {
              method: 'DELETE',
              headers: { 'Authorization': `Bearer ${token}` }
          })
              .then(response => {
                  console.log('Réponse fetch DELETE /categories/' + id, response.status);
                  if (!response.ok) {
                      return response.text().then(text => {
                          throw new Error(`Erreur HTTP ${response.status}: ${text}`);
                      });
                  }
                  console.log('Catégorie supprimée');
                  loadCategories();
              })
              .catch(error => {
                  console.error('Erreur suppression catégorie:', error);
                  categoryList.innerHTML = `<tr><td colspan="3" class="p-2 text-red-500">${error.message}</td></tr>`;
              });
      }

      categoryForm.addEventListener('submit', (e) => {
          e.preventDefault();
          const name = categoryNameInput.value.trim();
          if (!name) {
              alert('Le nom de la catégorie est requis');
              return;
          }

          const method = editingCategoryId ? 'PUT' : 'POST';
          const url = editingCategoryId ? `http://192.168.1.13:5000/categories/${editingCategoryId}` : 'http://192.168.1.13:5000/categories';
          console.log('Envoi catégorie', { method, url, name });

          fetch(url, {
              method,
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({ name })
          })
              .then(response => {
                  console.log('Réponse fetch ' + method + ' /categories', response.status);
                  if (!response.ok) {
                      return response.text().then(text => {
                          throw new Error(`Erreur HTTP ${response.status}: ${text}`);
                      });
                  }
                  return response.json();
              })
              .then(data => {
                  console.log('Catégorie enregistrée', data);
                  closeModal();
                  loadCategories();
              })
              .catch(error => {
                  console.error('Erreur envoi catégorie:', error);
                  alert(`Erreur: ${error.message}`);
              });
      });

      addCategoryBtn.addEventListener('click', () => openModal('add'));
      modalClose.addEventListener('click', closeModal);

      loadCategories();
  });