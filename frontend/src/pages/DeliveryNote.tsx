import { useState, useEffect } from 'react';
import './DeliveryNote.css';

interface Product {
  name: string;
  id: string | number;
  quantity: string | number;
}

interface DeliveryNote {
  DeliveryNoteID: string;
  employeID: string;
  employeName: string;
  clientID: string;
  clientName: string;
  date: string;
  totalPrice: string | number;
  products: Product[];
}

function DeliveryNoteTable() {
  const [deliveryNotes, setDeliveryNotes] = useState<DeliveryNote[]>([]);
  const [filteredDeliveryNotes, setFilteredDeliveryNotes] = useState<DeliveryNote[]>([]);
  const [filterStart, setFilterStart] = useState('');
  const [filterEnd, setFilterEnd] = useState('');
  const [selectedDeliveryNote, setSelectedDeliveryNote] = useState<DeliveryNote | null>(null);
  const [isProductsModalOpen, setIsProductsModalOpen] = useState(false);
  const [productsToShow, setProductsToShow] = useState<Product[]>([]);


  const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
  const rol = Number(backendData.rol) || -1;


  useEffect(() => {
    const fetchDeliveryNotes = async () => {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/deliverynote`, {
          headers: {
            Authorization: `Bearer ${credential}`,
          },
        });
        if (!response.ok) throw new Error('Error al obtener los albaranes');
        const data: DeliveryNote[] = await response.json();
        console.log(data);
        setDeliveryNotes(data);
        setFilteredDeliveryNotes(data);
      } catch {
        setDeliveryNotes([]);
        setFilteredDeliveryNotes([]);
      }
    };
    fetchDeliveryNotes();
  }, []);


  useEffect(() => {
    let filtered = deliveryNotes;
    if (filterStart) {
      filtered = filtered.filter(o => o.date >= filterStart);
    }
    if (filterEnd) {
      filtered = filtered.filter(o => o.date <= filterEnd);
    }
    setFilteredDeliveryNotes(filtered);
  }, [filterStart, filterEnd, deliveryNotes]);


  const handleConvertToInvoice = async () => {
    if (!selectedDeliveryNote) return;
    try {
      const credential = localStorage.getItem('credential');
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/invoice/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${credential}`,
        },
        body: JSON.stringify({ DeliveryNoteID: selectedDeliveryNote.DeliveryNoteID }),
      });
      if (!response.ok) {
        alert('Error al convertir el albarán en factura');
        return;
      }
      alert('Albarán convertido en factura correctamente');
    } catch {
      alert('Error al convertir el albarán en factura');
    }
  };


  const handleGeneratePDF = async () => {
    if (!selectedDeliveryNote) return;
    const credential = localStorage.getItem('credential');
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/deliverynote/pdf?deliveryNoteID=${selectedDeliveryNote.DeliveryNoteID}`,
      {
        headers: {
          Authorization: `Bearer ${credential}`,
        },
      }
    );
    if (!response.ok) {
      alert('Error al generar el PDF del albarán');
      return;
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `albaran_${selectedDeliveryNote.DeliveryNoteID}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="DeliveryNoteTable">
      <h1 className="deliverynote-title">Tabla de Albaranes</h1>
      <div className="deliverynote-filters">
        <label>
          Fecha inicial:
          <input type="date" value={filterStart} onChange={e => setFilterStart(e.target.value)} />
        </label>
        <label>
          Fecha final:
          <input type="date" value={filterEnd} onChange={e => setFilterEnd(e.target.value)} />
        </label>
      </div>
      <div className="deliverynotes-table-container">
        <table className="deliverynote-table">
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
            {filteredDeliveryNotes.map(note => (
              <tr
                key={note.DeliveryNoteID}
                className={selectedDeliveryNote?.DeliveryNoteID === note.DeliveryNoteID ? 'selected' : ''}
                onClick={() => setSelectedDeliveryNote(note)}
                style={{ cursor: 'pointer' }}
              >
                <td>{note.employeName}</td>
                <td>{note.clientName}</td>
                <td>{note.date}</td>
                <td>{note.totalPrice} €</td>
                <td>
                  <button
                    type="button"
                    onClick={e => {
                      e.stopPropagation();
                      setProductsToShow(note.products);
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
        <button
          onClick={handleConvertToInvoice}
          disabled={!selectedDeliveryNote}
        >
          Convertir a factura
        </button>
        {(rol === 1 || rol === 2 || rol === 3 || rol === 4) && (
          <button
            onClick={handleGeneratePDF}
            disabled={!selectedDeliveryNote}
          >
            Generar PDF Albaran
          </button>
        )}
      </div>
      {isProductsModalOpen && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>Productos del albarán</h2>
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

export default DeliveryNoteTable;