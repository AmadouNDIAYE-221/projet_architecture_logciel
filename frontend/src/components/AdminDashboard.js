// frontend/src/components/AdminDashboard.js
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token'); // Assure-toi que le token est stocké après login
    fetch('http://localhost:5000/api/users', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        const userTable = document.getElementById('userTableBody');
        if (data.length === 0) {
            userTable.innerHTML = '<tr><td colspan="4">Aucun utilisateur trouvé</td></tr>';
        } else {
            userTable.innerHTML = data.map(user => `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.role}</td>
                    <td>
                        <button onclick="deleteUser('${user.id}')">Supprimer</button>
                    </td>
                </tr>
            `).join('');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        userTable.innerHTML = '<tr><td colspan="4">Erreur lors du chargement des utilisateurs</td></tr>';
    });
});

function deleteUser(userId) {
    const token = localStorage.getItem('token');
    fetch(`http://localhost:5000/api/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Utilisateur supprimé');
            location.reload();
        } else {
            alert('Erreur lors de la suppression');
        }
    })
    .catch(error => console.error('Erreur:', error));
}// Composant pour le tableau de bord des administrateurs 
