import './Navbar.css';
import logo from '../images/logo.png';
import { Link, useNavigate } from 'react-router-dom';

interface NavbarProps {
  setIsAuthenticated: (value: boolean) => void;
}

function Navbar({ setIsAuthenticated }: NavbarProps) {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    // Delete the credential from local storage
    localStorage.removeItem('credential');
    
    // Update authentication state
    setIsAuthenticated(false);
    
    // Cerrar sesión de Google
    const googleLogoutUrl = 'https://accounts.google.com/logout';
    
    // Create an iframe to perform the logout
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = googleLogoutUrl;
    document.body.appendChild(iframe);
    
    // Redirect to the home page after logout
    navigate('/');
    
    // Clean up the iframe after a short delay
    setTimeout(() => {
      document.body.removeChild(iframe);
    }, 1000);
  };
  
  const navigateToHome = () => {
    navigate('/home');
  };

  return (
    <nav className="navbar">
      <div className="logo-container" onClick={navigateToHome} style={{ cursor: 'pointer' }}>
        <img src={logo} alt="Logo" className="logo" />
        <h2>SellControl</h2>
      </div>
      <ul className="nav-links">
        <li><Link to="/product">Producto</Link></li>
        <li><Link to="/offer">Oferta</Link></li>
        <li><Link to="/order">Pedido</Link></li>
        <li><Link to="/deliverynote">Albarán</Link></li>
        <li><Link to="/invoice">Factura</Link></li>
      </ul>
      <button className="login-button" onClick={handleLogout}>
        Cerrar sesión
      </button>
    </nav>
  );
}

export default Navbar;