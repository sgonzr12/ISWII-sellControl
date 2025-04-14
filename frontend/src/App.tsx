import './App.css';
import logo from './images/logo.png';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';


function App() {

  return (
    <Router>
      <div className="App">
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
          <Routes>
            <Route
              path="/"
              element={
                <div className="home">
                  <h1>Bienvenido a SellControl</h1>
                  <p>Haga click en iniciar sesión.</p>
                </div>
              }
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

//React context: gestionar el login y el estado de la aplicación.
//recoil: alternativa a react context
//Con esto puedo gestionar el login.
//jwt: manera de gestionar autenticación y autorización en aplicaciones web.