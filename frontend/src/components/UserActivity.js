import React from 'react';
import './UserActivity.css';

function UserActivity({ behavior }) {
  const activities = [
    { 
      key: 'viewed', 
      title: 'Recently Viewed', 
      icon: '👁️',
      color: '#3b82f6',
      items: behavior.viewed 
    },
    { 
      key: 'added_to_cart', 
      title: 'Added to Cart', 
      icon: '🛒',
      color: '#f59e0b',
      items: behavior.added_to_cart 
    },
    { 
      key: 'purchased', 
      title: 'Purchased', 
      icon: '✅',
      color: '#10b981',
      items: behavior.purchased 
    }
  ];

  return (
    <div className="user-activity">
      <div className="activity-header">
        <h2>📊 User Dashboard</h2>
        <p>Recent activity and interactions</p>
      </div>
      
      <div className="activity-grid">
        {activities.map(activity => (
          <div key={activity.key} className="activity-section">
            <div className="activity-title" style={{ borderLeftColor: activity.color }}>
              <span className="activity-icon">{activity.icon}</span>
              <h3>{activity.title}</h3>
              <span className="activity-count">{activity.items.length}</span>
            </div>
            
            <div className="products-container">
              {activity.items.length === 0 ? (
                <p className="no-products">No products in this category</p>
              ) : (
                activity.items.map(product => (
                  <div key={product._id} className="product-mini-card">
                    <div className="product-mini-header">
                      <h4>{product.name}</h4>
                      <span className="category-badge">{product.category}</span>
                    </div>
                    <p className="product-mini-description">{product.description}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default UserActivity;
