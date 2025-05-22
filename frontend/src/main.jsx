import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
// Garanta que as dependências estão sendo importadas corretamente
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { format } from 'date-fns';
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
    <ToastContainer />
  </React.StrictMode>
)