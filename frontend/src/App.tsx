import { HashRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import Landing from './pages/Landing';
import Home from './pages/Home';



function App() {

  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </HashRouter>
    
  );
}

export default App;

//React context: gestionar el login y el estado de la aplicación.
//recoil: alternativa a react context
//Con esto puedo gestionar el login.
//jwt: manera de gestionar autenticación y autorización en aplicaciones web.