document.addEventListener('DOMContentLoaded', () => {
    console.log('Chargement du tableau de bord...');
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    const authSection = document.getElementById('auth-section');

    if (token && role === 'admin') {
        console.log(`Utilisateur connecté : rôle ${role}`);
        authSection.innerHTML = `Connecté en tant que ${role} | <a href="#" id="logout" class="text-blue-600">Déconnexion</a>`;
        document.getElementById('logout').addEventListener('click', () => {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            window.location.href = 'login.html';
        });
    } else {
        console.log('Aucun utilisateur connecté ou rôle non autorisé');
        window.location.href = 'login.html';
    }
});