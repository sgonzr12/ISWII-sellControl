import './Landing.css';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';

interface LandingProps {
  setIsAuthenticated: (value: boolean) => void;
}

export default function Landing({ setIsAuthenticated }: LandingProps) {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <h1>Bienvenido</h1>
      <p>Por favor, inicia sesión para continuar.</p>
      <GoogleLogin
onSuccess={(credentialResponse) => {
        if (credentialResponse.credential) {

          //const decoded = jwtDecode(credentialResponse.credential);
          //console.log('Token de google:', decoded);
          
          //Envío el token al backend
          fetch(`http://192.168.1.172:8000/auth`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: credentialResponse.credential })
          })
          //Lo que me responde el backend es el awt. Este hay que decodificarlo y guardarlo en el localStorage
            .then(response => response.text())
            .then(token => {

            console.log('Respuesta completa del backend:', token);


            if (token) {
              const decodedToken = jwtDecode(token);
              console.log('Decoded JWT:', decodedToken);
              localStorage.setItem('credential', token);
              setIsAuthenticated(true);
              navigate('/home');
            } else {
              console.error('Token not received from backend');
              alert('Error al iniciar sesión. Por favor, intenta de nuevo.');
            }
            })
            .catch(error => {
            console.error('Error al contactar el backend:', error);
            alert('Error al iniciar sesión. Por favor, intenta de nuevo.');
            });
        } else {
          console.error('Credential is undefined');
        }
      }}
      />
    </div>
  );
}