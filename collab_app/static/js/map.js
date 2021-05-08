$(document).ready(() => {

  let posts = loadPosts()

  //getMarkers(posts)
  
})

const loadPosts = () => {
  
  $.ajax({ 
    url: "/getCoords/" 
  }).then(function(res) { 
    getMarkers(res.posts)
  }); 

  



 
}

const getMarkers = async (posts) =>  { 
  mapboxgl.accessToken = 'pk.eyJ1Ijoiam1wYXJrZXIiLCJhIjoiY2tvYTJieTJkMXlzeTJ3bWw0ZDl6YmJzeCJ9.4koTUeoAy2Pb9slTYj3bkg';
  var map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/mapbox/streets-v11', // style URL
  center: [-79.0558, 35.9132], // starting position [lng, lat]
  zoom: 11 // starting zoom
  });

  

  featured = []
  posts.forEach((x) => {
    inst = {type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: [x[10], x[9]]
            },
            properties: {
              title: x[1],
              description: x[8],
              id: x[0]
            }
          }
    featured.push(inst)
  })

  var geojson = {
  type: 'FeatureCollection',
  features: featured
  };

  // add markers to map
  geojson.features.forEach(function(marker) {

  // create a HTML element for each feature
  var el = document.createElement('div');
  el.className = 'marker';

  // make a marker for each feature and add to the map
  new mapboxgl.Marker(el)
  .setLngLat(marker.geometry.coordinates)
  .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
    .setHTML('<h3>' + marker.properties.title + '</h3><p>' + marker.properties.description + `</p><a class="action" href="/` + marker.properties.id + `/info">More Information</a>`))
  .addTo(map);
  });
  }
