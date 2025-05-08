import './Landing.css';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import logo from '../images/logo.png';

interface LandingProps {
  setIsAuthenticated: (value: boolean) => void;
}

export default function Landing({ setIsAuthenticated }: LandingProps) {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="landing-content">
        <img src={logo} alt="SellControl Logo" className="landing-logo" />
        <h1>Bienvenido a SellControl</h1>
        <p>La plataforma que simplifica la gestión de ventas y control de inventario para tu negocio.</p>
        
        <div className="google-login-wrapper">
          <GoogleLogin
            onSuccess={async (credentialResponse) => {
              if (credentialResponse.credential) {
                const token = jwtDecode(credentialResponse.credential);
                console.log('Decoded token:', token);

                if (token) {
                  try {
                    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/user`, {
                      headers: {
                        Authorization: `Bearer ${credentialResponse.credential}`
                      }
                    });
                    if (!response.ok) {
                      throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    // Solo aquí almacena la credencial y autentica
                    localStorage.setItem('credential', credentialResponse.credential);
                    setIsAuthenticated(true);
                    localStorage.setItem('backendData', JSON.stringify(data));
                    console.log('Data from backend:', data);
                    navigate('/home');
                  } catch (error) {
                    console.error('Error fetching data from backend:', error);
                    alert('No se pudo autenticar con el backend.');
                  }
                } else {
                  alert('Login failed. Please try again.');
                }
              }
            }}
          />
        </div>
      </div>
    </div>
  );
}