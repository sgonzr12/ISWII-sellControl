import './Home.css';
import logo from '../images/logo.png';


function Home() {
    return (
    <div className="Home">
        <nav className="navbar">
        <div className="logo-container">
            <img src={logo} alt="Logo" className="logo" />
            <h2>SellControl</h2>
        </div>
        <ul className="nav-links">
        </ul>
        <button className="login-button">
            Iniciar Sesión
        </button>
        </nav>
        <main className="main-content">
        <div className="home">
        <h1>Bienvenido a SellControl</h1>
        <p>Haga click en iniciar sesión.</p>
        </div>
        </main>
    </div>
    );
  }
  
  export default Home;