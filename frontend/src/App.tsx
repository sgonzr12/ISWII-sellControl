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

  // Verificar si hay credenciales almacenadas al cargar la aplicación
  useEffect(() => {
    const checkAuthStatus = () => {
      try {
        const credential = localStorage.getItem('credential');
        if (credential) {
          // Opcionalmente, validar el token
          try {
            const decoded = jwtDecode(credential);
            // Verificar si el token está expirado
            const currentTime = Date.now() / 1000;

            // Si exp es una cadena de fecha ISO, conviértela a timestamp
            let expTime = decoded.exp;
            if (typeof decoded.exp === 'string') {
              expTime = new Date(decoded.exp).getTime() / 1000;
            }

            if (expTime && expTime > currentTime) {
              setIsAuthenticated(true);
            } else {
              // Token expirado
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

  // Mostrar un indicador de carga mientras se verifica la autenticación
  if (isLoading) {
    return <div>Cargando...</div>;
  }



    const backendData = JSON.parse(localStorage.getItem('backendData') || '{}');
    const rol = Number(backendData.rol) || -1; 



  return (
    <BrowserRouter>
      {isAuthenticated && <Navbar setIsAuthenticated={setIsAuthenticated} />}
      <Routes>
        {/* Ruta pública - con redirección si ya está autenticado */}
        <Route 
          path="/" 
          element={
            isAuthenticated 
              ? <Navigate to="/home" replace /> 
              : <Landing setIsAuthenticated={setIsAuthenticated} />
          } 
        />
  
        {/* Rutas protegidas */}
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
        
        {/* Ruta 404 para manejar todas las rutas no definidas - debe ser la última */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
