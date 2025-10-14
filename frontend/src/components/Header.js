import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <span className="logo-icon">🛍️</span>
          <h1>Product Recommender</h1>
        </div>
        <p className="tagline">AI-Powered Shopping Assistant</p>
      </div>
    </header>
  );
}

export default Header;
