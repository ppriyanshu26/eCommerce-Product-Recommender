import React from 'react';
import './Recommendations.css';

function Recommendations({ recommendations }) {
  return (
    <div className="recommendations">
      <div className="recommendations-header">
        <h2>✨ Recommended for You</h2>
        <p>Personalized product recommendations based on your activity</p>
      </div>

      <div className="recommendations-grid">
        {recommendations.map((rec, index) => (
          <div key={rec.product._id} className="recommendation-card">
            <div className="recommendation-badge">
              <span className="badge-number">#{index + 1}</span>
              <span className="badge-text">Top Pick</span>
            </div>
            
            <div className="recommendation-content">
              <div className="product-header">
                <h3>{rec.product.name}</h3>
                <span className="product-category">{rec.product.category}</span>
              </div>
              
              <p className="product-description">{rec.product.description}</p>
              
              <div className="explanation-section">
                <div className="explanation-header">
                  <span className="explanation-icon">💡</span>
                  <h4>Why this product?</h4>
                </div>
                <p className="explanation-text">{rec.explanation}</p>
              </div>
            </div>

            <div className="card-footer">
              <button className="action-button primary">
                <span>View Details</span>
                <span className="button-icon">→</span>
              </button>
              <button className="action-button secondary">
                <span className="button-icon">🛒</span>
                <span>Add to Cart</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recommendations;
