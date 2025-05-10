import { useState, useEffect } from 'react';
import './Client.css';

interface Client {
  clientID: string;
  CompanyName: string;
  CIF: string;
  address: string;
  email: string;
  phone: string;
  contact: string;
}

function ClientTable() {
  const [clients, setClients] = useState<Client[]>([]);
  const [filteredClients, setFilteredClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Campos para crear/editar
  const [editCompanyName, setEditCompanyName] = useState('');
  const [editCIF, setEditCIF] = useState('');
  const [editAddress, setEditAddress] = useState('');
  const [editEmail, setEditEmail] = useState('');
  const [editPhone, setEditPhone] = useState('');
  const [editContact, setEditContact] = useState('');

  // Filtros
  const [filterCompanyName, setFilterCompanyName] = useState('');

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/client/`, {
          headers: {
            Authorization: `Bearer ${credential}`,
          },
        });
        if (!response.ok) {
          throw new Error('Error al obtener los clientes');
        }
        const data = await response.json();
        setClients(data);
        setFilteredClients(data);
      } catch (error) {
        console.error('Error fetching clients:', error);
      }
    };
    fetchClients();
  }, []);

  useEffect(() => {
    let filtered = clients;
    if (filterCompanyName) {
      filtered = filtered.filter(c =>
        c.CompanyName.toLowerCase().includes(filterCompanyName.toLowerCase())
      );
    }
    setFilteredClients(filtered);
  }, [filterCompanyName, clients]);

  const handleCreate = () => {
    setSelectedClient(null);
    setEditCompanyName('');
    setEditCIF('');
    setEditAddress('');
    setEditEmail('');
    setEditPhone('');
    setEditContact('');
    setIsModalOpen(true);
  };

  const handleEdit = () => {
    if (selectedClient) {
      setEditCompanyName(selectedClient.CompanyName);
      setEditCIF(selectedClient.CIF);
      setEditAddress(selectedClient.address);
      setEditEmail(selectedClient.email);
      setEditPhone(selectedClient.phone);
      setEditContact(selectedClient.contact);
      setIsModalOpen(true);
    }
  };

  // const handleDelete = async () => {
  //   if (selectedClient) {
  //     try {
  //       const credential = localStorage.getItem('credential');
  //       const response = await fetch(
  //         `${import.meta.env.VITE_BACKEND_URL}/client/${selectedClient.clientID}`,
  //         {
  //           method: 'DELETE',
  //           headers: {
  //             Authorization: `Bearer ${credential}`,
  //           },
  //         }
  //       );
  //       if (!response.ok) {
  //         throw new Error('Error al eliminar el cliente');
  //       }
  //       setClients(clients.filter(c => c.clientID !== selectedClient.clientID));
  //       setFilteredClients(filteredClients.filter(c => c.clientID !== selectedClient.clientID));
  //       setSelectedClient(null);
  //     } catch (error) {
  //       console.error('Error eliminando cliente:', error);
  //       alert('No se pudo eliminar el cliente');
  //     }
  //   }
  // };

  const handleSave = async () => {
    if (
      !editCompanyName ||
      !editCIF ||
      !editAddress ||
      !editEmail ||
      !editPhone ||
      !editContact
    ) {
      alert('Por favor, completa todos los campos.');
      return;
    }

    if (selectedClient) {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/client/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${credential}`,
          },
          body: JSON.stringify({
            clientID: selectedClient.clientID,
            address: editAddress,
            email: editEmail,
            phone: editPhone,
            contact: editContact,
          }),
        });
        if (!response.ok) {
          throw new Error('Error al actualizar el cliente');
        }
        const updatedClient = await response.json();
        setClients(clients.map(c =>
          c.clientID === selectedClient.clientID ? updatedClient : c
        ));
        setFilteredClients(clients.map(c =>
          c.clientID === selectedClient.clientID ? updatedClient : c
        ));
      } catch (error) {
        console.error('Error actualizando cliente:', error);
        alert('No se pudo actualizar el cliente');
      }
    } else {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/client/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${credential}`,
          },
          body: JSON.stringify({
            CompanyName: editCompanyName,
            CIF: editCIF,
            address: editAddress,
            email: editEmail,
            phone: editPhone,
            contact: editContact,
          }),
        });
        if (!response.ok) {
          throw new Error('Error al crear el cliente');
        }
        const newClient = await response.json();
        setClients([...clients, newClient]);
        setFilteredClients([...clients, newClient]);
      } catch (error) {
        console.error('Error creando cliente:', error);
        alert('No se pudo crear el cliente');
      }
    }
    setIsModalOpen(false);
  };

  return (
    <div className="Client">
      <main className="main-content">
        <div className="client-content">
          <h1 className="client-title">Tabla de Clientes</h1>
          <div className="client-filters">
            <label>
              Buscar por empresa: &nbsp;
              <input
                type="text"
                value={filterCompanyName}
                onChange={e => setFilterCompanyName(e.target.value)}
                placeholder="Nombre de empresa"
              />
            </label>
          </div>
          <table className="client-table">
            <thead>
              <tr>
                <th>Empresa</th>
                <th>CIF</th>
                <th>Dirección</th>
                <th>Email</th>
                <th>Teléfono</th>
                <th>Contacto</th>
              </tr>
            </thead>
            <tbody>
              {filteredClients.map(client => (
                <tr
                  key={client.clientID}
                  className={selectedClient?.clientID === client.clientID ? 'selected' : ''}
                  onClick={() => setSelectedClient(client)}
                  style={{ cursor: 'pointer' }}
                >
                  <td>{client.CompanyName}</td>
                  <td>{client.CIF}</td>
                  <td>{client.address}</td>
                  <td>{client.email}</td>
                  <td>{client.phone}</td>
                  <td>{client.contact}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="client-actions">
            <button onClick={handleCreate}>Crear cliente</button>
            <button onClick={handleEdit} disabled={!selectedClient}>Editar cliente</button>
            {/* <button onClick={handleDelete} disabled={!selectedClient}>Eliminar cliente</button> */}
          </div>
        </div>
        {isModalOpen && (
          <div className="modal-backdrop">
            <div className="modal">
              <h2>{selectedClient ? 'Editar cliente' : 'Crear cliente'}</h2>
              {/* Menú de crear: todos los campos editables */}
              {!selectedClient && (
                <>
                  <label>
                    Empresa: &nbsp;
                    <input type="text" value={editCompanyName} onChange={e => setEditCompanyName(e.target.value)} />
                  </label>
                  <label>
                    CIF: &nbsp;
                    <input type="text" value={editCIF} onChange={e => setEditCIF(e.target.value)} />
                  </label>
                  <label>
                    Dirección: &nbsp;
                    <input type="text" value={editAddress} onChange={e => setEditAddress(e.target.value)} />
                  </label>
                  <label>
                    Email: &nbsp;
                    <input type="email" value={editEmail} onChange={e => setEditEmail(e.target.value)} />
                  </label>
                  <label>
                    Teléfono: &nbsp;
                    <input type="text" value={editPhone} onChange={e => setEditPhone(e.target.value)} />
                  </label>
                  <label>
                    Contacto: &nbsp;
                    <input type="text" value={editContact} onChange={e => setEditContact(e.target.value)} />
                  </label>
                </>
              )}
              {/* Menú de editar: solo los campos editables */}
              {selectedClient && (
                <>
                  <label>
                    Dirección: &nbsp;
                    <input type="text" value={editAddress} onChange={e => setEditAddress(e.target.value)} />
                  </label>
                  <label>
                    Email: &nbsp;
                    <input type="email" value={editEmail} onChange={e => setEditEmail(e.target.value)} />
                  </label>
                  <label>
                    Teléfono: &nbsp;
                    <input type="text" value={editPhone} onChange={e => setEditPhone(e.target.value)} />
                  </label>
                  <label>
                    Contacto: &nbsp;
                    <input type="text" value={editContact} onChange={e => setEditContact(e.target.value)} />
                  </label>
                </>
              )}
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