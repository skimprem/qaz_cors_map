/* Example tile provider configuration.
 * Copy this file to `assets/config.js` and fill in your API keys.
 * Do NOT commit `assets/config.js` — it's ignored by .gitignore.
 * Supported fields:
 *  - url: tile URL template (must include {z}/{x}/{y} or similar)
 *  - attribution: HTML attribution string
 *  - options: additional Leaflet tile layer options (object)
 *
 * Examples:
 * MapTiler:
 * window.TILE_CONFIG = {
 *   url: 'https://api.maptiler.com/maps/streets/256/{z}/{x}/{y}.png?key=YOUR_MAPTILER_KEY',
 *   attribution: '© MapTiler © OpenStreetMap contributors',
 *   options: { maxZoom: 20 }
 * };
 *
 * Mapbox (use style URL and access token):
 * window.TILE_CONFIG = {
 *   url: 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=YOUR_MAPBOX_TOKEN',
 *   attribution: '© Mapbox © OpenStreetMap contributors',
 *   options: { id: 'mapbox/streets-v11', tileSize: 512, maxZoom: 20 }
 * };
 */

// Example default (MapTiler placeholder)
window.TILE_CONFIG = {
  // Replace with your provider's URL template and key
  url: 'https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=YOUR_MAPTILER_KEY',
  attribution: '© MapTiler © OpenStreetMap contributors',
  options: {
    maxZoom: 20,
    detectRetina: false
  }
};
