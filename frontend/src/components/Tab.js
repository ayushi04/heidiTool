import React from 'react';

const Tab = ({ activeTab, onTabChange }) => (
    <ul className="nav nav-tabs">
        <li className={`nav-item`}>
        <button
            className={`nav-link ${activeTab === 'image' ? 'active' : ''}`}
            onClick={() => onTabChange('image')}
        >
            Image
        </button>
        </li>
        <li className={`nav-item`}>
        <button
            className={`nav-link ${activeTab === 'consolidated' ? 'active' : ''}`}
            onClick={() => onTabChange('consolidated')}
        >
            Consolidated Image
        </button>
        </li>
  </ul>
);

export default Tab;
