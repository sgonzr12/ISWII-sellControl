import './Home.css';

function Home() {
  return (
    <div className="Home">
      <main className="main-content">
        <div className="home">
          <h1>Bienvenido a SellControl</h1>
          <p>
            Esta plataforma te permite gestionar ofertas, pedidos, albaranes y facturas de forma sencilla y eficiente.
          </p>
          <p>
            Si es la primera vez que te registras, recuerda que necesitarás que un administrador te asigne un rol para poder acceder a todas las funcionalidades del sistema.
            Ponte en contacto con un administrador para completar tu registro y comenzar a utilizar SellControl sin restricciones.
          </p>
          <p>
            ¡Gracias por confiar en nosotros!
          </p>
        </div>
      </main>
    </div>
  );
}

export default Home;