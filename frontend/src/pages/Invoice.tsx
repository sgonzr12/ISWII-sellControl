import { useState, useEffect } from 'react';
import './Invoice.css';

interface Product {
  name: string;
  id: string | number;
  quantity: string | number;
}

interface Invoice {
  invoiceID: string;
  employeID: string;
  employeName: string;
  clientID: string;
  clientName: string;
  date: string;
  totalPrice: string | number;
  products: Product[];
}

function InvoiceTable() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [filteredInvoices, setFilteredInvoices] = useState<Invoice[]>([]);
  const [filterStart, setFilterStart] = useState('');
  const [filterEnd, setFilterEnd] = useState('');
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);
  const [isProductsModalOpen, setIsProductsModalOpen] = useState(false);
  const [productsToShow, setProductsToShow] = useState<Product[]>([]);

  // Obtener el rol del usuario
  const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
  const rol = Number(backendData.rol) || -1;

  // Llamada GET al backend para obtener las facturas
  useEffect(() => {
    const fetchInvoices = async () => {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/invoice/`, {
          headers: {
            Authorization: `Bearer ${credential}`,
          },
        });
        if (!response.ok) throw new Error('Error al obtener las facturas');
        const data: Invoice[] = await response.json();
        console.log(data);
        setInvoices(data);
        setFilteredInvoices(data);
      } catch {
        setInvoices([]);
        setFilteredInvoices([]);
      }
    };
    fetchInvoices();
  }, []);

  // Filtrado por fecha
  useEffect(() => {
    let filtered = invoices;
    if (filterStart) {
      filtered = filtered.filter(o => o.date >= filterStart);
    }
    if (filterEnd) {
      filtered = filtered.filter(o => o.date <= filterEnd);
    }
    setFilteredInvoices(filtered);
  }, [filterStart, filterEnd, invoices]);

  // Generar factura (deja el hueco para la llamada al backend)
  const handleGenerateInvoice = async () => {
    if (!selectedInvoice) return;
    const credential = localStorage.getItem('credential');
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/invoice/pdf?invoiceID=${selectedInvoice.invoiceID}`,
      {
        headers: {
          Authorization: `Bearer ${credential}`,
        },
      }
    );
    if (!response.ok) {
      alert('Error al generar el PDF de la factura');
      return;
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `factura_${selectedInvoice.invoiceID}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="InvoiceTable">
      <h1 className="invoice-title">Tabla de Facturas</h1>
      <div className="invoice-filters">
        <label>
          Fecha inicial:
          <input type="date" value={filterStart} onChange={e => setFilterStart(e.target.value)} />
        </label>
        <label>
          Fecha final:
          <input type="date" value={filterEnd} onChange={e => setFilterEnd(e.target.value)} />
        </label>
      </div>
      <div className="invoices-table-container">
        <table className="invoice-table">
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
            {filteredInvoices.map(invoice => (
              <tr
                key={invoice.invoiceID}
                className={selectedInvoice?.invoiceID === invoice.invoiceID ? 'selected' : ''}
                onClick={() => setSelectedInvoice(invoice)}
                style={{ cursor: 'pointer' }}
              >
                <td>{invoice.employeName}</td>
                <td>{invoice.clientName}</td>
                <td>{invoice.date}</td>
                <td>{invoice.totalPrice}</td>
                <td>
                  <button
                    type="button"
                    onClick={e => {
                      e.stopPropagation();
                      setProductsToShow(invoice.products);
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
        {(rol === 1 || rol === 3) && (
          <button
            onClick={handleGenerateInvoice}
            disabled={!selectedInvoice}
          >
            Generar PDF factura
          </button>
        )}
      </div>
      {isProductsModalOpen && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>Productos de la factura</h2>
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

export default InvoiceTable;