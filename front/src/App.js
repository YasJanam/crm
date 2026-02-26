import logo from './logo.svg';
import './App.css';
import { Routes, Route } from 'react-router-dom';

import LoginPage from './common_components/login';
import RegisterPage from './common_components/register';

import AdminSidebar from './admin/admin_sidebar';
import ManagerSidebar from './manager/manager_sidebar';
import SalerSidebar from './saler/saler_sidebar';


function App() {
  return (
    <Routes>

      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route path="/adminpanel" element={<AdminSidebar />} />
      <Route path="/managerpanel" element={<ManagerSidebar />} />
      <Route path="/salerpanel" element={<SalerSidebar />} />

    </Routes>
  )
}

export default App;
