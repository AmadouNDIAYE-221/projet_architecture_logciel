document.addEventListener('DOMContentLoaded', () => {
        console.log('Initialisation de navigation.js');
        const navContainer = document.getElementById('nav-container');
        const role = localStorage.getItem('role') || 'visiteur';

        const navItems = [
            { role: 'administrateur', text: 'Tableau de bord', href: 'dashboard.html' },
            { role: 'administrateur', text: 'Gestion des utilisateurs', href: 'gestion_utilisateurs.html' },
            { role: 'administrateur', text: 'Gestion des Jetons', href: 'gestion_jetons.html' },
            { role: 'administrateur', text: 'Gestion des articles', href: 'gestion_articles.html' },
            { role: 'administrateur', text: 'Retour à la page principale', href: 'index.html' },
            { role: 'administrateur', text: 'Déconnexion', href: '#', class: 'text-red-600', isLogout: true, action: () => {
                console.log('Déconnexion : suppression de token et role');
                localStorage.removeItem('token');
                localStorage.removeItem('role');
                console.log('Redirection vers login.html');
                window.location.href = 'login.html';
            }},
            { role: 'editeur', text: 'Gestion des articles', href: 'gestion_articles.html' },
            { role: 'editeur', text: 'Retour à la page principale', href: 'index.html' },
            { role: 'editeur', text: 'Déconnexion', href: '#', class: 'text-red-600', isLogout: true, action: () => {
                console.log('Déconnexion : suppression de token et role');
                localStorage.removeItem('token');
                localStorage.removeItem('role');
                console.log('Redirection vers login.html');
                window.location.href = 'login.html';
            }},
            { role: 'visiteur', text: 'Accueil', href: 'index.html' },
            { role: 'visiteur', text: 'Se connecter', href: 'login.html' }
        ];

        const nav = document.createElement('nav');
        nav.className = 'fixed top-0 left-0 w-full z-50 bg-white text-black shadow-md';

        const container = document.createElement('div');
        container.className = 'max-w-7xl mx-auto px-4 py-3 flex justify-between items-center';

        const ul = document.createElement('ul');
        ul.className = 'flex space-x-6';

        const rightDiv = document.createElement('div');
        rightDiv.className = 'flex items-center';

        navItems.forEach(item => {
            if (!item.role || item.role === role) {
                const a = document.createElement('a');
                a.textContent = item.text;
                a.href = item.href || '#';
                a.className = `px-4 py-2 hover:underline ${item.class || 'text-blue-600'} font-medium`;

                if (item.action) {
                    a.addEventListener('click', (e) => {
                        e.preventDefault();
                        item.action();
                    });
                }

                if (item.isLogout) {
                    rightDiv.appendChild(a);
                } else {
                    const li = document.createElement('li');
                    li.appendChild(a);
                    ul.appendChild(li);
                }
            }
        });

        container.appendChild(ul);
        container.appendChild(rightDiv);
        nav.appendChild(container);
        navContainer.innerHTML = '';
        navContainer.appendChild(nav);
    });