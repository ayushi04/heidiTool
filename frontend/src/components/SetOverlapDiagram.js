import React, { useRef, useEffect } from "react";
import * as d3 from "d3";
import '../css/SetOverlapDiagram.css';

const SetOverlapDiagram = ({ xPoints, yPoints, totalPoints }) => {
  const svgRef = useRef();

  useEffect(() => {
    // Clear any previous chart
    d3.select(svgRef.current).selectAll("*").remove();

    // Calculate the intersection points using Set for string-based points
    const xyPoints = [...new Set(xPoints)].filter((value) => new Set(yPoints).has(value));

    // Points that are in totalPoints but not in xPoints or yPoints (neither set)
    const pointsOutside = [...new Set(totalPoints)].filter(
      (value) => !new Set(xPoints).has(value) && !new Set(yPoints).has(value)
    );

    // Compute the sizes based on the points
    const sizeX = xPoints.length - xyPoints.length; // Unique X points
    const sizeY = yPoints.length - xyPoints.length; // Unique Y points
    const sizeOverlap = xyPoints.length; // Overlap size
    const sizeOutside = pointsOutside.length; // Points outside both sets

    // Total number of points
    const total = totalPoints.length;

    // Compute proportions based on total points
    const proportionX = sizeX / total;
    const proportionY = sizeY / total;
    const proportionOverlap = sizeOverlap / total;
    const proportionOutside = sizeOutside / total;

    // Visualization dimensions
    const width = 600,
      height = 600,
      radius = 200;

    // Create the SVG canvas
    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    // Create patterns for X, Y, and intersection of X and Y
    const defs = svg.append("defs");

    // Pattern for Set X
    defs.append("pattern")
      .attr("id", "xPattern")
      .attr("patternUnits", "userSpaceOnUse")
      .attr("width", 10)
      .attr("height", 10)
      .append("path")
      .attr("d", "M0,0 L10,10 M10,0 L0,10")
      .attr("stroke", "orange")
      .attr("stroke-width", 2);

    // Pattern for Set Y
    defs.append("pattern")
      .attr("id", "yPattern")
      .attr("patternUnits", "userSpaceOnUse")
      .attr("width", 10)
      .attr("height", 10)
      .append("path")
      .attr("d", "M5,0 L5,10 M0,5 L10,5")
      .attr("stroke", "orange")
      .attr("stroke-width", 2);

    // Pattern for Intersection of Set X and Set Y
    defs.append("pattern")
      .attr("id", "xyPattern")
      .attr("patternUnits", "userSpaceOnUse")
      .attr("width", 10)
      .attr("height", 10)
      .append("path")
      .attr("d", "M0,0 L10,10 M10,0 L0,10 M5,0 L5,10 M0,5 L10,5")
      .attr("stroke", "orange")
      .attr("stroke-width", 2);

    // Pattern for points outside both sets
    defs.append("pattern")
      .attr("id", "outsidePattern")
      .attr("patternUnits", "userSpaceOnUse")
      .attr("width", 10)
      .attr("height", 10)
      .append("path")
      .attr("d", "M0,5 L10,5 M5,0 L5,10")
      .attr("stroke", "grey")
      .attr("stroke-width", 2);

    // Create circular segments using arcs
    const arcGenerator = d3
      .arc()
      .innerRadius(0)
      .outerRadius(radius);

    const pieGenerator = d3
      .pie()
      .sort(null) // No sorting; keep order
      .value((d) => d.value);

    const data = [
      { label: "X", value: proportionX, pattern: "xPattern" },
      { label: "Y", value: proportionY, pattern: "yPattern" },
      { label: "X ∩ Y", value: proportionOverlap, pattern: "xyPattern" },
      { label: "Outside", value: proportionOutside, pattern: "outsidePattern" },
    ];

    // Create arcs for each part of the diagram
    const arcs = svg
      .append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`)
      .selectAll("path")
      .data(pieGenerator(data))
      .enter()
      .append("path")
      .attr("class", (d) => d.data.pattern)
      .attr("d", arcGenerator)
      .style("fill", (d) => `url(#${d.data.pattern})`);

    // Add legend with counts
    const legendData = [
      { label: `Set X (${sizeX})`, pattern: "xPattern" },
      { label: `Set Y (${sizeY})`, pattern: "yPattern" },
      { label: `Set X ∩ Set Y (${sizeOverlap})`, pattern: "xyPattern" },
      { label: `Outside (${sizeOutside})`, pattern: "outsidePattern" },
    ];

    const legend = svg
      .selectAll(".legend")
      .data(legendData)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr("transform", (d, i) => `translate(50, ${50 + i * 30})`);

    legend.append("rect")
      .attr("width", 20)
      .attr("height", 20)
      .style("fill", (d) => `url(#${d.pattern})`);

    legend.append("text")
      .attr("x", 30)
      .attr("y", 15)
      .text((d) => d.label);
  }, [xPoints, yPoints, totalPoints]);

  return <svg ref={svgRef}></svg>;
};

export default SetOverlapDiagram;