document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('collaborationMap');
  const script = document.getElementById('collaboration-data');
  if (!container || !script || !window.L) {
    return;
  }

  let data = [];
  try {
    data = JSON.parse(script.textContent);
  } catch (error) {
    console.warn('Unable to parse collaboration data', error);
  }

  const map = L.map('collaborationMap', {
    worldCopyJump: true,
  }).setView([10, 0], data.length ? 2 : 1);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 6,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);

  data.forEach((item) => {
    const marker = L.marker([item.lat, item.lng]).addTo(map);
    marker.bindPopup(
      `<strong>${item.name}</strong><br>${item.region}<br>${item.duration}<br>${item.summary}`,
    );
  });
});

