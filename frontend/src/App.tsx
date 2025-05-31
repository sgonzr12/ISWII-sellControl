import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Landing from './pages/Landing';
import Home from './pages/Home';
import Administrator from './pages/Administrator';
import Client from './pages/Client';
import Product from './pages/Product';
import Offer from './pages/offer/Offer';
import CreateOffer from './pages/offer/CreateOffer';
import EditOffer from './pages/offer/EditOffer';
import Order from './pages/Order';

import Invoice from './pages/Invoice';
import DeliveryNote from './pages/DeliveryNote';
import NotFound from './pages/NotFound';
import ProtectedRoutes from './components/ProtectedRoutes';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import { jwtDecode } from 'jwt-decode';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Check if there are stored credentials when the application loads.
  useEffect(() => {
    const checkAuthStatus = () => {
      try {
        const credential = localStorage.getItem('credential');
        if (credential) {
          // Optionally, validate the token.
          try {
            const decoded = jwtDecode(credential);
            // Verify if token has expired
            const currentTime = Date.now() / 1000;

            // Convert iso to timestamp
            let expTime = decoded.exp;
            if (typeof decoded.exp === 'string') {
              expTime = new Date(decoded.exp).getTime() / 1000;
            }

            if (expTime && expTime > currentTime) {
              setIsAuthenticated(true);
            } else {
              // Expired token
              console.log('Token expirado');
              localStorage.removeItem('credential');
              setIsAuthenticated(false);
            }
          } catch (error) {
            console.error('Error al decodificar el token:', error);
            localStorage.removeItem('credential');
            setIsAuthenticated(false);
          }
        }
      } finally {
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  // Show charging indicator
  if (isLoading) {
    return <div>Cargando...</div>;
  }



    const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
    const rol = Number(backendData.rol) || -1; 



  return (
    <BrowserRouter>
      {isAuthenticated && <Navbar setIsAuthenticated={setIsAuthenticated} />}
      <Routes>
        {/* Public route – with redirect if already authenticated. */}
        <Route 
          path="/" 
          element={
            isAuthenticated 
              ? <Navigate to="/home" replace /> 
              : <Landing setIsAuthenticated={setIsAuthenticated} />
          } 
        />
  
        {/* Protected routes */}
        <Route element={<ProtectedRoutes isAuthenticated={isAuthenticated} />}>

          <Route path="/home" element={<Home />} />

          {(rol === 1 || rol === 2 || rol === 3 || rol === 4) && <Route path="/product" element={<Product />} />}

          {(rol === 1 || rol === 2 || rol === 3) && <Route path="/offer" element={<Offer />} />}

          {(rol === 1 || rol === 2 || rol === 3) && <Route path="/createoffer" element={<CreateOffer />} />}
          
          {(rol === 1 || rol === 2 || rol === 3) && <Route path="/editoffer" element={<EditOffer />} />}
          
          {(rol === 1 || rol === 2 || rol === 3 || rol === 4) && <Route path="/order" element={<Order />} />}

          {(rol === 1 || rol === 2 || rol === 4) && <Route path="/deliverynote" element={<DeliveryNote />} />}

          {(rol === 1 || rol === 2 || rol === 3) && <Route path="/invoice" element={<Invoice />} />}

          {(rol === 1 || rol === 2 || rol === 3) && <Route path="/client" element={<Client />} />}

          {(rol === 1) && <Route path="/administrator" element={<Administrator />} />}

        </Route>
        
        {/* 404 Route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
