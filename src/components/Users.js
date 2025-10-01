import React, { useState, useEffect } from 'react';
import UserForm from '../forms/UserForm';

function Users() {
  const [users, setUsers] = useState([]);
  const [editingUser, setEditingUser] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleSubmit = async (values, { resetForm }) => {
    try {
      const url = editingUser 
        ? `/api/users/${editingUser.id}`
        : '/api/users';
      
      const method = editingUser ? 'PATCH' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });

      if (response.ok) {
        fetchUsers();
        resetForm();
        setEditingUser(null);
      } else {
        const error = await response.json();
        alert(error.error || 'Error saving user');
      }
    } catch (error) {
      console.error('Error saving user:', error);
      alert('Error saving user');
    }
  };

  const handleDelete = async (userId) => {
    try {
      const response = await fetch(`/api/users/${userId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchUsers();
      }
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  return (
    <div className="container">
      <h2>User Management</h2>
      
      <UserForm 
        onSubmit={handleSubmit}
        editingUser={editingUser}
        onCancel={() => setEditingUser(null)}
      />

      <div className="users-list">
        {users.length === 0 ? (
          <p style={{color: 'white', textAlign: 'center'}}>No users created yet.</p>
        ) : (
          users.map(user => (
            <div key={user.id} className="user-card">
              <h3>{user.username}</h3>
              <p>{user.email}</p>
              <p>Created: {new Date(user.created_at).toLocaleDateString()}</p>
              <div className="user-actions">
                <button onClick={() => setEditingUser(user)}>Edit</button>
                <button onClick={() => handleDelete(user.id)} className="delete-button">Delete</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Users;