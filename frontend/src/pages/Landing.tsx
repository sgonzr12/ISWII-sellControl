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
        <GoogleLogin
        onSuccess={(credentialResponse) => {
          if (credentialResponse.credential) {

            const token = jwtDecode(credentialResponse.credential);

              if (token) {
                //const decodedToken = jwtDecode(token);
                console.log('Decoded JWT:', token);
                localStorage.setItem('credential', credentialResponse.credential);
                setIsAuthenticated(true);

                // Realizar petición fetch al backend
                fetch('http://aperturelab.ignorelist.com:8000/user', {
                  headers: {
                    Authorization: `Bearer ${credentialResponse.credential}`
                  }
                })
                  .then(response => {
                    if (!response.ok) {
                      throw new Error('Network response was not ok');
                    }
                    return response.json();
                  })
                  .then(data => {
                    // Almacenar la respuesta en localStorage
                    localStorage.setItem('backendData', JSON.stringify(data));
                    console.log('Data from backend:', data);
                    
                    // Navegar a home después de recibir la respuesta
                    navigate('/home');
                  })
                  .catch(error => {
                    console.error('Error fetching data from backend:', error);
                    // Navegar a home incluso si hay un error
                    //navigate('/home');
                  });
              } else {
                alert('Login failed. Please try again.');
            }
          }
        }}
        />
      </div>
    </div>
  );
}