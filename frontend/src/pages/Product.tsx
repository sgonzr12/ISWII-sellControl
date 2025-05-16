import './Product.css';
import { useState, useEffect } from 'react';

function Product() {
    const [products, setProducts] = useState<{productId: string; name: string; description: string; stock: number; maxStock: number; minStock: number; purchasePrice: number; sellPrice: number }[]>([]);
    const [selectedProduct, setSelectedProduct] = useState<{productId: string; name: string; description: string; stock: number; maxStock: number; minStock: number; purchasePrice: number; sellPrice: number } | null>(null);

    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [addName, setAddName] = useState('');
    const [addDescription, setAddDescription] = useState('');
    const [addStock, setAddStock] = useState('');
    const [addMaxStock, setAddMaxStock] = useState('');
    const [addMinStock, setAddMinStock] = useState('');
    const [addPurchasePrice, setAddPurchasePrice] = useState('');
    const [addSellPrice, setAddSellPrice] = useState('');

    const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
    const [editStock, setEditStock] = useState('');
    const [editMaxStock, setEditMaxStock] = useState('');
    const [editMinStock, setEditMinStock] = useState('');
    const [editPurchasePrice, setEditPurchasePrice] = useState('');
    const [editSellPrice, setEditSellPrice] = useState('');

    const [search, setSearch] = useState('');

    // Obtener el rol del usuario
    const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
    const rol = Number(backendData.rol) || -1;

    const fetchProducts = async () => {
        try {
            const credential = localStorage.getItem('credential');
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/product/`, {
                headers: {
                    Authorization: `Bearer ${credential}`
                }
            });

            if (!response.ok) {
                throw new Error('Error fetching products');
            }

            const data = await response.json();
            setProducts(data);
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };

    useEffect(() => {
        fetchProducts();
    }, []);

    const handleSelectProduct = (product: {productId: string; name: string; description: string; stock: number; maxStock: number; minStock: number; purchasePrice: number; sellPrice: number }) => {
        setSelectedProduct(product);
    }

    const handleEditClick = () => {
        if (selectedProduct) {
            setEditStock(selectedProduct.stock.toString());
            setEditMaxStock(selectedProduct.maxStock.toString());
            setEditMinStock(selectedProduct.minStock.toString());
            setEditPurchasePrice(selectedProduct.purchasePrice.toString());
            setEditSellPrice(selectedProduct.sellPrice.toString());
        }
        setIsUpdateModalOpen(true);
    }

    const handleAddClick = () => {
        setAddName('');
        setAddDescription('');
        setAddStock('');
        setAddMaxStock('');
        setAddMinStock('');
        setAddPurchasePrice('');
        setAddSellPrice('');
        setIsAddModalOpen(true);
    }

    const handleSave = async () => {
        if (!selectedProduct) return;
        try {
            const credential = localStorage.getItem('credential');
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/product`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${credential}`
                },
                body: JSON.stringify({
                    productId: selectedProduct.productId,
                    name: selectedProduct.name,
                    description: selectedProduct.description,
                    stock: editStock,
                    maxStock: editMaxStock,
                    minStock: editMinStock,
                    purchasePrice: editPurchasePrice,
                    sellPrice: editSellPrice,
                }),
            });

            if (!response.ok) {
                throw new Error('Error updating product');
            }

            const data = await response.json();
            setProducts(products.map(products => products.productId === selectedProduct.productId ? data : products));
            setIsUpdateModalOpen(false);
            fetchProducts();
        }
        catch (error) {
            console.error('Error updating product:', error);
        }
    };

    const handleAdd = async () => {
        try {
            const credential = localStorage.getItem('credential');
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/product`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${credential}`
                },
                body: JSON.stringify({
                    name: addName,
                    description: addDescription,
                    stock: addStock,
                    maxStock: addMaxStock,
                    minStock: addMinStock,
                    purchasePrice: addPurchasePrice,
                    sellPrice: addSellPrice,
                }),
            });

            if (!response.ok) {
                throw new Error('Error adding product');
            }

            const data = await response.json();
            setProducts([...products, data]);
            setIsAddModalOpen(false);
            fetchProducts();
        }
        catch (error) {
            console.error('Error adding product:', error);
        }
    }

    // Filtrado por nombre de producto
    const filteredProducts = products.filter(product =>
        product.name.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="Product">
            <main className="main-content">
                <div className="product">
                    <h1>Productos</h1>
                    <div style={{ marginBottom: '1rem', textAlign: 'center' }}>
                        <input
                            type="text"
                            placeholder="Buscar producto..."
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                            style={{ padding: '0.5rem', width: '250px' }}
                        />
                    </div>
                    <div className="product-table-container">
                        <table className="product-table">
                            <thead>
                                <tr>
                                    <th>Nombre</th>
                                    <th>Descripción</th>
                                    <th>Stock</th>
                                    <th>Stock máximo</th>
                                    <th>Stock mínimo</th>
                                    <th>Precio compra</th>
                                    <th>Precio venta</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredProducts.map(product => (
                                    <tr
                                        key={product.productId}
                                        className={selectedProduct?.productId === product.productId ? 'selected' : ''}
                                        onClick={() => handleSelectProduct(product)}
                                        style={{ cursor: 'pointer' }}
                                    >
                                        <td>{product.name}</td>
                                        <td>{product.description}</td>
                                        <td>{product.stock}</td>
                                        <td>{product.maxStock}</td>
                                        <td>{product.minStock}</td>
                                        <td>{product.purchasePrice}</td>
                                        <td>{product.sellPrice}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div className="product-buttons-row">
                        {/* Solo admin, manager y warehouseManager pueden crear o editar productos */}
                        {(rol === 1 || rol === 2 || rol === 4) && (
                            <button
                                className="add-product-button"
                                onClick={handleAddClick}>
                                Añadir producto
                            </button>
                        )}
                        {(rol === 1 || rol === 2 || rol === 4) && (
                            <button
                                className="update-product-button"
                                onClick={handleEditClick}
                                disabled={!selectedProduct}>
                                Modificar producto
                            </button>
                        )}
                    </div>
                </div>

                {isUpdateModalOpen && (
                    <div className="modal-backdrop">
                        <div className="modal">
                            <h2>Modificar producto</h2>
                            <label>Nombre: &nbsp; {selectedProduct?.name}</label>
                            <label>Descripción: &nbsp; {selectedProduct?.description}</label>
                            <label>Stock: &nbsp;</label>
                            <input type="number" value={editStock} onChange={e => setEditStock(e.target.value)} />
                            <label>Stock máximo: &nbsp;</label>
                            <input type="number" value={editMaxStock} onChange={e => setEditMaxStock(e.target.value)} />
                            <label>Stock mínimo: &nbsp;</label>
                            <input type="number" value={editMinStock} onChange={e => setEditMinStock(e.target.value)} />
                            <label>Precio de compra: &nbsp;</label>
                            <input type="number" value={editPurchasePrice} step="0.01" onChange={e => setEditPurchasePrice(e.target.value)} />
                            <label>Precio de venta: &nbsp;</label>
                            <input type="number" value={editSellPrice} step="0.01" onChange={e => setEditSellPrice(e.target.value)} />

                            <div className="modal-buttons">
                                <button onClick={handleSave}>Guardar</button>
                                <button onClick={() => setIsUpdateModalOpen(false)}>Cancelar</button>
                            </div>
                        </div>
                    </div>
                )}

                {isAddModalOpen && (
                    <div className="modal-backdrop">
                        <div className="modal">
                            <h2>Añadir producto</h2>
                            <label>Nombre: &nbsp;</label>
                            <input type="text" value={addName} onChange={e => setAddName(e.target.value)} />
                            <label>Descripción: &nbsp;</label>
                            <input type="text" value={addDescription} onChange={e => setAddDescription(e.target.value)} />
                            <label>Stock: &nbsp;</label>
                            <input type="number" value={addStock} onChange={e => setAddStock(e.target.value)} />
                            <label>Stock máximo: &nbsp;</label>
                            <input type="number" value={addMaxStock} onChange={e => setAddMaxStock(e.target.value)} />
                            <label>Stock mínimo: &nbsp;</label>
                            <input type="number" value={addMinStock} onChange={e => setAddMinStock(e.target.value)} />
                            <label>Precio de compra: &nbsp;</label>
                            <input type="number" value={addPurchasePrice} onChange={e => setAddPurchasePrice(e.target.value)} />
                            <label>Precio de venta: &nbsp;</label>
                            <input type="number" value={addSellPrice} onChange={e => setAddSellPrice(e.target.value)} />

                            <div className="modal-buttons">
                                <button onClick={handleAdd}>Guardar</button>
                                <button onClick={() => setIsAddModalOpen(false)}>Cancelar</button>
                            </div>
                        </div>
                    </div>
                )}

            </main>
        </div>
    );
}

export default Product;