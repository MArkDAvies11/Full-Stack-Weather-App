import React, { useState, useEffect } from 'react';
import FavoriteForm from '../forms/FavoriteForm';

function Favorites() {
  const [favorites, setFavorites] = useState([]);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchFavorites();
    fetchUsers();
  }, []);

  const fetchFavorites = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/favorites');
      const data = await response.json();
      setFavorites(data);
    } catch (error) {
      console.error('Error fetching favorites:', error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleSubmit = async (values, { resetForm }) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/favorites', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });

      if (response.ok) {
        fetchFavorites();
        resetForm();
      } else {
        const error = await response.json();
        alert(error.error);
      }
    } catch (error) {
      console.error('Error adding favorite:', error);
    }
  };

  const handleDelete = async (favoriteId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/favorites/${favoriteId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchFavorites();
      }
    } catch (error) {
      console.error('Error deleting favorite:', error);
    }
  };

  return (
    <div className="container">
      <h2>Favorite Cities</h2>
      
      <FavoriteForm 
        onSubmit={handleSubmit}
        users={users}
      />

      <div className="favorites-list">
        {favorites.length === 0 ? (
          <p>No favorites added yet.</p>
        ) : (
          favorites.map(favorite => (
            <div key={favorite.id} className="favorite-card">
              <h3>{favorite.location?.name || 'Unknown City'}</h3>
              <p>Added by: {favorite.user?.username || 'Unknown User'}</p>
              <p>Date: {new Date(favorite.created_at).toLocaleDateString()}</p>
              <button onClick={() => handleDelete(favorite.id)} className="delete-button">
                Remove
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Favorites;