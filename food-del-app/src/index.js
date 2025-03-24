import ReactDOM from 'react-dom/client';
import App from "./App.js"
import "./index.css";
import { HashRouter } from "react-router-dom";
import StoreContextProvider, { StoreContext } from "./context/StoreContext.js";
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <HashRouter>
    <StoreContextProvider>
      <App />
    </StoreContextProvider>
  </HashRouter>,

);
reportWebVitals();
