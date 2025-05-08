import './Administrator.css';
import { useState, useEffect} from 'react';

/*
Endpoints: 
get /user/ Información del usuario logueado. Un json con el usuario en cuestión.
get /user/users Información de todos los usuarios. Devuelve un json con todos los usuarios.
put /user/update:id:rol Cambia el rol del usuario. Recibe un json con todos los datos del usuario.
*/

// const mockUsers = [
//   { EmployeID: '100317434052211591144', Name: 'David Fernández Urdiales', Family_name: 'Fernandez Urdiales', Email: 'dfernu00@estudiantes.unileon.es', Rol: 1 },
//   { EmployeID: '100317434052211591145', Name: 'Juan', Family_name: 'Ffff', Email: 'email@email.com', Rol: 2 },
//   { EmployeID: '100317434052211591146', Name: 'Pedro', Family_name: 'sdfdsf', Email: 'email3@email.com', Rol: 3 }
// ];


function Administrator() {
  const [users, setUsers] = useState<{ employe_id: string; name: string; family_name: string; email: string; rol: number }[]>([]);
  //const [users] = useState(mockUsers);
  const [selectedUser, setSelectedUser] = useState<{ employe_id: string; name: string; family_name: string; email: string; rol: number } | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editRol, setEditRol] = useState('');

  const fetchUsers = async () => {
    try {
      const credential = localStorage.getItem('credential');
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/user/users`, {
        headers: {
          Authorization: `Bearer ${credential}`,
        },
      });
      if (!response.ok) {
        throw new Error('Error al obtener los usuarios');
      }
      const data = await response.json();
      console.log('Data from backend:', data);
      setUsers(data); // data debe ser un array de usuarios
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
      setEditRol(selectedUser.rol.toString()); // Asignar el rol actual al campo de edición
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
        throw new Error('Error al actualizar el rol');
      }
      setIsModalOpen(false);
      fetchUsers(); // Recarga la lista de usuarios
    } catch (error) {
      console.error('Error updating user:', error);
      alert('No se pudo actualizar el usuario');
    }
  };

  return (
    <div className="Administrator">
      <main className="main-content">
        <div className="administrator">
          <h1>Panel de administración</h1>
          <ul className="user-list">
            {users.map(user => (
              <li
                key={user.employe_id}
                className={selectedUser?.employe_id === user.employe_id ? 'selected' : ''}
                onClick={() => handleSelectUser(user)}
              >
                {user.name} ({user.rol})
              </li>
            ))}
          </ul>
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
              <label>
                Rol: &nbsp;
              </label>
              <input
                  type="text"
                  value={editRol}
                  onChange={e => setEditRol(e.target.value)}
                />
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