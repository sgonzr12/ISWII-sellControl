import './Product.css';
import { useState, useEffect} from 'react';

function Product() {
    const [products, setProducts] = useState<{productId: string; name: string; description: string; stock: number; maxStock: number; minStock: number; location: string; purchasePrice: number; sellPrice: number }[]>([]);
    const [selectedProduct, setSelectedProduct] = useState<{productId: string; name: string; description: string; stock: number; maxStock: number; minStock: number; location: string; purchasePrice: number; sellPrice: number } | null>(null);

    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [addName, setAddName] = useState('');
    const [addDescription, setAddDescription] = useState('');
    const [addStock, setAddStock] = useState('');
    const [addMaxStock, setAddMaxStock] = useState('');
    const [addMinStock, setAddMinStock] = useState('');
    const [addLocation, setAddLocation] = useState('');
    const [addPurchasePrice, setAddPurchasePrice] = useState('');
    const [addSellPrice, setAddSellPrice] = useState('');

    const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
    const [editStock, setEditStock] = useState('');
    const [editMaxStock, setEditMaxStock] = useState('');
    const [editMinStock, setEditMinStock] = useState('');
    const [editLocation, setEditLocation] = useState('');
    const [editPurchasePrice, setEditPurchasePrice] = useState('');
    const [editSellPrice, setEditSellPrice] = useState('');

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

    const handleSelectProduct = (product: {productId: string; name: string; description: string; stock: number; maxStock: number; minStock: number; location: string; purchasePrice: number; sellPrice: number }) => {
        setSelectedProduct(product);
    }

    const handleEditClick = () => {
        if (selectedProduct) {
            setEditStock(selectedProduct.stock.toString());
            setEditMaxStock(selectedProduct.maxStock.toString());
            setEditMinStock(selectedProduct.minStock.toString());
            setEditLocation(selectedProduct.location);
            setEditPurchasePrice(selectedProduct.purchasePrice.toString());
            setEditSellPrice(selectedProduct.sellPrice.toString());
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
            setAddPurchasePrice(selectedProduct.purchasePrice.toString());
            setAddSellPrice(selectedProduct.sellPrice.toString());
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
                    stock: editStock,
                    maxStock: editMaxStock,
                    minStock: editMinStock,
                    location: editLocation,
                    purchasePrice: editPurchasePrice,
                    sellPrice: editSellPrice,
                }),
            });

            if (!response.ok) {
                throw new Error('Error updating product');
            }

            const data = await response.json();
            console.log('Updated product:', data);
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
                    location: addLocation,
                    purchasePrice: addPurchasePrice,
                    sellPrice: addSellPrice,
                }),
            });

            if (!response.ok) {
                throw new Error('Error adding product');
            }

            const data = await response.json();
            console.log('Added product:', data);
            setProducts([...products, data]);
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
                        {products.map(product => (
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
                                <p>Precio de compra: {product.purchasePrice}</p>
                                <p>Precio de venta: {product.sellPrice}</p>
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
                            <label>Stock: &nbsp;</label>
                            <input type="number" value={selectedProduct?.stock} onChange={e => setEditStock(e.target.value)}/>
                            <label>Stock máximo: &nbsp;</label>
                            <input type="number" value={selectedProduct?.maxStock} onChange={e => setEditMaxStock(e.target.value)} />
                            <label>Stock mínimo: &nbsp;</label>
                            <input type="number" value={selectedProduct?.minStock} onChange={e => setEditMinStock(e.target.value)} />
                            <label>Ubicación: &nbsp;</label>
                            <input type="text" value={selectedProduct?.location} onChange={e => setEditLocation(e.target.value)} />
                            <label>Precio de compra: &nbsp;</label>
                            <input type="number" value={selectedProduct?.purchasePrice} onChange={e => setEditPurchasePrice(e.target.value)} />
                            <label>Precio de venta: &nbsp;</label>
                            <input type="number" value={selectedProduct?.sellPrice} onChange={e => setEditSellPrice(e.target.value)} />
                        
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
                            <input type="number" onChange={e => setAddPurchasePrice(e.target.value)} />
                            <label>Precio de venta: &nbsp;</label>
                            <input type="number" onChange={e => setAddSellPrice(e.target.value)} />

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