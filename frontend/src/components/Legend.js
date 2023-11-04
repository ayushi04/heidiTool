import React from 'react';

const Legend = ({ legendData }) => {
    return (
        <div>
        <h2>Legend</h2>
        <table>
          <thead>
            <tr>
              <th>Color</th>
              <th>Subspace</th>
            </tr>
          </thead>
          <tbody>
            {legendData.map((item, index) => (
              <tr key={index}>
                <td>
                  <div
                    style={{
                      backgroundColor: `rgb(${item.color.join(',')})`,
                      width: '20px',
                      height: '20px',
                      marginRight: '10px',
                    }}
                  />
                </td>
                <td>{item.dimensions.toString()}</td>
              </tr>
            ))}
          </tbody>
          </table>
      </div>
    );
  };

  export default Legend;