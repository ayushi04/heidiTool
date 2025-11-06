import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const DynamicDiagram = ({ data }) => {
  const svgRef = useRef();

  useEffect(() => {
    // Clear any previous content
    d3.select(svgRef.current).selectAll('*').remove();

    const width = 1000; // Increased width for wider links
    const height = 800; // Adjust height to provide enough space
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    // Create the main circles for C1 and C2
    svg.append('circle')
      .attr('cx', 200) // Adjusted position to give more space
      .attr('cy', height / 2)
      .attr('r', 40)
      .attr('fill', 'orange')
      .attr('stroke', 'black')
      .attr('stroke-width', 2);

    svg.append('circle')
      .attr('cx', width - 200)
      .attr('cy', height / 2)
      .attr('r', 40)
      .attr('fill', 'orange')
      .attr('stroke', 'black')
      .attr('stroke-width', 2);

    // Text labels for C1 and C2
    svg.append('text')
      .attr('x', 200)
      .attr('y', height / 2)
      .attr('text-anchor', 'middle')
      .attr('dy', '.35em')
      .attr('font-size', '16px')
      .attr('fill', 'black')
      .text('C1');

    svg.append('text')
      .attr('x', width - 200)
      .attr('y', height / 2)
      .attr('text-anchor', 'middle')
      .attr('dy', '.35em')
      .attr('font-size', '16px')
      .attr('fill', 'black')
      .text('C2');

    // Adjust spacing and layout for subtypes dynamically
    const subtypeSpacing = height / (data.length + 1); // Dynamic spacing based on number of subtypes

    // Draw Subtypes as diamonds and connect them dynamically with straight links
    data.forEach((subtype, index) => {
      const xPos = width / 2; // Center x position for all subtypes
      const yPos = (index + 1) * subtypeSpacing; // Adjusted vertical position

      // Draw diamond (rhombus) for each subtype
      svg.append('polygon')
        .attr('points', `${xPos},${yPos-40} ${xPos+40},${yPos} ${xPos},${yPos+40} ${xPos-40},${yPos}`)
        .attr('fill', 'lightblue')
        .attr('stroke', 'black')
        .attr('stroke-width', 2);

      // Text label for the subtype
      svg.append('text')
        .attr('x', xPos)
        .attr('y', yPos)
        .attr('text-anchor', 'middle')
        .attr('dy', '.35em')
        .attr('font-size', '14px')
        .attr('fill', 'black')
        .text(subtype.subspace);

      // Straight link from C1 to Subtype
      svg.append('line')
        .attr('x1', 240) // C1 adjusted position
        .attr('y1', height / 2)
        .attr('x2', xPos - 40) // Left side of the diamond
        .attr('y2', yPos)
        .attr('stroke', 'orange')
        .attr('stroke-width', 4); // Thicker stroke for better visibility

      // Straight link from Subtype to C2
      svg.append('line')
        .attr('x1', xPos + 40) // Right side of the diamond
        .attr('y1', yPos)
        .attr('x2', width - 240) // C2 adjusted position
        .attr('y2', height / 2)
        .attr('stroke', 'orange')
        .attr('stroke-width', 4); // Thicker stroke for better visibility

      // Add percentage text for C1 to Subtype
      svg.append('text')
        .attr('x', (240 + (xPos - 40)) / 2) // Midpoint of the line between C1 and Subtype
        .attr('y', (height / 2 + yPos) / 2 - 10) // Slightly above the line
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', 'black')
        .text(`${subtype.percentage_rowPoints}%`);

      // Add percentage text for Subtype to C2
      svg.append('text')
        .attr('x', ((xPos + 40) + (width - 240)) / 2) // Midpoint of the line between Subtype and C2
        .attr('y', (height / 2 + yPos) / 2 - 10) // Slightly above the line
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', 'black')
        .text(`${subtype.percentage_colPoints}%`);
    });

  }, [data]);

  return <svg ref={svgRef}></svg>;
};

export default DynamicDiagram;