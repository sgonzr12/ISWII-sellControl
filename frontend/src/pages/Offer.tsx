import { useState, useEffect } from 'react';
import './Offer.css';

interface Offer {
  id: string;
  name: string;
  price: number;
  date: string; // formato ISO: "2024-05-10"
}

function OfferTable() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [filteredOffers, setFilteredOffers] = useState<Offer[]>([]);
  const [selectedOffer, setSelectedOffer] = useState<Offer | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editName, setEditName] = useState('');
  const [editPrice, setEditPrice] = useState('');
  const [editDate, setEditDate] = useState('');
  const [filterStart, setFilterStart] = useState('');
  const [filterEnd, setFilterEnd] = useState('');

  // Simulación de fetch de ofertas
  useEffect(() => {
    // Aquí deberías hacer fetch a tu backend
    const mockOffers: Offer[] = [
      { id: '1', name: 'Oferta 1', price: 100, date: '2024-05-01' },
      { id: '2', name: 'Oferta 2', price: 200, date: '2024-05-05' },
      { id: '3', name: 'Oferta 3', price: 150, date: '2024-05-10' },
    ];
    setOffers(mockOffers);
    setFilteredOffers(mockOffers);
  }, []);

  // Filtrado por fecha
  useEffect(() => {
    let filtered = offers;
    if (filterStart) {
      filtered = filtered.filter(o => o.date >= filterStart);
    }
    if (filterEnd) {
      filtered = filtered.filter(o => o.date <= filterEnd);
    }
    setFilteredOffers(filtered);
  }, [filterStart, filterEnd, offers]);

  const handleCreate = () => {
    setSelectedOffer(null);
    setEditName('');
    setEditPrice('');
    setEditDate('');
    setIsModalOpen(true);
  };

  const handleEdit = () => {
    if (selectedOffer) {
      setEditName(selectedOffer.name);
      setEditPrice(selectedOffer.price.toString());
      setEditDate(selectedOffer.date);
      setIsModalOpen(true);
    }
  };

  const handleDelete = () => {
    if (selectedOffer) {
      // Aquí deberías hacer un fetch DELETE al backend
      setOffers(offers.filter(o => o.id !== selectedOffer.id));
      setSelectedOffer(null);
    }
  };

  const handleSave = () => {
    if (selectedOffer) {
      // Editar oferta existente
      setOffers(offers.map(o =>
        o.id === selectedOffer.id
          ? { ...o, name: editName, price: Number(editPrice), date: editDate }
          : o
      ));
    } else {
      // Crear nueva oferta
      const newOffer: Offer = {
        id: Date.now().toString(),
        name: editName,
        price: Number(editPrice),
        date: editDate,
      };
      setOffers([...offers, newOffer]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="OfferTable">
      <h1>Tabla de Ofertas</h1>
      <div style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <label>
          Fecha inicial:
          <input type="date" value={filterStart} onChange={e => setFilterStart(e.target.value)} />
        </label>
        <label>
          Fecha final:
          <input type="date" value={filterEnd} onChange={e => setFilterEnd(e.target.value)} />
        </label>
      </div>
      <table className="offer-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {filteredOffers.map(offer => (
            <tr
              key={offer.id}
              className={selectedOffer?.id === offer.id ? 'selected' : ''}
              onClick={() => setSelectedOffer(offer)}
              style={{ cursor: 'pointer' }}
            >
              <td>{offer.name}</td>
              <td>{offer.price}</td>
              <td>{offer.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '1rem' }}>
        <button onClick={handleCreate}>Crear oferta</button>
        <button onClick={handleEdit} disabled={!selectedOffer}>Editar oferta</button>
        <button onClick={handleDelete} disabled={!selectedOffer}>Eliminar oferta</button>
      </div>
      {isModalOpen && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>{selectedOffer ? 'Editar oferta' : 'Crear oferta'}</h2>
            <label>
              Nombre:
              <input type="text" value={editName} onChange={e => setEditName(e.target.value)} />
            </label>
            <label>
              Precio:
              <input type="number" value={editPrice} onChange={e => setEditPrice(e.target.value)} />
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
    </div>
  );
}

export default OfferTable;