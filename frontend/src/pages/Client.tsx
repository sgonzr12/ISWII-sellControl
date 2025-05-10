import { useState, useEffect } from 'react';
import './Client.css';

interface Client {
  id: string;
  name: string;
  email: string;
  date: string; // Fecha de alta o similar
}

function ClientTable() {
  const [clients, setClients] = useState<Client[]>([]);
  const [filteredClients, setFilteredClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editName, setEditName] = useState('');
  const [editEmail, setEditEmail] = useState('');
  const [editDate, setEditDate] = useState('');

  // Simulación de fetch de clientes
  useEffect(() => {
    const mockClients: Client[] = [
      { id: '1', name: 'Cliente 1', email: 'cliente1@email.com', date: '2024-05-01' },
      { id: '2', name: 'Cliente 2', email: 'cliente2@email.com', date: '2024-05-05' },
      { id: '3', name: 'Cliente 3', email: 'cliente3@email.com', date: '2024-05-10' },
    ];
    setClients(mockClients);
    setFilteredClients(mockClients);
  }, []);


  const handleCreate = () => {
    setSelectedClient(null);
    setEditName('');
    setEditEmail('');
    setEditDate('');
    setIsModalOpen(true);
  };

  const handleEdit = () => {
    if (selectedClient) {
      setEditName(selectedClient.name);
      setEditEmail(selectedClient.email);
      setEditDate(selectedClient.date);
      setIsModalOpen(true);
    }
  };

  const handleDelete = () => {
    if (selectedClient) {
      setClients(clients.filter(c => c.id !== selectedClient.id));
      setSelectedClient(null);
    }
  };

  const handleSave = () => {
    if (selectedClient) {
      setClients(clients.map(c =>
        c.id === selectedClient.id
          ? { ...c, name: editName, email: editEmail, date: editDate }
          : c
      ));
    } else {
      const newClient: Client = {
        id: Date.now().toString(),
        name: editName,
        email: editEmail,
        date: editDate,
      };
      setClients([...clients, newClient]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="Client">
      <main className="main-content">
        <div className="client-content">
        <h1 className="client-title">Tabla de Clientes</h1>
          <table className="client-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Email</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {filteredClients.map(client => (
                <tr
                  key={client.id}
                  className={selectedClient?.id === client.id ? 'selected' : ''}
                  onClick={() => setSelectedClient(client)}
                  style={{ cursor: 'pointer' }}
                >
                  <td>{client.name}</td>
                  <td>{client.email}</td>
                  <td>{client.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="client-actions">
            <button onClick={handleCreate}>Crear cliente</button>
            <button onClick={handleEdit} disabled={!selectedClient}>Editar cliente</button>
            <button onClick={handleDelete} disabled={!selectedClient}>Eliminar cliente</button>
          </div>
        </div>
        {isModalOpen && (
          <div className="modal-backdrop">
            <div className="modal">
              <h2>{selectedClient ? 'Editar cliente' : 'Crear cliente'}</h2>
              <label>
                Nombre:
                <input type="text" value={editName} onChange={e => setEditName(e.target.value)} />
              </label>
              <label>
                Email:
                <input type="email" value={editEmail} onChange={e => setEditEmail(e.target.value)} />
              </label>
              <label>
                Fecha:
                <input type="date" value={editDate} onChange={e => setEditDate(e.target.value)} />
              </label>
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

export default ClientTable;