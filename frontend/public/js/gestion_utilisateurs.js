document.addEventListener('DOMContentLoaded', function() {
    console.log('Initialisation de gestion_utilisateurs.js');
    const token = localStorage.getItem('token');
    console.log('Token récupéré de localStorage:', token);
    if (!token) {
        console.error('Aucun token trouvé dans localStorage');
        alert('Veuillez vous connecter en tant qu’administrateur');
        window.location.href = '/login.html';
        return;
    }

    const userModal = document.getElementById('user-modal');
    const userModalTitle = document.getElementById('user-modal-title');
    const userForm = document.getElementById('user-form');
    const userIdInput = document.getElementById('user-id');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const roleSelect = document.getElementById('role');
    const addUserBtn = document.getElementById('add-user-btn');
    const userModalClose = document.getElementById('user-modal-close');

    loadUsers();

    addUserBtn.addEventListener('click', () => {
        userModalTitle.textContent = 'Ajouter un utilisateur';
        userIdInput.value = '';
        usernameInput.value = '';
        passwordInput.value = '';
        roleSelect.value = '';
        userModal.classList.remove('hidden');
    });

    userModalClose.addEventListener('click', () => {
        userModal.classList.add('hidden');
        userForm.reset();
    });

    userForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const id = userIdInput.value;
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        const role = roleSelect.value;

        if (!username || !role) {
            alert('Veuillez remplir tous les champs requis (nom d’utilisateur, rôle)');
            return;
        }
        if (id && isNaN(id)) {
            console.error('ID utilisateur invalide:', id);
            alert('Erreur : ID utilisateur invalide');
            return;
        }

        const data = { username, role };
        if (password) data.password = password;

        try {
            const url = id ? `http://192.168.1.13:5000/users/${id}` : 'http://192.168.1.13:5000/users';
            const method = id ? 'PUT' : 'POST';
            console.log(`Envoi requête ${method} à ${url} avec données:`, data);
            console.log('En-tête Authorization:', `Bearer ${token}`);

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert(id ? 'Utilisateur modifié avec succès' : 'Utilisateur ajouté avec succès');
                userModal.classList.add('hidden');
                userForm.reset();
                loadUsers();
            } else {
                const error = await response.json();
                console.error('Erreur:', error);
                alert(`Erreur : ${error.error}`);
                if (response.status === 401) {
                    alert('Session expirée. Veuillez vous reconnecter.');
                    window.location.href = '/login.html';
                }
            }
        } catch (error) {
            console.error('Erreur lors de la requête:', error);
            alert('Erreur serveur lors de l’opération');
        }
    });

    document.getElementById('user-list').addEventListener('click', async function(event) {
        if (event.target.classList.contains('edit-btn')) {
            const id = event.target.getAttribute('data-id');
            if (!id || isNaN(id)) {
                console.error('ID utilisateur manquant ou invalide pour modification:', id);
                alert('Erreur : ID utilisateur non défini ou invalide');
                return;
            }

            try {
                console.log('Récupération utilisateur ID:', id);
                console.log('En-tête Authorization:', `Bearer ${token}`);
                const response = await fetch(`http://192.168.1.13:5000/users/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const user = await response.json();
                    console.log('Utilisateur récupéré pour modification:', user);
                    userModalTitle.textContent = 'Modifier un utilisateur';
                    userIdInput.value = user.id;
                    usernameInput.value = user.username;
                    passwordInput.value = '';
                    roleSelect.value = user.role;
                    userModal.classList.remove('hidden');
                } else {
                    const error = await response.json();
                    console.error('Erreur:', error);
                    alert(`Erreur : ${error.error}`);
                }
            } catch (error) {
                console.error('Erreur lors de la récupération de l’utilisateur:', error);
                alert('Erreur serveur lors de la récupération de l’utilisateur');
            }
        }

        if (event.target.classList.contains('delete-btn')) {
            const id = event.target.getAttribute('data-id');
            if (!id || isNaN(id)) {
                console.error('ID utilisateur manquant ou invalide pour suppression:', id);
                alert('Erreur : ID utilisateur non défini ou invalide');
                return;
            }

            if (confirm('Voulez-vous vraiment supprimer cet utilisateur ?')) {
                try {
                    console.log('Suppression utilisateur ID:', id);
                    console.log('En-tête Authorization:', `Bearer ${token}`);
                    const response = await fetch(`http://192.168.1.13:5000/users/${id}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        alert('Utilisateur supprimé avec succès');
                        loadUsers();
                    } else {
                        const error = await response.json();
                        console.error('Erreur:', error);
                        alert(`Erreur : ${error.error}`);
                    }
                } catch (error) {
                    console.error('Erreur lors de la suppression:', error);
                    alert('Erreur serveur lors de la suppression');
                }
            }
        }
    });

    async function loadUsers() {
        try {
            console.log('Chargement des utilisateurs, Authorization:', `Bearer ${token}`);
            const response = await fetch('http://192.168.1.13:5000/users', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            console.log('Réponse fetch /users:', response.status, response.statusText);
            if (response.ok) {
                const users = await response.json();
                console.log('Utilisateurs reçus:', users);
                const userList = document.getElementById('user-list');
                userList.innerHTML = '';

                if (users.length === 0) {
                    userList.innerHTML = '<tr><td colspan="4" class="px-4 py-2 text-center">Aucun utilisateur trouvé</td></tr>';
                    return;
                }

                users.forEach(user => {
                    if (!user.id) {
                        console.warn('Utilisateur sans ID:', user);
                        return;
                    }
                    userList.innerHTML += `
                        <tr>
                            <td class="px-4 py-2">${user.id}</td>
                            <td class="px-4 py-2">${user.username}</td>
                            <td class="px-4 py-2">${user.role}</td>
                            <td class="px-4 py-2">
                                <button class="edit-btn bg-gray-600 text-white p-1 rounded hover:bg-gray-700" data-id="${user.id}">Modifier</button>
                                <button class="delete-btn bg-red-600 text-white p-1 rounded hover:bg-red-700" data-id="${user.id}">Supprimer</button>
                            </td>
                        </tr>
                    `;
                });
            } else {
                const error = await response.json();
                console.error('Erreur lors du chargement des utilisateurs:', error);
                document.getElementById('user-list').innerHTML = '<tr><td colspan="4" class="px-4 py-2 text-center">Erreur lors du chargement des utilisateurs</td></tr>';
                if (response.status === 401) {
                    alert('Session expirée. Veuillez vous reconnecter.');
                    window.location.href = '/login.html';
                }
            }
        } catch (error) {
            console.error('Erreur serveur lors du chargement des utilisateurs:', error);
            document.getElementById('user-list').innerHTML = '<tr><td colspan="4" class="px-4 py-2 text-center">Erreur serveur</td></tr>';
        }
    }
});