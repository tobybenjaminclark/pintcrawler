import axios from 'axios';
import mapboxgl from "mapbox-gl";

// Fetch crime data by point
export const getCrimesByPoint = async (lat, lng, date = "2024-01", category = "all-crime") => {
  const url = `https://data.police.uk/api/crimes-street/${category}`;
  const params = {
    date: date,
    lat: lat,
    lng: lng,
  };

  try {
    const response = await axios.get(url, { params });
    return response.data; // Return the crime data
  } catch (error) {
    console.error("Error fetching crimes by point:", error);
    return [];
  }
};

export const plotCrimes = (map, crimes) => {
  // Create a GeoJSON object from the crimes
  const crimeData = {
    type: 'FeatureCollection',
    features: crimes.map(crime => ({
      type: 'Feature',
      properties: {
        category: crime.category, // You can customize this to display more crime details in the popup
      },
      geometry: {
        type: 'Point',
        coordinates: [
          parseFloat(crime.location.longitude), // Ensure it's a float for accurate coordinates
          parseFloat(crime.location.latitude),   // Ensure it's a float for accurate coordinates
        ],
      },
    })),
  };

  // Add GeoJSON source to the map
  map.addSource('crime-source', {
    type: 'geojson',
    data: crimeData,
  });

// Add a layer to display the crime points with a black outline
map.addLayer({
  id: 'crime-layer',
  type: 'circle',
  source: 'crime-source',
  paint: {
    'circle-color': '#ff0000',    // Red color for the crime markers
    'circle-radius': 6,           // Size of the marker
    'circle-opacity': 0.7,        // Opacity of the marker
    'circle-stroke-color': '#000000', // Black outline for the marker
    'circle-stroke-width': 2,     // Width of the outline
  },
});


  // Optional: Add popups when clicking a crime marker
  map.on('click', 'crime-layer', (e) => {
    const coordinates = e.features[0].geometry.coordinates.slice();
    const category = e.features[0].properties.category;

    new mapboxgl.Popup()
    .setLngLat(coordinates)
    .setHTML(`
      <div style="text-align: center; background-color: #B5AE90; border: 2px solid black; padding: 10px;">
        <p style="font-size: 20px; font-family: 'medieval', sans-serif; color: #000000;">
          <strong>Crime Category: </strong>${category}
        </p>
      </div>
    `)
    .addTo(map);
  });

  // Change the cursor to a pointer when hovering over a crime marker
  map.on('mouseenter', 'crime-layer', () => {
    map.getCanvas().style.cursor = 'pointer';
  });

  map.on('mouseleave', 'crime-layer', () => {
    map.getCanvas().style.cursor = '';
  });
  // Add the source for the crime data
  map.on('load', () => {
    map.addSource('crimes', {
      type: 'geojson',
      data: crimeData,
      cluster: true,
      clusterMaxZoom: 14,
      clusterRadius: 50,
    });

    // Add the clusters layer
    map.addLayer({
      id: 'clusters',
      type: 'circle',
      source: 'crimes',
      filter: ['has', 'point_count'],
      paint: {
        'circle-color': '#51bbd6',
        'circle-radius': [
          'step',
          ['get', 'point_count'],
          20,
          100, 40,
          750, 50,
        ],
      },
    });

    // Add the cluster count layer
    map.addLayer({
      id: 'cluster-count',
      type: 'symbol',
      source: 'crimes',
      filter: ['has', 'point_count'],
      layout: {
        'text-field': '{point_count_abbreviated}',
        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
        'text-size': 12,
      },
      paint: {
        'text-color': '#ffffff',
      },
    });

    // Add the unclustered points layer
    map.addLayer({
      id: 'unclustered-point',
      type: 'circle',
      source: 'crimes',
      filter: ['!', ['has', 'point_count']],
      paint: {
        'circle-color': '#ff0000',
        'circle-radius': 5,
      },
    });
  });
};