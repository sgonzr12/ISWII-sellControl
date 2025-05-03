import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',   // <- Escucha en todas las IPs (no solo localhost)
    port: 5173,        // <- Asegúrate de que esté abierto
    strictPort: true,  // <- Si el 5173 está ocupado, falla (útil para debugging)
    cors: true         // <- Activa CORS por si se conecta un backend externo
  }
})
