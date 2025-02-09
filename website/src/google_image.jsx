export const getPlacePhoto = async (photoReference) => {
    const photoUrl = `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${photoReference}&key=AIzaSyD2-qiQoW3Qd6-ToCN9gAmW6e2RqSwJYsk`; // Replace with your Google Maps API Key
  
    try {
      const response = await fetch(photoUrl);
      if (response.ok) {
        return response.url; // Return the image URL
      } else {
        console.error("Failed to fetch photo:", response.statusText);
        return null;
      }
    } catch (error) {
      console.error("Error fetching photo:", error);
      return null;
    }
  };
  
 export const addMarkerWithPhoto = async (map, routeData, nodeType) => {
    const node = routeData[nodeType];
    if (node && node.loc && Array.isArray(node.loc)) {
      const [lat, lng] = node.loc;
  
      // Create marker for node
      const marker = new mapboxgl.Marker()
        .setLngLat([lng, lat])
        .addTo(map)
        .getElement()
        .addEventListener("click", async () => {
          // Fetch photo using the PhotoReference if it exists
          if (node.PhotoReference) {
            const photoUrl = await getPlacePhoto(node.PhotoReference);
            if (photoUrl) {
              // Set the photo and other info in the overlay
              setMarkerInfoContent(`
                <div>
                  <strong>${node.name}</strong>
                  <br />
                  <img src="${photoUrl}" alt="${node.name}" style="width: 100px; height: 100px; object-fit: cover;"/>
                  <br />
                  Location: [${lat}, ${lng}]
                </div>
              `);
            } else {
              setMarkerInfoContent(`${node.name}: [${lat}, ${lng}]`);
            }
          } else {
            setMarkerInfoContent(`${node.name}: [${lat}, ${lng}]`);
          }
  
          // Calculate pixel position for the overlay
          const { x, y } = map.project([lng, lat]);
          setMarkerInfoPosition({ x, y });
          setMarkerInfoVisible(true);
        });
  
      markersRef.current.push(marker); // Store marker in the ref
    }
  };
  