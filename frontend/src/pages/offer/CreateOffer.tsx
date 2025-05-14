import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import './CreateOffer.css';

interface Product {
  name: string;
  quantity: string;
}

interface ProductOption {
  id: string;
  name: string;
}

interface Client {
  id: string;
  name: string;
}

interface BackendProduct {
  productId: string;
  name: string;
  description: string;
  stock: number;
  maxStock: number;
  minStock: number;
  purchasePrice: number;
  sellPrice: number;
}

interface BackendClient {
  clientID: string;
  CompanyName: string;
  CIF: string;
  address: string;
  email: string;
  phone: string;
  contact: string;
}

function CreateOffer() {
  const [client, setClient] = useState<Client | null>(null);
  const [clients, setClients] = useState<Client[]>([]);
  const [product, setProduct] = useState<ProductOption | null>(null);
  const [productsOptions, setProductsOptions] = useState<ProductOption[]>([]);
  const [productQuantity, setProductQuantity] = useState('');
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  // Fetch real de clientes desde el backend y mapea solo id y name
  useEffect(() => {
    const fetchClients = async () => {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/client/`, {
          headers: {
            Authorization: `Bearer ${credential}`,
          },
        });
        if (!response.ok) throw new Error('Error al obtener los clientes');
        const backendClients: BackendClient[] = await response.json();
        setClients(
          backendClients.map((cli) => ({
            id: cli.clientID,
            name: cli.CompanyName,
          }))
        );
      } catch {
        setClients([]);
      }
    };
    fetchClients();
  }, []);

  // Fetch real de productos desde el backend y mapea solo id y name
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const credential = localStorage.getItem('credential');
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/product/`, {
          headers: {
            Authorization: `Bearer ${credential}`,
          },
        });
        if (!response.ok) throw new Error('Error al obtener productos');
        const backendProducts: BackendProduct[] = await response.json();
        setProductsOptions(
          backendProducts.map((prod) => ({
            id: prod.productId,
            name: prod.name,
          }))
        );
      } catch {
        setProductsOptions([]);
      }
    };
    fetchProducts();
  }, []);

  const handleAddProduct = () => {
    setError(null);
    if (!product || !productQuantity.trim()) return;
    if (products.some(p => p.name === product.name)) {
      setError('Este producto ya ha sido añadido.');
      return;
    }
    setProducts([...products, { name: product.name, quantity: productQuantity }]);
    setProduct(null);
    setProductQuantity('');
  };

  const handleDeleteProduct = (idx: number) => {
    setProducts(products.filter((_, i) => i !== idx));
  };

const handleCreateOffer = async () => {
  if (!client || products.length === 0) {
    setError('Selecciona un cliente y añade al menos un producto.');
    return;
  }
  const offerPayload = {
    clientId: client.id,
    products: JSON.stringify( products.map(prod => {
      // Buscar el id real del producto por el nombre
      const prodOption = productsOptions.find(opt => opt.name === prod.name);
      return {
        id: prodOption ? prodOption.id : '',
        quantity: prod.quantity,
      };
    }))
  };

  try {
    console.log('Payload:', offerPayload);
    const credential = localStorage.getItem('credential');
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/offer/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${credential}`,
      },
      body: JSON.stringify(offerPayload),
    });
    if (!response.ok) throw new Error('Error al crear la oferta');
    navigate('/offer');
  } catch {
    setError('Error al crear la oferta');
  }
};

  return (
    <main className="main-content">
      <div className="create-offer-form">
        <h1 className="offer-title">Crear oferta</h1>
        <div className="form-group cliente-group">
          <Autocomplete
            options={clients}
            getOptionLabel={(option) => option.name}
            value={client}
            onChange={(_, newValue) => setClient(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Cliente" placeholder="Nombre del cliente" />
            )}
            sx={{ width: 300 }}
            isOptionEqualToValue={(option, value) => option.id === value.id}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end' }}>
          <Autocomplete
            options={productsOptions}
            getOptionLabel={(option) => option.name}
            value={product}
            onChange={(_, newValue) => setProduct(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Producto" placeholder="Nombre del producto" />
            )}
            sx={{ width: 200 }}
            isOptionEqualToValue={(option, value) => option.id === value.id}
          />
          <label>
            <input
              type="number"
              min="1"
              value={productQuantity}
              onChange={e => setProductQuantity(e.target.value)}
              placeholder="Cantidad"
            />
          </label>
          <button type="button" onClick={handleAddProduct}>
            Añadir producto
          </button>
        </div>
        {error && (
          <div style={{ color: 'red', marginTop: '0.5rem', width: '100%' }}>
            {error}
          </div>
        )}
        <div className="products-table-container" style={{ marginTop: '2rem' }}>
          <table className="products-table">
            <thead>
              <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Eliminar</th>
              </tr>
            </thead>
            <tbody>
              {products.map((prod, idx) => (
                <tr key={idx}>
                  <td>{prod.name}</td>
                  <td>{prod.quantity}</td>
                  <td>
                    <button type="button" onClick={() => handleDeleteProduct(idx)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
              {products.length === 0 && (
                <tr>
                  <td colSpan={3} style={{ textAlign: 'center', color: '#888' }}>
                    No hay productos añadidos
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
          <button type="button" onClick={handleCreateOffer}>
            Crear oferta
          </button>
        </div>
      </div>
    </main>
  );
}

export default CreateOffer;