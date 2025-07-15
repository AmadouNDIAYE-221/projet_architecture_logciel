document.addEventListener('DOMContentLoaded', function() {
    console.log('Initialisation de gestion_jetons.js');
    const token = localStorage.getItem('token');
    console.log('Token récupéré de localStorage:', token);
    if (!token) {
        console.error('Aucun token trouvé dans localStorage');
        alert('Veuillez vous connecter en tant qu’administrateur');
        window.location.href = '/login.html';
        return;
    }
    loadTokens();
    loadUsers();

    const generateModal = document.getElementById('generate-modal');
    const deleteModal = document.getElementById('delete-modal');
    const openGenerateModal = document.getElementById('open-generate-modal');
    const openDeleteModal = document.getElementById('open-delete-modal');
    const cancelGenerate = document.getElementById('cancel-generate');
    const cancelDelete = document.getElementById('cancel-delete');

    openGenerateModal.addEventListener('click', () => {
        generateModal.classList.remove('hidden');
    });

    openDeleteModal.addEventListener('click', () => {
        deleteModal.classList.remove('hidden');
    });

    cancelGenerate.addEventListener('click', () => {
        generateModal.classList.add('hidden');
        document.getElementById('generate-username').value = '';
    });

    cancelDelete.addEventListener('click', () => {
        deleteModal.classList.add('hidden');
        document.getElementById('delete-token-id').value = '';
    });

    async function loadUsers() {
        try {
            console.log('Chargement des utilisateurs, Authorization:', `Bearer ${token}`);
            const response = await fetch('http://192.168.1.13:5000/users', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            console.log('Réponse fetch /users:', response.status, response.statusText);
            if (response.ok) {
                const users = await response.json();
                console.log('Utilisateurs reçus:', users);
                const userSelect = document.getElementById('generate-username');
                userSelect.innerHTML = '<option value="" disabled selected>Sélectionnez un utilisateur</option>';
                if (!users || users.length === 0) {
                    console.warn('Aucun utilisateur renvoyé par /users');
                    userSelect.innerHTML += '<option value="" disabled>Aucun utilisateur trouvé</option>';
                } else {
                    users.forEach(user => {
                        userSelect.innerHTML += `<option value="${user.username}">${user.username} (${user.role})</option>`;
                    });
                }
            } else {
                const error = await response.json();
                console.error('Erreur lors du chargement des utilisateurs:', error);
                alert(`Erreur : ${error.error || 'Impossible de charger les utilisateurs'}`);
                if (response.status === 401) {
                    alert('Session expirée. Veuillez vous reconnecter.');
                    window.location.href = '/login.html';
                }
            }
        } catch (error) {
            console.error('Erreur serveur lors du chargement des utilisateurs:', error);
            alert('Erreur serveur lors du chargement des utilisateurs. Vérifiez la connexion au serveur.');
        }
    }

    const generateTokenForm = document.getElementById('generate-token-form');
    if (generateTokenForm) {
        generateTokenForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const username = document.getElementById('generate-username').value;
            if (!username) {
                alert('Veuillez sélectionner un utilisateur');
                return;
            }

            try {
                console.log('Génération jeton pour username:', username);
                console.log('En-tête Authorization:', `Bearer ${token}`);
                const response = await fetch('http://192.168.1.13:5000/tokens/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ username })
                });

                if (response.ok) {
                    alert('Jeton généré avec succès');
                    document.getElementById('generate-username').value = '';
                    generateModal.classList.add('hidden');
                    loadTokens();
                } else {
                    const error = await response.json();
                    console.error('Erreur:', error);
                    alert(`Erreur : ${error.error}`);
                }
            } catch (error) {
                console.error('Erreur lors de la génération du jeton:', error);
                alert('Erreur serveur lors de la génération du jeton');
            }
        });
    }

    const deleteTokenForm = document.getElementById('delete-token-form');
    if (deleteTokenForm) {
        deleteTokenForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const tokenId = document.getElementById('delete-token-id').value.trim();
            if (!tokenId) {
                alert('Veuillez entrer un ID de jeton');
                return;
            }

            try {
                console.log('Suppression jeton ID:', tokenId);
                console.log('En-tête Authorization:', `Bearer ${token}`);
                const response = await fetch(`http://192.168.1.13:5000/tokens/${tokenId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    alert('Jeton supprimé avec succès');
                    document.getElementById('delete-token-id').value = '';
                    deleteModal.classList.add('hidden');
                    loadTokens();
                } else {
                    const error = await response.json();
                    console.error('Erreur:', error);
                    alert(`Erreur : ${error.error}`);
                }
            } catch (error) {
                console.error('Erreur lors de la suppression du jeton:', error);
                alert('Erreur serveur lors de la suppression du jeton');
            }
        });
    }

    document.getElementById('token-list').addEventListener('click', async function(event) {
        if (event.target.classList.contains('delete-btn')) {
            const tokenId = event.target.getAttribute('data-id');
            if (confirm('Voulez-vous vraiment supprimer ce jeton ?')) {
                try {
                    console.log('Suppression jeton ID:', tokenId);
                    console.log('En-tête Authorization:', `Bearer ${token}`);
                    const response = await fetch(`http://192.168.1.13:5000/tokens/${tokenId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        alert('Jeton supprimé avec succès');
                        loadTokens();
                    } else {
                        const error = await response.json();
                        console.error('Erreur:', error);
                        alert(`Erreur : ${error.error}`);
                    }
                } catch (error) {
                    console.error('Erreur lors de la suppression du jeton:', error);
                    alert('Erreur serveur lors de la suppression du jeton');
                }
            }
        }
    });

    async function loadTokens() {
        try {
            console.log('Chargement des jetons, Authorization:', `Bearer ${token}`);
            const response = await fetch('http://192.168.1.13:5000/tokens', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            console.log('Réponse fetch /tokens:', response.status, response.statusText);
            if (response.ok) {
                const tokens = await response.json();
                console.log('Jetons reçus:', tokens);
                const tokenList = document.getElementById('token-list');
                tokenList.innerHTML = '';

                if (tokens.length === 0) {
                    tokenList.innerHTML = '<tr><td colspan="6" class="px-4 py-2 text-center">Aucun jeton trouvé</td></tr>';
                    return;
                }

                tokens.forEach(t => {
                    const tokenPreview = t.token ? `${t.token.substring(0, 15)}...` : 'N/A';
                    tokenList.innerHTML += `
                        <tr>
                            <td class="px-4 py-2">${t.token_id}</td>
                            <td class="px-4 py-2">${t.username}</td>
                            <td class="px-4 py-2">${t.role}</td>
                            <td class="px-4 py-2">${tokenPreview}</td>
                            <td class="px-4 py-2">${t.created_at}</td>
                            <td class="px-4 py-2">
                                <button data-id="${t.token_id}" class="delete-btn bg-red-600 text-white p-2 rounded hover:bg-red-700">Supprimer</button>
                            </td>
                        </tr>
                    `;
                });
            } else {
                const error = await response.json();
                console.error('Erreur lors du chargement des jetons:', error);
                document.getElementById('token-list').innerHTML = '<tr><td colspan="6" class="px-4 py-2 text-center">Erreur lors du chargement des jetons</td></tr>';
                if (response.status === 401) {
                    alert('Session expirée. Veuillez vous reconnecter.');
                    window.location.href = '/login.html';
                }
            }
        } catch (error) {
            console.error('Erreur serveur lors du chargement des jetons:', error);
            document.getElementById('token-list').innerHTML = '<tr><td colspan="6" class="px-4 py-2 text-center">Erreur serveur</td></tr>';
        }
    }
});