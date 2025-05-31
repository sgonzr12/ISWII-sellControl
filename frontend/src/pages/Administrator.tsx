import './Administrator.css';
import { useState, useEffect } from 'react';

const ROLES: { [key: string]: number } = {
  Ninguno: 0,
  Administrador: 1,
  Manager: 2,
  Comercial: 3,
  "Jefe de almacen": 4,
};

const ROLE_NAMES: { [key: number]: string } = Object.fromEntries(
  Object.entries(ROLES).map(([name, num]) => [num, name])
);

function Administrator() {
  const [users, setUsers] = useState<{ employe_id: string; name: string; family_name: string; email: string; rol: number }[]>([]);
  const [selectedUser, setSelectedUser] = useState<{ employe_id: string; name: string; family_name: string; email: string; rol: number } | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editRol, setEditRol] = useState('');
  const [search, setSearch] = useState('');

  const fetchUsers = async () => {
    try {
      const credential = localStorage.getItem('credential');
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/user/users`, {
        headers: {
          Authorization: `Bearer ${credential}`,
        },
      });
      if (!response.ok) {
        throw new Error('Error fetching users.');
      }
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSelectUser = (user: { employe_id: string; name: string; family_name: string; email: string; rol: number }) => {
    setSelectedUser(user);
  };

  const handleEditClick = () => {
    if (selectedUser) {
      setEditRol(selectedUser.rol.toString());
    }
    setIsModalOpen(true);
  };

  const handleSave = async () => {
    if (!selectedUser) return;
    try {
      const credential = localStorage.getItem('credential');
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/user/update`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${credential}`,
        },
        body: JSON.stringify({
          employe_id: selectedUser.employe_id,
          rol: editRol,
        }),
      });
      if (!response.ok) {
        throw new Error('Error updating role');
      }
      setIsModalOpen(false);
      fetchUsers();
    } catch (error) {
      console.error('Error updating user:', error);
      alert('No se pudo actualizar el usuario');
    }
  };

  // Filtrado y ordenación alfabética por nombre
  const filteredUsers = users
    .filter(user => user.name.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className="Administrator">
      <main className="main-content">
        <div className="administrator">
          <h1>Panel de administración</h1>
          <div style={{ marginBottom: '1rem', textAlign: 'center' }}>
            <input
              type="text"
              placeholder="Buscar por nombre..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{ padding: '0.5rem', width: '250px' }}
            />
          </div>
          <div className="admin-table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Rol</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map(user => (
                  <tr
                    key={user.employe_id}
                    className={selectedUser?.employe_id === user.employe_id ? 'selected' : ''}
                    onClick={() => handleSelectUser(user)}
                    style={{ cursor: 'pointer' }}
                  >
                    <td>{user.name}</td>
                    <td>{ROLE_NAMES[user.rol] ?? user.rol}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button
            className="edit-btn"
            onClick={handleEditClick}
            disabled={!selectedUser}
          >
            Editar rol
          </button>
        </div>
        {isModalOpen && (
          <div className="modal-backdrop">
            <div className="modal">
              <h2>Cambiar rol</h2>
              <select
                value={editRol}
                onChange={e => setEditRol(e.target.value)}
              >
                {Object.entries(ROLES).map(([name, num]) => (
                  <option key={num} value={num}>
                    {name}
                  </option>
                ))}
              </select>
              <div className="modal-actions">
                <button onClick={handleSave}>Guardar</button>
                <button onClick={() => setIsModalOpen(false)}>Cancelar</button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Administrator;