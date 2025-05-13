import { useState, useEffect } from 'react';
import './Offer.css';

interface Product {
  name: string;
  id: string;
  quantity: string;
}

interface Offer {
  offerID: number;
  employeId: string;
  employeName: string;
  clientId: string;
  clientName: string;
  date: string;
  totalPrize: string;
  products: Product[];
}

function OfferTable() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [filteredOffers, setFilteredOffers] = useState<Offer[]>([]);
  const [selectedOffer, setSelectedOffer] = useState<Offer | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editEmployeName, setEditEmployeName] = useState('');
  const [editClientName, setEditClientName] = useState('');
  const [editTotalPrize, setEditTotalPrize] = useState('');
  const [editDate, setEditDate] = useState('');
  const [filterStart, setFilterStart] = useState('');
  const [filterEnd, setFilterEnd] = useState('');
  const [isProductsModalOpen, setIsProductsModalOpen] = useState(false);
  const [productsToShow, setProductsToShow] = useState<Product[]>([]);

  // Simulación de fetch de ofertas
  useEffect(() => {
    const mockOffers: Offer[] = [
      {
        offerID: 1234156,
        employeId: "employee_id_placeholder",
        employeName: "Juan",
        clientId: "client_id_placeholder",
        clientName: "Pedro",
        date: "2023-10-01",
        totalPrize: "1000",
        products: [
          {
            name: "Laptop",
            id: "product_id_placeholder",
            quantity: "1"
          }
        ]
      },
      {
        offerID: 1234157,
        employeId: "employee_id_placeholder2",
        employeName: "Ana",
        clientId: "client_id_placeholder2",
        clientName: "Maria",
        date: "2023-10-10",
        totalPrize: "1500",
        products: [
          { name: "Tablet", id: "product_id_2", quantity: "2" },
          { name: "Ratón", id: "product_id_3", quantity: "3" }
        ]
      }
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
    setEditEmployeName('');
    setEditClientName('');
    setEditTotalPrize('');
    setEditDate('');
    setIsModalOpen(true);
  };

  const handleEdit = () => {
    if (selectedOffer) {
      setEditEmployeName(selectedOffer.employeName);
      setEditClientName(selectedOffer.clientName);
      setEditTotalPrize(selectedOffer.totalPrize);
      setEditDate(selectedOffer.date);
      setIsModalOpen(true);
    }
  };

  const handleDelete = () => {
    if (selectedOffer) {
      setOffers(offers.filter(o => o.offerID !== selectedOffer.offerID));
      setSelectedOffer(null);
    }
  };

  const handleSave = () => {
    if (selectedOffer) {
      setOffers(offers.map(o =>
        o.offerID === selectedOffer.offerID
          ? {
              ...o,
              employeName: editEmployeName,
              clientName: editClientName,
              totalPrize: editTotalPrize,
              date: editDate
            }
          : o
      ));
    } else {
      const newOffer: Offer = {
        offerID: Date.now(),
        employeId: "",
        employeName: editEmployeName,
        clientId: "",
        clientName: editClientName,
        date: editDate,
        totalPrize: editTotalPrize,
        products: []
      };
      setOffers([...offers, newOffer]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="OfferTable">
      <h1 className="offer-title">Tabla de Ofertas</h1>
      <div className="offer-filters">
        <label>
          Fecha inicial:
          <input type="date" value={filterStart} onChange={e => setFilterStart(e.target.value)} />
        </label>
        <label>
          Fecha final:
          <input type="date" value={filterEnd} onChange={e => setFilterEnd(e.target.value)} />
        </label>
      </div>
      <div className="offers-table-container">
        <table className="offer-table">
          <thead>
            <tr>
              <th>Empleado</th>
              <th>Cliente</th>
              <th>Fecha</th>
              <th>Precio Total</th>
              <th>Productos</th>
            </tr>
          </thead>
          <tbody>
            {filteredOffers.map(offer => (
              <tr
                key={offer.offerID}
                className={selectedOffer?.offerID === offer.offerID ? 'selected' : ''}
                onClick={() => setSelectedOffer(offer)}
                style={{ cursor: 'pointer' }}
              >
                <td>{offer.employeName}</td>
                <td>{offer.clientName}</td>
                <td>{offer.date}</td>
                <td>{offer.totalPrize}</td>
                <td>
                  <button
                    type="button"
                    onClick={e => {
                      e.stopPropagation();
                      setProductsToShow(offer.products);
                      setIsProductsModalOpen(true);
                    }}
                  >
                    Mostrar productos
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
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
              Empleado:
              <input type="text" value={editEmployeName} onChange={e => setEditEmployeName(e.target.value)} />
            </label>
            <label>
              Cliente:
              <input type="text" value={editClientName} onChange={e => setEditClientName(e.target.value)} />
            </label>
            <label>
              Precio Total:
              <input type="text" value={editTotalPrize} onChange={e => setEditTotalPrize(e.target.value)} />
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
      {isProductsModalOpen && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>Productos de la oferta</h2>
            <div className="products-table-container">
              <table className="products-table">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Cantidad</th>
                  </tr>
                </thead>
                <tbody>
                  {productsToShow.map((prod, idx) => (
                    <tr key={idx}>
                      <td>{prod.name}</td>
                      <td>{prod.quantity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="modal-actions">
              <button onClick={() => setIsProductsModalOpen(false)}>Cerrar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default OfferTable;