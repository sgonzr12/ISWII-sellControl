import { useState, useEffect } from 'react';
import './Order.css';

interface Product {
  name: string;
  id: string | number;
  quantity: string | number;
}

interface Order {
  orderID: string;
  employeID: string;
  employeName: string;
  clientID: string;
  clientName: string;
  date: string;
  totalPrice: string | number;
  products: Product[];
}

function OrderTable() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [filteredOrders, setFilteredOrders] = useState<Order[]>([]);
  const [filterStart, setFilterStart] = useState('');
  const [filterEnd, setFilterEnd] = useState('');
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [isProductsModalOpen, setIsProductsModalOpen] = useState(false);
  const [productsToShow, setProductsToShow] = useState<Product[]>([]);


  const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
  const rol = Number(backendData.rol) || -1;


  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/order/`, {
          headers: {
            Authorization: `Bearer ${credential}`,
          },
        });
        if (!response.ok) throw new Error('Error al obtener los pedidos');
        const data: Order[] = await response.json();
        setOrders(data);
        setFilteredOrders(data);
      } catch {
        setOrders([]);
        setFilteredOrders([]);
      }
    };
    fetchOrders();
  }, []);

  // Filtrado por fecha
  useEffect(() => {
    let filtered = orders;
    if (filterStart) {
      filtered = filtered.filter(o => o.date >= filterStart);
    }
    if (filterEnd) {
      filtered = filtered.filter(o => o.date <= filterEnd);
    }
    setFilteredOrders(filtered);
  }, [filterStart, filterEnd, orders]);

  // Convertir a albarán
  const handleConvertToDeliveryNote = async () => {
    if (!selectedOrder) return;
    try {
      const credential = localStorage.getItem('credential');
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/deliverynote/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${credential}`,
        },
        body: JSON.stringify({ orderID: selectedOrder.orderID }),
      });
      if (!response.ok) {
        alert('Error al convertir el pedido en albarán');
        return;
      }
      alert('Pedido convertido en albarán correctamente');
    } catch {
      alert('Error al convertir el pedido en albarán');
    }
  };


  const handleGeneratePDF = async () => {
  if (!selectedOrder) return;
    const credential = localStorage.getItem('credential');
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/order/pdf?orderID=${selectedOrder.orderID}`,
      {
        headers: {
          Authorization: `Bearer ${credential}`,
        },
      }
    );
    if (!response.ok) {
      alert('Error al generar el PDF del pedido');
      return;
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pedido_${selectedOrder.orderID}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="OrderTable">
      <h1 className="order-title">Tabla de Pedidos</h1>
      <div className="order-filters">
        <label>
          Fecha inicial:
          <input type="date" value={filterStart} onChange={e => setFilterStart(e.target.value)} />
        </label>
        <label>
          Fecha final:
          <input type="date" value={filterEnd} onChange={e => setFilterEnd(e.target.value)} />
        </label>
      </div>
      <div className="orders-table-container">
        <table className="order-table">
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
            {filteredOrders.map(order => (
              <tr
                key={order.orderID}
                className={selectedOrder?.orderID === order.orderID ? 'selected' : ''}
                onClick={() => setSelectedOrder(order)}
                style={{ cursor: 'pointer' }}
              >
                <td>{order.employeName}</td>
                <td>{order.clientName}</td>
                <td>{order.date}</td>
                <td>{order.totalPrice} €</td>
                <td>
                  <button
                    type="button"
                    onClick={e => {
                      e.stopPropagation();
                      setProductsToShow(order.products);
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
          onClick={handleConvertToDeliveryNote}
          disabled={!selectedOrder}
        >
          Convertir a albarán
        </button>
        {(rol === 1 || rol === 2 || rol === 3 || rol === 4) && (
          <button
            onClick={handleGeneratePDF}
            disabled={!selectedOrder}
          >
            Generar PDF Pedido
          </button>
        )}
      </div>
      {isProductsModalOpen && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>Productos del pedido</h2>
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

export default OrderTable;