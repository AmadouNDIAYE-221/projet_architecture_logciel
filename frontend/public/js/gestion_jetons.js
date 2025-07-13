document.addEventListener('DOMContentLoaded', () => {
  const tokenList = document.getElementById('token-list');
  const deleteForm = document.getElementById('delete-token-form');
  const deleteInput = document.getElementById('delete-token-id');
  const BASE_URL = 'http://localhost:5000';
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  // Afficher la nav si connecté
  if (role) {
    document.getElementById('nav-container').style.display = 'block';
  }

  if (!token) {
    alert('Vous devez être connecté pour accéder à cette page.');
    window.location.href = 'login.html';
    return;
  }

  async function loadTokens() {
    try {
      const res = await fetch(`${BASE_URL}/tokens`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!res.ok) throw new Error('Erreur lors du chargement des jetons');
      const tokens = await res.json();

      if (tokens.length === 0) {
        tokenList.innerHTML = `<tr><td colspan="5" class="text-center text-gray-500 p-2">Aucun jeton trouvé</td></tr>`;
        return;
      }

      tokenList.innerHTML = '';
      tokens.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="p-2 border">${t.token_id}</td>
          <td class="p-2 border">${t.username}</td>
          <td class="p-2 border">${t.role}</td>
          <td class="p-2 border">${t.token}</td>
          
          <td class="p-2 border">${new Date(t.created_at).toLocaleString()}</td>
          <td class="p-2 border">
            <button data-id="${t.token_id}" class="delete-btn bg-red-600 text-white p-1 rounded hover:bg-red-700">Supprimer</button>
          </td>
        `;
        tokenList.appendChild(tr);
      });

      // Gestion suppression depuis bouton de tableau
      document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = btn.dataset.id;
          if (confirm(`Supprimer le jeton ID ${id} ?`)) {
            deleteToken(id);
          }
        });
      });

    } catch (err) {
      tokenList.innerHTML = `<tr><td colspan="5" class="text-center text-red-600 p-2">${err.message}</td></tr>`;
    }
  }

  async function deleteToken(id) {
    try {
      const res = await fetch(`${BASE_URL}/tokens/${encodeURIComponent(id)}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Erreur lors de la suppression');
      alert(`Jeton ${id} supprimé`);
      loadTokens();
    } catch (err) {
      alert(err.message);
    }
  }

  // Suppression via formulaire
  deleteForm.addEventListener('submit', e => {
    e.preventDefault();
    const id = deleteInput.value.trim();
    if (!id) {
      alert('Veuillez entrer un ID valide');
      return;
    }
    if (confirm(`Supprimer le jeton ID ${id} ?`)) {
      deleteToken(id);
      deleteInput.value = '';
    }
  });

  loadTokens();
});
