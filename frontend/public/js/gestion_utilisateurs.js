document.addEventListener('DOMContentLoaded', () => {
         const role = localStorage.getItem('role');
         if (role !== 'administrateur') {
             console.error('Accès non autorisé : redirection vers login.html');
             window.location.href = 'login.html';
             return;
         }

         const userList = document.getElementById('user-list');
         const userForm = document.getElementById('user-form');
         const userModal = document.getElementById('user-modal');
         const userModalTitle = document.getElementById('user-modal-title');
         const userModalClose = document.getElementById('user-modal-close');
         const addUserBtn = document.getElementById('add-user-btn');
         const BASE_URL = 'http://192.168.1.13:5000';

         const getToken = () => localStorage.getItem('token');

         async function loadUsers() {
             try {
                 console.log('Tentative de chargement des utilisateurs...');
                 const token = getToken();
                 if (!token) {
                     throw new Error('Aucun token trouvé. Veuillez vous connecter.');
                 }
                 const response = await fetch(`${BASE_URL}/users`, {
                     method: 'GET',
                     headers: {
                         'Content-Type': 'application/json',
                         'Authorization': `Bearer ${token}`
                     }
                 });
                 console.log('Réponse:', { status: response.status, headers: [...response.headers] });
                 if (!response.ok) {
                     const errorData = await response.json();
                     throw new Error(`Erreur ${response.status}: ${errorData.error || response.statusText}`);
                 }
                 const users = await response.json();
                 console.log('Utilisateurs:', users);
                 userList.innerHTML = '';
                 if (!users || users.length === 0) {
                     userList.innerHTML = '<tr><td colspan="4" class="p-2 text-center text-gray-600">Aucun utilisateur trouvé</td></tr>';
                     return;
                 }
                 users.forEach(user => {
                     const tr = document.createElement('tr');
                     tr.innerHTML = `
                         <td class="p-2 border">${user.id}</td>
                         <td class="p-2 border">${user.username}</td>
                         <td class="p-2 border">${user.role}</td>
                         <td class="p-2 border flex space-x-2">
                             <button class="edit-btn bg-gray-600 text-white p-1 rounded hover:bg-gray-700" data-id="${user.id}">Modifier</button>
                             <button class="delete-btn bg-red-600 text-white p-1 rounded hover:bg-red-700" data-id="${user.id}">Supprimer</button>
                         </td>
                     `;
                     userList.appendChild(tr);
                 });

                 document.querySelectorAll('.edit-btn').forEach(btn => {
                     btn.addEventListener('click', async (e) => {
                         const userId = e.target.dataset.id;
                         try {
                             const response = await fetch(`${BASE_URL}/users/${userId}`, {
                                 method: 'GET',
                                 headers: {
                                     'Authorization': `Bearer ${token}`,
                                     'Content-Type': 'application/json'
                                 }
                             });
                             if (!response.ok) {
                                 const errorData = await response.json();
                                 throw new Error(`Erreur ${response.status}: ${errorData.error || response.statusText}`);
                             }
                             const user = await response.json();
                             document.getElementById('user-id').value = user.id;
                             document.getElementById('username').value = user.username;
                             document.getElementById('password').value = '';
                             document.getElementById('role').value = user.role;
                             userModalTitle.textContent = 'Modifier un utilisateur';
                             userModal.classList.remove('hidden');
                         } catch (error) {
                             console.error('Erreur chargement utilisateur:', error);
                             alert(`Erreur: ${error.message}`);
                         }
                     });
                 });

                 document.querySelectorAll('.delete-btn').forEach(btn => {
                     btn.addEventListener('click', async (e) => {
                         const userId = e.target.dataset.id;
                         if (confirm('Voulez-vous supprimer cet utilisateur ?')) {
                             try {
                                 const response = await fetch(`${BASE_URL}/users/${userId}`, {
                                     method: 'DELETE',
                                     headers: {
                                         'Authorization': `Bearer ${token}`,
                                         'Content-Type': 'application/json'
                                     }
                                 });
                                 if (!response.ok) {
                                     const errorData = await response.json();
                                     throw new Error(`Erreur ${response.status}: ${errorData.error || response.statusText}`);
                                 }
                                 loadUsers();
                             } catch (error) {
                                 console.error('Erreur suppression:', error);
                                 alert(`Erreur: ${error.message}`);
                             }
                         }
                     });
                 });
             } catch (error) {
                 console.error('Erreur chargement utilisateurs:', error);
                 userList.innerHTML = `<tr><td colspan="4" class="p-2 text-center text-red-600">Erreur: ${error.message}</td></tr>`;
             }
         }

         addUserBtn.addEventListener('click', () => {
             userModalTitle.textContent = 'Ajouter un utilisateur';
             userForm.reset();
             document.getElementById('user-id').value = '';
             userModal.classList.remove('hidden');
         });

         userModalClose.addEventListener('click', () => {
             userModal.classList.add('hidden');
         });

         userForm.addEventListener('submit', async (e) => {
             e.preventDefault();
             const userId = document.getElementById('user-id').value;
             const username = document.getElementById('username').value;
             const password = document.getElementById('password').value;
             const role = document.getElementById('role').value;
             const token = getToken();

             try {
                 const method = userId ? 'PUT' : 'POST';
                 const url = userId ? `${BASE_URL}/users/${userId}` : `${BASE_URL}/users`;
                 const response = await fetch(url, {
                     method,
                     headers: {
                         'Content-Type': 'application/json',
                         'Authorization': `Bearer ${token}`
                     },
                     body: JSON.stringify({ username, password, role })
                 });
                 if (!response.ok) {
                     const errorData = await response.json();
                     throw new Error(`Erreur ${response.status}: ${errorData.error || response.statusText}`);
                 }
                 userModal.classList.add('hidden');
                 loadUsers();
             } catch (error) {
                 console.error('Erreur soumission:', error);
                 alert(`Erreur: ${error.message}`);
             }
         });

         loadUsers();
     });