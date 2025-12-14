import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [sweets, setSweets] = useState([]);
  const [search, setSearch] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [showLogin, setShowLogin] = useState(!token);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [newSweet, setNewSweet] = useState({ name: '', category: '', price: '', quantity: '' });
  const [editing, setEditing] = useState(null);

  useEffect(() => {
    if (token) {
      loadSweets();
      checkAdmin();
    }
  }, [token]);

  const checkAdmin = async () => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      setIsAdmin(payload.admin || false);
    } catch {
      setIsAdmin(false);
    }
  };

  const loadSweets = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/sweets`);
      setSweets(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_BASE}/api/auth/login`, { username, password });
      setToken(res.data.access_token);
      localStorage.setItem('token', res.data.access_token);
      setShowLogin(false);
      checkAdmin();
      loadSweets();
    } catch (err) {
      alert('Login failed');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE}/api/auth/register`, { username, password });
      alert('Registered successfully');
    } catch (err) {
      alert('Registration failed');
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    setSweets([]);
    setIsAdmin(false);
    setShowLogin(true);
  };

  const handleSearch = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/sweets/search?name=${search}`);
      setSweets(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handlePurchase = async (id) => {
    try {
      await axios.post(`${API_BASE}/api/sweets/${id}/purchase`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadSweets();
    } catch (err) {
      alert('Purchase failed');
    }
  };

  const handleAddSweet = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE}/api/sweets`, newSweet, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNewSweet({ name: '', category: '', price: '', quantity: '' });
      loadSweets();
    } catch (err) {
      alert('Add failed');
    }
  };

  const handleUpdateSweet = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`${API_BASE}/api/sweets/${editing.id}`, editing, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEditing(null);
      loadSweets();
    } catch (err) {
      alert('Update failed');
    }
  };

  const handleDeleteSweet = async (id) => {
    if (!window.confirm('Delete sweet?')) return;
    try {
      await axios.delete(`${API_BASE}/api/sweets/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadSweets();
    } catch (err) {
      alert('Delete failed');
    }
  };

  if (showLogin) {
    return (
      <div className="login">
        <h1>Sweet Shop</h1>
        <form onSubmit={handleLogin}>
          <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
          <button type="submit">Login</button>
        </form>
        <form onSubmit={handleRegister}>
          <button type="submit">Register</button>
        </form>
      </div>
    );
  }

  return (
    <div className="app">
      <header>
        <h1>Sweet Shop</h1>
        <button onClick={handleLogout}>Logout</button>
      </header>
      <div className="search">
        <input type="text" placeholder="Search sweets" value={search} onChange={e => setSearch(e.target.value)} />
        <button onClick={handleSearch}>Search</button>
        <button onClick={loadSweets}>Show All</button>
      </div>
      {isAdmin && (
        <form onSubmit={handleAddSweet} className="add-form">
          <input type="text" placeholder="Name" value={newSweet.name} onChange={e => setNewSweet({...newSweet, name: e.target.value})} required />
          <input type="text" placeholder="Category" value={newSweet.category} onChange={e => setNewSweet({...newSweet, category: e.target.value})} required />
          <input type="number" step="0.01" placeholder="Price" value={newSweet.price} onChange={e => setNewSweet({...newSweet, price: e.target.value})} required />
          <input type="number" placeholder="Quantity" value={newSweet.quantity} onChange={e => setNewSweet({...newSweet, quantity: e.target.value})} required />
          <button type="submit">Add Sweet</button>
        </form>
      )}
      <div className="sweets">
        {sweets.map(sweet => (
          <div key={sweet.id} className="sweet">
            <h3>{sweet.name}</h3>
            <p>Category: {sweet.category}</p>
            <p>Price: ${sweet.price}</p>
            <p>Quantity: {sweet.quantity}</p>
            <button onClick={() => handlePurchase(sweet.id)} disabled={sweet.quantity === 0}>Purchase</button>
            {isAdmin && (
              <div className="admin-actions">
                <button onClick={() => setEditing(sweet)}>Edit</button>
                <button onClick={() => handleDeleteSweet(sweet.id)}>Delete</button>
              </div>
            )}
          </div>
        ))}
      </div>
      {editing && (
        <form onSubmit={handleUpdateSweet} className="edit-form">
          <input type="text" value={editing.name} onChange={e => setEditing({...editing, name: e.target.value})} required />
          <input type="text" value={editing.category} onChange={e => setEditing({...editing, category: e.target.value})} required />
          <input type="number" step="0.01" value={editing.price} onChange={e => setEditing({...editing, price: e.target.value})} required />
          <input type="number" value={editing.quantity} onChange={e => setEditing({...editing, quantity: e.target.value})} required />
          <button type="submit">Update</button>
          <button onClick={() => setEditing(null)}>Cancel</button>
        </form>
      )}
    </div>
  );
}

export default App;