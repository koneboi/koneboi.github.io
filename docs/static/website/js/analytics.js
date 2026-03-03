document.addEventListener('DOMContentLoaded', () => {
  if (!window.Plotly) {
    return;
  }

  const parseData = (id) => {
    const script = document.getElementById(id);
    if (!script) {
      return [];
    }
    try {
      return JSON.parse(script.textContent);
    } catch (error) {
      console.warn('Unable to parse analytics data', id, error);
      return [];
    }
  };

  const publicationData = parseData('publication-data');
  if (publicationData.length) {
    Plotly.newPlot('publicationChart', [{
      x: publicationData.map(item => item.year),
      y: publicationData.map(item => item.total),
      type: 'scatter',
      mode: 'lines+markers',
      marker: { color: '#118ab2' },
      fill: 'tozeroy',
    }], {
      margin: { t: 30, l: 40, r: 10, b: 40 },
      xaxis: { title: 'Year' },
      yaxis: { title: 'Publications' },
    }, { displayModeBar: false, responsive: true });
  }

  const projectData = parseData('project-data');
  if (projectData.length) {
    Plotly.newPlot('projectChart', [{
      labels: projectData.map(item => item.project_type),
      values: projectData.map(item => item.total),
      type: 'pie',
      hole: 0.4,
    }], {
      margin: { t: 30, b: 30 },
    }, { displayModeBar: false, responsive: true });
  }
});

