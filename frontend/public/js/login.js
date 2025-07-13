document.getElementById('login-form').addEventListener('submit', async (e) => {
         e.preventDefault();
         const username = document.getElementById('username').value;
         const password = document.getElementById('password').value;
         console.log('Tentative de connexion :', username);
     
         try {
             const response = await fetch('http://192.168.1.13:5000/login', {
                 method: 'POST',
                 headers: {
                     'Content-Type': 'application/json'
                 },
                 body: JSON.stringify({ username, password })
             });
             console.log('Réponse login', response.status);
             const data = await response.json();
             if (response.ok) {
                 localStorage.setItem('token', data.token);
                 localStorage.setItem('role', data.role);
                 console.log('Connexion réussie, token:', data.token, 'rôle:', data.role);
                 if (data.role === 'editeur') {
                     window.location.href = '/gestion_articles.html';
                 } else if (data.role === 'administrateur') {
                     window.location.href = '/dashboard.html';
                 } else {
                     console.error('Rôle non autorisé pour cette interface:', data.role);
                     alert('Rôle non autorisé');
                 }
             } else {
                 console.error('Erreur de connexion :', data.error);
                 alert(data.error);
             }
         } catch (error) {
             console.error('Erreur de connexion :', error);
             alert('Erreur de connexion');
         }
     });