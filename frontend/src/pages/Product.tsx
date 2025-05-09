import './Product.css';
import { useState, useEffect} from 'react';

function Product() {
    const [product, setProducts] = useState<{productId: string, name: string, description: string, stock: number, maxStock: number, minStock: number, location: string, purchasePrize: number, sellPrize: number }[]>([]);
    const [selectedProduct, setSelectedProduct] = useState<{productId: string, name: string, description: string, stock: number, maxStock: number, minStock: number, location: string, purchasePrize: number, sellPrize: number } | null>(null);

    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [addName, setAddName] = useState('');
    const [addDescription, setAddDescription] = useState('');
    const [addStock, setAddStock] = useState('');
    const [addMaxStock, setAddMaxStock] = useState('');
    const [addMinStock, setAddMinStock] = useState('');
    const [addLocation, setAddLocation] = useState('');
    const [addPurchasePrize, setAddPurchasePrize] = useState('');
    const [addSellPrize, setAddSellPrize] = useState('');

    const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
    const [editMaxStock, setEditMaxStock] = useState('');
    const [editMinStock, setEditMinStock] = useState('');
    const [editLocation, setEditLocation] = useState('');
    const [editPurchasePrize, setEditPurchasePrize] = useState('');
    const [editSellPrize, setEditSellPrize] = useState('');

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
            console.log('Fetched products:', data);
            setProducts(data);
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };

    useEffect(() => {
        fetchProducts();
    } , []);

    const handleSelectProduct = (product: {productId: string, name: string, description: string, stock: number, maxStock: number, minStock: number, location: string, purchasePrize: number, sellPrize: number }) => {
        setSelectedProduct(product);
    }

    const handleEditClick = () => {
        if (selectedProduct) {
            setEditMaxStock(selectedProduct.maxStock.toString());
            setEditMinStock(selectedProduct.minStock.toString());
            setEditLocation(selectedProduct.location);
            setEditPurchasePrize(selectedProduct.purchasePrize.toString());
            setEditSellPrize(selectedProduct.sellPrize.toString());
        }
        setIsUpdateModalOpen(true);
    }

    const handleAddClick = () => {
        if (selectedProduct){
            setAddName(selectedProduct.name);
            setAddDescription(selectedProduct.description);
            setAddStock(selectedProduct.stock.toString());
            setAddMaxStock(selectedProduct.maxStock.toString());
            setAddMinStock(selectedProduct.minStock.toString());
            setAddLocation(selectedProduct.location);
            setAddPurchasePrize(selectedProduct.purchasePrize.toString());
            setAddSellPrize(selectedProduct.sellPrize.toString());
        }
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
                    stock: selectedProduct.stock,
                    maxStock: editMaxStock,
                    minStock: editMinStock,
                    location: editLocation,
                    purchasePrize: editPurchasePrize,
                    sellPrize: editSellPrize,
                }),
            });

            if (!response.ok) {
                throw new Error('Error updating product');
            }

            const data = await response.json();
            console.log('Updated product:', data);
            setProducts(product.map(product => product.productId === selectedProduct.productId ? data : product));
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
                    location: addLocation,
                    purchasePrize: addPurchasePrize,
                    sellPrize: addSellPrize,
                }),
            });

            if (!response.ok) {
                throw new Error('Error adding product');
            }

            const data = await response.json();
            console.log('Added product:', data);
            setProducts([...product, data]);
            setIsAddModalOpen(false);
            fetchProducts();
        }
        catch (error) {
            console.error('Error adding product:', error);
        }
    }

    return (
        <div className="Product">
            <main className="main-content">
                <div className="product">
                    <h1>Productos</h1>
                    
                    <ul className="product-list">
                        {product.map(product => (
                            <li 
                                key={product.productId} 
                                className={selectedProduct?.productId === product.productId ? 'selected' : ''}
                                onClick={() => handleSelectProduct(product)}>
                                
                                <h2>{product.name}</h2>
                                <p>{product.description}</p>
                                <p>Stock: {product.stock}</p>
                                <p>Stock máximo: {product.maxStock}</p>
                                <p>Stock mínimo: {product.minStock}</p>
                                <p>Ubicación: {product.location}</p>
                                <p>Precio de compra: {product.purchasePrize}</p>
                                <p>Precio de venta: {product.sellPrize}</p>
                            </li>
                        ))}
                    </ul>

                    <button 
                        className="update-product-button"
                        onClick={handleEditClick}
                        disabled={!selectedProduct}>
                        
                        Modificar producto
                    </button>
                    
                    <button
                        className="add-product-button"
                        onClick={handleAddClick}>

                        Añadir producto
                    </button>
                </div>

                {isUpdateModalOpen && (
                    <div className= "modal-backdrop">
                        <div className="modal">
                            <h2>Modificar producto</h2>
                            <label>Nombre: &nbsp; {selectedProduct?.name}</label>
                            <label>Descripción: &nbsp; {selectedProduct?.description}</label>
                            <label>Stock: &nbsp; {selectedProduct?.stock}</label>
                            <label>Stock máximo: &nbsp;</label>
                            <input type="number" value={selectedProduct?.maxStock} onChange={e => setEditMaxStock(e.target.value)} />
                            <label>Stock mínimo: &nbsp;</label>
                            <input type="number" value={selectedProduct?.minStock} onChange={e => setEditMinStock(e.target.value)} />
                            <label>Ubicación: &nbsp;</label>
                            <input type="text" value={selectedProduct?.location} onChange={e => setEditLocation(e.target.value)} />
                            <label>Precio de compra: &nbsp;</label>
                            <input type="number" value={selectedProduct?.purchasePrize} onChange={e => setEditPurchasePrize(e.target.value)} />
                            <label>Precio de venta: &nbsp;</label>
                            <input type="number" value={selectedProduct?.sellPrize} onChange={e => setEditSellPrize(e.target.value)} />
                        
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
                            <input type="text" onChange={e => setAddName(e.target.value)} />
                            <label>Descripción: &nbsp;</label>
                            <input type="text" onChange={e => setAddDescription(e.target.value)} />
                            <label>Stock: &nbsp;</label>
                            <input type="number" onChange={e => setAddStock(e.target.value)} />
                            <label>Stock máximo: &nbsp;</label>
                            <input type="number" onChange={e => setAddMaxStock(e.target.value)} />
                            <label>Stock mínimo: &nbsp;</label>
                            <input type="number" onChange={e => setAddMinStock(e.target.value)} />
                            <label>Ubicación: &nbsp;</label>
                            <input type="text" onChange={e => setAddLocation(e.target.value)} />
                            <label>Precio de compra: &nbsp;</label>
                            <input type="number" onChange={e => setAddPurchasePrize(e.target.value)} />
                            <label>Precio de venta: &nbsp;</label>
                            <input type="number" onChange={e => setAddSellPrize(e.target.value)} />

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