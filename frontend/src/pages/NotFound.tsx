import { Link } from 'react-router-dom';
import './NotFound.css';

function NotFound() {
  return (
    <div className="not-found-container">
      <h1>404</h1>
      <h2>Página no encontrada</h2>
      <p>Lo sentimos, la página que estás buscando no existe o no está disponible actualmente.</p>
      <Link to="/home" className="back-button">
        Volver al inicio
      </Link>
    </div>
  );
}

export default NotFound;