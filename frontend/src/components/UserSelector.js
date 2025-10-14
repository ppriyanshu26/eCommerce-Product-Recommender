import React from 'react';
import './UserSelector.css';

function UserSelector({ users, selectedUser, onUserChange }) {
  return (
    <div className="user-selector-container">
      <div className="selector-card">
        <div className="selector-header">
          <span className="selector-icon">👤</span>
          <h2>Select User</h2>
        </div>
        <select 
          className="user-select"
          value={selectedUser || ''}
          onChange={(e) => onUserChange(e.target.value)}
        >
          {users.map(user => (
            <option key={user.user_id} value={user.user_id}>
              {user.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default UserSelector;
