import React, { useRef, useEffect } from 'react';
import { MapContainer, ImageOverlay, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const ZoomableImage = ({ imageUrl, onImageClick, nOfpoints }) => {
  const mapContainerRef = useRef(null);

  useEffect(() => {
    const mapContainer = mapContainerRef.current;

    if (mapContainer) {
      const MIN_ZOOM = -1;
      const MAX_ZOOM = 5;
      const INITIAL_ZOOM = 1;
      const ACTUAL_SIZE_ZOOM = 3;
      const map = L.map(mapContainer, {
        minZoom: MIN_ZOOM,
        maxZoom: MAX_ZOOM,
        center: [0, 0],
        zoom: INITIAL_ZOOM,
        crs: L.CRS.Simple
      });
      

      const southWest = map.unproject([0, nOfpoints], ACTUAL_SIZE_ZOOM);
      const northEast = map.unproject([nOfpoints, 0], ACTUAL_SIZE_ZOOM);
      console.log(southWest, northEast);
      const bounds = new L.LatLngBounds(southWest, northEast);

      // const map = L.map(mapContainer).setView([0, 0], 2);
      // const bounds = [[-90, -180], [90, 180]];
      const imageOverlay = L.imageOverlay(imageUrl, bounds).addTo(map);

      // Add a click event listener to the map
      map.on('click', (event) => {
        const { latlng } = event;
        const { lat, lng } = latlng;

        // Convert latlng to pixel coordinates
        const point = map.latLngToContainerPoint([lat, lng]);
        var x =  Math.round((lat*nOfpoints) / (southWest.lat - northEast.lat));
        var y =  Math.round((lng*nOfpoints) / (-southWest.lng + northEast.lng));
        

        if (x >= 0 && x <= nOfpoints && y >= 0 && y <= nOfpoints) {
          console.log(x + ':' + y);
          onImageClick(x, y);
        }
        else {
          console.log('Clicked outside image!');
        }

      });

      map.fitBounds(bounds);

      return () => {
        map.remove();
      };
    }
  }, [imageUrl, onImageClick]);

  return <div ref={mapContainerRef} style={{ height: '500px' }} />;
};

export default ZoomableImage;
