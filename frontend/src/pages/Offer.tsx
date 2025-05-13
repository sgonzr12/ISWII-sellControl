import { useState, useEffect } from 'react';
import './Offer.css';

interface Product {
  productName: string;
  quantity: number;
  price: number;
}

interface Offer {
  OfferID: number;
  Employe: string;
  Client: string;
  Date: string;
  price: number;
  products: Product | Product[];
}

function OfferTable() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [filteredOffers, setFilteredOffers] = useState<Offer[]>([]);
  const [selectedOffer, setSelectedOffer] = useState<Offer | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editEmploye, setEditEmploye] = useState('');
  const [editClient, setEditClient] = useState('');
  const [editPrice, setEditPrice] = useState('');
  const [editDate, setEditDate] = useState('');
  const [filterStart, setFilterStart] = useState('');
  const [filterEnd, setFilterEnd] = useState('');
  const [isProductsModalOpen, setIsProductsModalOpen] = useState(false);
  const [productsToShow, setProductsToShow] = useState<Product[]>([]);

  // Simulación de fetch de ofertas
  useEffect(() => {
    // Ejemplo compatible con tu JSON
    const mockOffers: Offer[] = [
    {
      OfferID: 1,
      Employe: "Juan",
      Client: "Pedro",
      Date: "2023-10-01",
      price: 1000,
      products: {
        productName: "Laptop",
        quantity: 1,
        price: 1000
      }
    },
    {
      OfferID: 2,
      Employe: "Ana",
      Client: "Maria",
      Date: "2023-10-10",
      price: 1500,
      products: [
        { productName: "Tablet", quantity: 2, price: 500 },
        { productName: "Ratón", quantity: 3, price: 100 }
      ]
    },
    {
      OfferID: 3,
      Employe: "Luis",
      Client: "Carlos",
      Date: "2023-11-05",
      price: 800,
      products: {
        productName: "Monitor",
        quantity: 2,
        price: 400
      }
    },
    {
      OfferID: 4,
      Employe: "Marta",
      Client: "Lucía",
      Date: "2023-12-12",
      price: 1200,
      products: [
        { productName: "Teclado", quantity: 4, price: 50 },
        { productName: "Impresora", quantity: 1, price: 1000 }
      ]
    },
    {
      OfferID: 5,
      Employe: "Pedro",
      Client: "Sofía",
      Date: "2024-01-15",
      price: 600,
      products: {
        productName: "Altavoz",
        quantity: 3,
        price: 200
      }
    },
    {
      OfferID: 6,
      Employe: "Elena",
      Client: "Miguel",
      Date: "2024-02-20",
      price: 950,
      products: [
        { productName: "Tablet", quantity: 1, price: 500 },
        { productName: "Ratón", quantity: 5, price: 90 }
      ]
    },
    {
      OfferID: 7,
      Employe: "Carlos",
      Client: "Raúl",
      Date: "2024-03-10",
      price: 1100,
      products: {
        productName: "Proyector",
        quantity: 1,
        price: 1100
      }
    },
    {
      OfferID: 8,
      Employe: "Lucía",
      Client: "Paula",
      Date: "2024-04-05",
      price: 700,
      products: [
        { productName: "Auriculares", quantity: 2, price: 150 },
        { productName: "Webcam", quantity: 1, price: 400 }
      ]
    },
    {
      OfferID: 9,
      Employe: "Miguel",
      Client: "David",
      Date: "2024-05-18",
      price: 1300,
      products: {
        productName: "Silla ergonómica",
        quantity: 2,
        price: 650
      }
    },
    {
      OfferID: 10,
      Employe: "Raúl",
      Client: "Elena",
      Date: "2024-06-22",
      price: 2000,
      products: [
        { productName: "PC Gaming", quantity: 1, price: 1800 },
        { productName: "Alfombrilla", quantity: 2, price: 100 }
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
      filtered = filtered.filter(o => o.Date >= filterStart);
    }
    if (filterEnd) {
      filtered = filtered.filter(o => o.Date <= filterEnd);
    }
    setFilteredOffers(filtered);
  }, [filterStart, filterEnd, offers]);

  const handleCreate = () => {
    setSelectedOffer(null);
    setEditEmploye('');
    setEditClient('');
    setEditPrice('');
    setEditDate('');
    setIsModalOpen(true);
  };

  const handleEdit = () => {
    if (selectedOffer) {
      setEditEmploye(selectedOffer.Employe);
      setEditClient(selectedOffer.Client);
      setEditPrice(selectedOffer.price.toString());
      setEditDate(selectedOffer.Date);
      setIsModalOpen(true);
    }
  };

  const handleDelete = () => {
    if (selectedOffer) {
      setOffers(offers.filter(o => o.OfferID !== selectedOffer.OfferID));
      setSelectedOffer(null);
    }
  };

  const handleSave = () => {
    if (selectedOffer) {
      // Editar oferta existente
      setOffers(offers.map(o =>
        o.OfferID === selectedOffer.OfferID
          ? {
              ...o,
              Employe: editEmploye,
              Client: editClient,
              price: Number(editPrice),
              Date: editDate
            }
          : o
      ));
    } else {
      // Crear nueva oferta
      const newOffer: Offer = {
        OfferID: Date.now(),
        Employe: editEmploye,
        Client: editClient,
        price: Number(editPrice),
        Date: editDate,
        products: []
      };
      setOffers([...offers, newOffer]);
    }
    setIsModalOpen(false);
  };

  // Normaliza products a array para mostrar en la tabla
  const getProductsArray = (products: Product | Product[] | undefined) => {
    if (!products) return [];
    return Array.isArray(products) ? products : [products];
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
              <th>Precio</th>
              <th>Productos</th>
            </tr>
          </thead>
          <tbody>
            {filteredOffers.map(offer => (
              <tr
                key={offer.OfferID}
                className={selectedOffer?.OfferID === offer.OfferID ? 'selected' : ''}
                onClick={() => setSelectedOffer(offer)}
                style={{ cursor: 'pointer' }}
              >
                <td>{offer.Employe}</td>
                <td>{offer.Client}</td>
                <td>{offer.Date}</td>
                <td>{offer.price}</td>
                <td>
                  <button
                    type="button"
                    onClick={e => {
                      e.stopPropagation();
                      setProductsToShow(getProductsArray(offer.products));
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
              <input type="text" value={editEmploye} onChange={e => setEditEmploye(e.target.value)} />
            </label>
            <label>
              Cliente:
              <input type="text" value={editClient} onChange={e => setEditClient(e.target.value)} />
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
                    <th>Precio</th>
                  </tr>
                </thead>
                <tbody>
                  {productsToShow.map((prod, idx) => (
                    <tr key={idx}>
                      <td>{prod.productName}</td>
                      <td>{prod.quantity}</td>
                      <td>{prod.price}</td>
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