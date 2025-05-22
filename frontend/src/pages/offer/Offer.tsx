import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Offer.css';

interface Product {
  name: string;
  id: string | number;
  quantity: string | number;
}

interface Offer {
  offerID: string;
  employeID: string;
  employeName: string;
  clientID: string;
  clientName: string;
  date: string;
  totalPrice: string | number;
  products: Product[];
}

function OfferTable() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [filteredOffers, setFilteredOffers] = useState<Offer[]>([]);
  const [selectedOffer, setSelectedOffer] = useState<Offer | null>(null);
  const [filterStart, setFilterStart] = useState('');
  const [filterEnd, setFilterEnd] = useState('');
  const [isProductsModalOpen, setIsProductsModalOpen] = useState(false);
  const [productsToShow, setProductsToShow] = useState<Product[]>([]);

  const navigate = useNavigate();

  // Obtener el rol del usuario (si lo necesitas para el botón PDF)
  //const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
  //const rol = Number(backendData.rol) || -1;

  // Fetch real de ofertas desde el backend
  useEffect(() => {
    const fetchOffers = async () => {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/offer/`, {
          headers: {
            Authorization: `Bearer ${credential}`,
          },
        });
        if (!response.ok) throw new Error('Error al obtener las ofertas');
        const data: Offer[] = await response.json();
        setOffers(data);
        setFilteredOffers(data);
      } catch {
        setOffers([]);
        setFilteredOffers([]);
      }
    };
    fetchOffers();
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

  const handleConvertToOrder = async () => {
    if (!selectedOffer) return;
    try {
      const credential = localStorage.getItem('credential');
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/order/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${credential}`,
        },
        body: JSON.stringify({ offerID: selectedOffer.offerID }),
      });
      if (!response.ok) {
        alert('Error al convertir la oferta en pedido');
        return;
      }
      alert('Oferta convertida en pedido correctamente');
    } catch {
      alert('Error al convertir la oferta en pedido');
    }
  };

  // Generar PDF de la oferta seleccionada
  const handleGenerateOfferPDF = async () => {
    if (!selectedOffer) return;
    const credential = localStorage.getItem('credential');
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/offer/pdf?offerID=${selectedOffer.offerID}`,
      {
        headers: {
          Authorization: `Bearer ${credential}`,
        },
      }
    );
    if (!response.ok) {
      alert('Error al generar el PDF de la oferta');
      return;
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${selectedOffer.offerID}_${selectedOffer.date}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
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
              <th>Precio total</th>
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
                <td>{offer.totalPrice}</td>
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
        <button onClick={() => navigate('/createoffer')}>Crear oferta</button>
        <button
          onClick={() => {
            if (selectedOffer) {
              navigate('/editoffer', { state: { offerID: selectedOffer.offerID, products: selectedOffer.products } });
            }
          }}
          disabled={!selectedOffer}
        >
          Editar oferta
        </button>
        <button onClick={handleConvertToOrder} disabled={!selectedOffer}>
          Convertir a pedido
        </button>
        <button
          onClick={handleGenerateOfferPDF}
          disabled={!selectedOffer}
        >
          Generar PDF oferta
        </button>
      </div>
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
                    <tr key={prod.id ?? idx}>
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