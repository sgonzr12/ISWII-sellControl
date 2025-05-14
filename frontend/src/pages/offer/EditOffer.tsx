import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import './EditOffer.css';

interface Product {
  name: string;
  quantity: string;
}

interface ProductOption {
  id: string;
  name: string;
}

function EditOffer() {
  const navigate = useNavigate();
  const location = useLocation();
  const { offerID, products: initialProducts } = location.state || {};

  const [products, setProducts] = useState<Product[]>(initialProducts || []);
  const [product, setProduct] = useState<ProductOption | null>(null);
  const [productsOptions, setProductsOptions] = useState<ProductOption[]>([]);
  const [productQuantity, setProductQuantity] = useState('');
  const [error, setError] = useState<string | null>(null);

  // Fetch productos disponibles para añadir
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
        const backendProducts = await response.json();
        type BackendProduct = { productId: string; name: string };
        setProductsOptions(
          (backendProducts as BackendProduct[]).map((prod) => ({
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
    if (Number(productQuantity) <= 0) {
      setError('La cantidad debe ser mayor que 0.');
      return;
    }
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

  const handleQuantityChange = (idx: number, value: string) => {
    if (Number(value) <= 0) {
      setError('La cantidad debe ser mayor que 0.');
      return;
    }
    setError(null);
    setProducts(products.map((prod, i) => i === idx ? { ...prod, quantity: value } : prod));
  };

  const handleSave = async () => {
    // Validar que ninguna cantidad sea 0 o menor
    if (products.some(p => Number(p.quantity) <= 0)) {
      setError('No puede haber productos con cantidad 0 o menor.');
      return;
    }
    try {
      const credential = localStorage.getItem('credential');
      // Buscar los ids reales de los productos por el nombre
      const productsWithIds = products.map(prod => {
        const prodOption = productsOptions.find(opt => opt.name === prod.name);
        return {
          id: prodOption ? prodOption.id : '',
          quantity: prod.quantity,
        };
      });
      const payload = { offerID, products: productsWithIds };
      console.log('PUT payload:', JSON.stringify(payload));
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/offer/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${credential}`,
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        setError('Error al guardar los cambios');
        return;
      }
      navigate('/offer');
    } catch {
      setError('Error al guardar los cambios');
    }
  };

  return (
    <main className="main-content">
      <div className="edit-offer-form">
        <h1 className="offer-title">Editar oferta</h1>
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
                  <td>
                    <input
                      type="number"
                      min="1"
                      value={prod.quantity}
                      onChange={e => handleQuantityChange(idx, e.target.value)}
                      style={{ width: '60px', textAlign: 'center' }}
                    />
                  </td>
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
          <button type="button" onClick={handleSave}>
            Guardar cambios
          </button>
        </div>
      </div>
    </main>
  );
}

export default EditOffer;