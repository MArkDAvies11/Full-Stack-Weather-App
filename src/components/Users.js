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
      const response = await fetch('http://localhost:5000/api/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleSubmit = async (values, { resetForm }) => {
    try {
      const url = editingUser 
        ? `http://localhost:5000/api/users/${editingUser.id}`
        : 'http://localhost:5000/api/users';
      
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
      }
    } catch (error) {
      console.error('Error saving user:', error);
    }
  };

  const handleDelete = async (userId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/users/${userId}`, {
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
        {users.map(user => (
          <div key={user.id} className="user-card">
            <h3>{user.username}</h3>
            <p>{user.email}</p>
            <div className="user-actions">
              <button onClick={() => setEditingUser(user)}>Edit</button>
              <button onClick={() => handleDelete(user.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Users;