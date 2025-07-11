document.getElementById('loginForm').addEventListener('submit', (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
        .then(response => {
            if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('role', data.role);
                window.location.href = 'index.html';
            } else {
                document.getElementById('authResult').innerHTML = 'Identifiants incorrects';
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            document.getElementById('authResult').innerHTML = 'Erreur lors de la connexion';
        });
});