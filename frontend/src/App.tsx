import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Landing from './pages/Landing';
import Home from './pages/Home';
//import Product from './pages/Product';
import Administrator from './pages/Administrator';
import Client from './pages/Client';
// import Product from './pages/Product';
import Product from './pages/Product';
// import Offer from './pages/Offer';
import Offer from './pages/Offer';
// import Order from './pages/Order';
// import DeliveryNote from './pages/DeliveryNote';
// import Invoice from './pages/Invoice';
import NotFound from './pages/NotFound'; // Importa el componente NotFound
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
        <Route path="/product" element={<Product />} />
          <Route path="/home" element={<Home />} />
          {rol === 1 && <Route path="/administrator" element={<Administrator />} />}
          <Route path="/client" element={<Client />} />
          <Route path="/offer" element={<Offer />} />

         

          {/* <Route path="/product" element={<Product />} />
          <Route path="/product" element={<Product />} />
          <Route path="/order" element={<Order />} />
          <Route path="/deliverynote" element={<DeliveryNote />} />
          <Route path="/invoice" element={<Invoice />} /> */}
        </Route>
        
        {/* Ruta 404 para manejar todas las rutas no definidas - debe ser la última */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;