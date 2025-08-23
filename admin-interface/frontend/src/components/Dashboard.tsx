import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  username: string;
}

interface Source {
  id: number;
  name: string;
  type: string;
  url: string;
  is_active: boolean;
}

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ user, onLogout }) => {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newSource, setNewSource] = useState({
    name: '',
    type: 'youtube',
    url: ''
  });

  const getAuthHeaders = () => ({
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  });

  const fetchSources = async () => {
    try {
      const response = await axios.get('http://localhost:8000/sources', {
        headers: getAuthHeaders()
      });
      setSources(response.data);
    } catch (error) {
      console.error('Failed to fetch sources:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSources();
  }, []);

  const handleAddSource = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/sources', newSource, {
        headers: getAuthHeaders()
      });
      setNewSource({ name: '', type: 'youtube', url: '' });
      setShowAddForm(false);
      fetchSources();
    } catch (error) {
      console.error('Failed to add source:', error);
    }
  };

  const handleDeleteSource = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this source?')) {
      try {
        await axios.delete(`http://localhost:8000/sources/${id}`, {
          headers: getAuthHeaders()
        });
        fetchSources();
      } catch (error) {
        console.error('Failed to delete source:', error);
      }
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Grundrisse Admin Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user.username}</span>
          <button onClick={onLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <main className="dashboard-content">
        <section className="sources-section">
          <div className="section-header">
            <h2>Content Sources</h2>
            <button 
              onClick={() => setShowAddForm(!showAddForm)}
              className="add-btn"
            >
              {showAddForm ? 'Cancel' : 'Add Source'}
            </button>
          </div>

          {showAddForm && (
            <form onSubmit={handleAddSource} className="add-source-form">
              <div className="form-group">
                <label htmlFor="name">Name:</label>
                <input
                  type="text"
                  id="name"
                  value={newSource.name}
                  onChange={(e) => setNewSource({...newSource, name: e.target.value})}
                  required
                  placeholder="e.g., Tech Channel"
                />
              </div>
              <div className="form-group">
                <label htmlFor="type">Type:</label>
                <select
                  id="type"
                  value={newSource.type}
                  onChange={(e) => setNewSource({...newSource, type: e.target.value})}
                >
                  <option value="youtube">YouTube</option>
                  <option value="rss">RSS</option>
                  <option value="podcast">Podcast</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="url">URL:</label>
                <input
                  type="url"
                  id="url"
                  value={newSource.url}
                  onChange={(e) => setNewSource({...newSource, url: e.target.value})}
                  required
                  placeholder="https://www.youtube.com/channel/..."
                />
              </div>
              <button type="submit">Add Source</button>
            </form>
          )}

          {loading ? (
            <div>Loading sources...</div>
          ) : (
            <div className="sources-list">
              {sources.length === 0 ? (
                <p>No sources added yet. Click "Add Source" to get started.</p>
              ) : (
                sources.map(source => (
                  <div key={source.id} className="source-item">
                    <div className="source-info">
                      <h3>{source.name}</h3>
                      <p className="source-type">{source.type.toUpperCase()}</p>
                      <p className="source-url">{source.url}</p>
                      <p className={`source-status ${source.is_active ? 'active' : 'inactive'}`}>
                        {source.is_active ? 'Active' : 'Inactive'}
                      </p>
                    </div>
                    <div className="source-actions">
                      <button 
                        onClick={() => handleDeleteSource(source.id)}
                        className="delete-btn"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
};

export default Dashboard;