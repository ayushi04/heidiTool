import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

const ThreeDPlot = () => {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer();
  const planeZ = useRef();
  const planeY = useRef();
  const lineX = useRef();

  let isMouseDown = false;
  let previousMousePosition = { x: 0, y: 0 };

  useEffect(() => {
    // Set up renderer
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Set background color to white
    renderer.setClearColor(0xffffff);

    // Create planes along z-axis and y-axis
    const planeGeometry = new THREE.PlaneGeometry(3, 3);
    const planeMaterial = new THREE.MeshBasicMaterial({ color: 0x0000ff, side: THREE.DoubleSide });

    planeZ.current = new THREE.Mesh(planeGeometry, planeMaterial);
    planeZ.current.position.set(0, 0, -2.5);
    scene.add(planeZ.current);

    planeY.current = new THREE.Mesh(planeGeometry, planeMaterial);
    planeY.current.position.set(0, -2.5, 0);
    planeY.current.rotation.x = Math.PI / 2; // Rotate the plane to align along the y-axis
    scene.add(planeY.current);

    // Draw a line along the x-axis
    const lineGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-2.5, 0, 0),
      new THREE.Vector3(2.5, 0, 0),
    ]);

    const lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000, linewidth: 5 });
    lineX.current = new THREE.Line(lineGeometry, lineMaterial);
    scene.add(lineX.current);

    // Position camera
    camera.position.z = 10;

    // Handle window resize
    const handleResize = () => {
      const newWidth = window.innerWidth;
      const newHeight = window.innerHeight;

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();

      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    // Mouse events
    const handleMouseDown = (event) => {
      isMouseDown = true;
      previousMousePosition = { x: event.clientX, y: event.clientY };
    };

    const handleMouseMove = (event) => {
      if (isMouseDown) {
        const deltaX = event.clientX - previousMousePosition.x;
        const deltaY = event.clientY - previousMousePosition.y;

        // Update scene position based on mouse movement
        scene.position.x += deltaX * 0.01;
        scene.position.y -= deltaY * 0.01;

        previousMousePosition = { x: event.clientX, y: event.clientY };
      }
    };

    const handleMouseUp = () => {
      isMouseDown = false;
    };

    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    // Render function
    const render = () => {
      renderer.render(scene, camera);
    };

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      render();
    };

    animate();

    // Clean up on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      document.body.removeChild(renderer.domElement);
    };
  }, []); // Empty dependency array ensures that useEffect runs only once

  return null; // This component doesn't render anything directly
};

export default ThreeDPlot;
