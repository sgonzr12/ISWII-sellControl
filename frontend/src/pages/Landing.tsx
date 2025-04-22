import './Landing.css';
import { GoogleLogin } from '@react-oauth/google'; //googleLogout
import { jwtDecode } from 'jwt-decode'; // Importación corregida
import { useNavigate } from 'react-router-dom';

export default function Landing() { // Cambiado a exportación por defecto

  const navigate = useNavigate(); // Inicializa el hook useNavigate

//   function handleLogOut() {
//     googleLogout(); // Cierra sesión de Google
//     console.log("Logout Success"); // Mensaje de éxito en la consola
//   }

  return (
    <div className="landing-container">
      <h1>Bienvenido</h1>
      <p>Por favor, inicia sesión para continuar.</p>
      <GoogleLogin 
        onSuccess={(credentialResponse) => {
          console.log(credentialResponse);
          if (credentialResponse.credential) {
            const decoded = jwtDecode(credentialResponse.credential); // Decodifica el token JWT
            console.log(decoded);
            navigate("/home"); // Navega a la ruta "/home"
          } else {
            console.error("Credential is undefined");
          }
        }}
        onError={() => {
          console.log("Login Failed")}}
          auto_select={true}/>
    </div>
  );
}