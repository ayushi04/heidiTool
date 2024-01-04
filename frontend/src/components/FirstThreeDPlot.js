import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const FirstThreeDPlot = ({ dataset, container, width, height }) => {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer();
  const orbit = new OrbitControls(camera, renderer.domElement);
  const plane1 = useRef();
  const plane2 = useRef();
  const linesGroup = useRef();
  const arrowsGroup = useRef();

  useEffect(() => {
    // Set up renderer
    renderer.setSize(width, height);
    container?.appendChild(renderer.domElement); // Append to the provided container

    // Update background color
    renderer.setClearColor(0xeeeeee);

    const axisHelper = new THREE.AxesHelper(5);
    scene.add(axisHelper);
    camera.position.set(0, 2, 5);
    orbit.update();

    const gridHelper = new THREE.GridHelper();
    scene.add(gridHelper);

    // Create planes along z-axis
    const planeGeometry = new THREE.PlaneGeometry(2, 3);
    const planeMaterial = new THREE.MeshBasicMaterial({ color: 0x0000ff, side: THREE.DoubleSide });

    plane1.current = new THREE.Mesh(planeGeometry, planeMaterial);
    plane1.current.position.set(0, 0, -2);
    scene.add(plane1.current);

    plane2.current = new THREE.Mesh(planeGeometry, planeMaterial);
    plane2.current.position.set(0, 0, 0);
    scene.add(plane2.current);

    // Create a group for lines
    linesGroup.current = new THREE.Group();
    scene.add(linesGroup.current);

    dataset.forEach((row) => {
      const curve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(row.x1, row.y1, -2),
        new THREE.Vector3(row.x2, row.y2, 0),
      ]);

      const points = curve.getPoints(50); // Adjust the number of points as needed

      const lineGeometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points), 50, 0.02, 8, false);
      const lineMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
      const line = new THREE.Mesh(lineGeometry, lineMaterial);
      linesGroup.current.add(line);
    });

    // Render function
    const render = () => {
      orbit.update();
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
      container?.removeChild(renderer.domElement); // Remove from the container
    };
  }, [dataset, container, height, width]); // Add dataset, container, height, and width to the dependency array

  const handleResize = () => {
    const newWidth = width;
    const newHeight = height;

    camera.aspect = newWidth / newHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(newWidth, newHeight);
  };

  window.addEventListener('resize', handleResize);

  return null; // This component doesn't render anything directly
};

export default FirstThreeDPlot;
