    import React from 'react'
    import ReactDOM from 'react-dom/client'
    import App from './App.jsx' // Importa o componente principal
    
    // Pega a 'root' do HTML e manda o React renderizar o componente 'App'
    ReactDOM.createRoot(document.getElementById('root')).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
    )
    
