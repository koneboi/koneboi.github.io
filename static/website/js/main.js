document.addEventListener('DOMContentLoaded', () => {
  // Research filter logic
  const researchGrid = document.getElementById('researchGrid');
  if (researchGrid) {
    const topicFilter = document.getElementById('topicFilter');
    const yearFilter = document.getElementById('yearFilter');
    const researchCards = [...researchGrid.querySelectorAll('[data-topic]')];

    const applyResearchFilters = () => {
      const topicValue = topicFilter.value;
      const yearValue = yearFilter.value;
      researchCards.forEach(card => {
        const matchesTopic = topicValue === 'all' || card.dataset.topic === topicValue;
        const matchesYear = yearValue === 'all' || card.dataset.year === yearValue;
        card.style.display = matchesTopic && matchesYear ? '' : 'none';
      });
    };

    topicFilter?.addEventListener('change', applyResearchFilters);
    yearFilter?.addEventListener('change', applyResearchFilters);
  }

  // Project filter buttons
  const projectGrid = document.getElementById('projectGrid');
  if (projectGrid) {
    const projectButtons = document.querySelectorAll('[data-project-filter]');
    const projectCards = [...projectGrid.querySelectorAll('[data-project-type]')];

    projectButtons.forEach(button => {
      button.addEventListener('click', () => {
        projectButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        const value = button.dataset.projectFilter;
        projectCards.forEach(card => {
          const matches = value === 'all' || card.dataset.projectType === value;
          card.style.display = matches ? '' : 'none';
        });
      });
    });
  }

  // Skills Chart.js visualization
  const skillDataScript = document.getElementById('skill-chart-data');
  const chartCanvas = document.getElementById('skillsChart');
  if (skillDataScript && chartCanvas && window.Chart) {
    try {
      const skillData = JSON.parse(skillDataScript.textContent);
      const grouped = skillData.reduce((acc, skill) => {
        acc[skill.category] = (acc[skill.category] || 0) + skill.proficiency;
        return acc;
      }, {});
      const labels = Object.keys(grouped);
      const data = Object.values(grouped);

      new Chart(chartCanvas, {
        type: 'polarArea',
        data: {
          labels,
          datasets: [{
            data,
            backgroundColor: ['#118ab2', '#06d6a0', '#ffd166', '#ef476f'],
          }],
        },
        options: {
          plugins: { legend: { position: 'right' } },
          scales: { r: { beginAtZero: true } },
        },
      });
    } catch (error) {
      console.warn('Unable to render skills chart', error);
    }
  }
});

