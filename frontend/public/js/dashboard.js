document.addEventListener('DOMContentLoaded', () => {
    console.log('Initialisation de dashboard.js');
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    const authSection = document.getElementById('auth-section');

    if (!token || role !== 'administrateur') {
        console.log('Aucun utilisateur connecté ou rôle non autorisé, redirection vers /index.html');
        window.location.replace('/index.html');
        return;
    }

    console.log(`Utilisateur connecté : rôle ${role}`);
    authSection.innerHTML = `<a href="#" onclick="logout()" class="text-red-600  font-semibold hover:text-red-700 hover:underline">Déconnexion</a>`;
});

function logout() {
    console.log('Déconnexion depuis dashboard');
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.replace('/index.html');
}