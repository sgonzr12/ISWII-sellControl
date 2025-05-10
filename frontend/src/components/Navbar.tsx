import './Navbar.css';
import logo from '../images/logo.png';
import { Link, useNavigate } from 'react-router-dom';

import { googleLogout } from '@react-oauth/google';

interface NavbarProps {
  setIsAuthenticated: (value: boolean) => void;
}

function Navbar({ setIsAuthenticated }: NavbarProps) {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    // Clear local storage
    localStorage.removeItem('credential');
    
    // Update authentication state
    setIsAuthenticated(false);
    
    // Use the official method
    googleLogout();
    
    // Redirect to home page
    navigate('/');
  };
  
  const navigateToHome = () => {
    navigate('/home');
  };


  const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
  const rol = Number(backendData.rol) || -1; 

  return (
    <nav className="navbar">
      <div className="logo-container" onClick={navigateToHome} style={{ cursor: 'pointer' }}>
      <img src={logo} alt="Logo" className="navbar-logo" />
        <h2>SellControl</h2>
      </div>
      <ul className="nav-links">
        <li><Link to="/product">Producto</Link></li>
        <li><Link to="/offer">Oferta</Link></li>
        <li><Link to="/order">Pedido</Link></li>
        <li><Link to="/deliverynote">Albarán</Link></li>
        <li><Link to="/invoice">Factura</Link></li>
        <li><Link to="/client">Clientes</Link></li>
        {rol === 1 && (<li><Link to="/administrator">Administración</Link></li>)}
        
      </ul>
      <button className="login-button" onClick={handleLogout}>
        Cerrar sesión
      </button>
    </nav>
  );
}

export default Navbar;