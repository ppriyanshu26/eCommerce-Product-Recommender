import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import UserSelector from './components/UserSelector';
import UserActivity from './components/UserActivity';
import Recommendations from './components/Recommendations';
import Header from './components/Header';

const API_URL = 'http://127.0.0.1:5000';

function App() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userBehavior, setUserBehavior] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch users on component mount
  useEffect(() => {
    fetchUsers();
  }, []);

  // Fetch user data when selected user changes
  useEffect(() => {
    if (selectedUser) {
      fetchUserData(selectedUser);
    }
  }, [selectedUser]);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_URL}/users`);
      setUsers(response.data);
      if (response.data.length > 0) {
        setSelectedUser(response.data[0].user_id);
      }
    } catch (err) {
      setError('Failed to fetch users. Please ensure the backend is running.');
      console.error('Error fetching users:', err);
    }
  };

  const fetchUserData = async (userId) => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch user behavior and recommendations in parallel
      const [behaviorRes, recommendationsRes] = await Promise.all([
        axios.get(`${API_URL}/user_behavior?user_id=${userId}`),
        axios.get(`${API_URL}/recommendations?user_id=${userId}`)
      ]);
      
      setUserBehavior(behaviorRes.data);
      setRecommendations(recommendationsRes.data);
    } catch (err) {
      setError('Failed to fetch user data. Please try again.');
      console.error('Error fetching user data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUserChange = (userId) => {
    setSelectedUser(userId);
  };

  return (
    <div className="App">
      <Header />
      
      <div className="container">
        <UserSelector 
          users={users} 
          selectedUser={selectedUser} 
          onUserChange={handleUserChange}
        />

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading data...</p>
          </div>
        ) : (
          <>
            {userBehavior && (
              <UserActivity behavior={userBehavior} />
            )}
            
            {recommendations.length > 0 && (
              <Recommendations recommendations={recommendations} />
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
