<template>
  <div class="dashboard-stats">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <h3>{{ stats.articles.total }}</h3>
          <p>مقالات ({{ stats.articles.published }} منتشر شده)</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🏗️</div>
        <div class="stat-content">
          <h3>{{ stats.projects }}</h3>
          <p>پروژه‌ها</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-content">
          <h3>{{ stats.contacts.total }}</h3>
          <p>تماس‌ها ({{ stats.contacts.new }} جدید)</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>{{ stats.team }}</h3>
          <p>اعضای تیم</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardStats',
  props: {
    stats: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.dashboard-stats {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 32px;
  opacity: 0.8;
}

.stat-content h3 {
  margin: 0 0 5px 0;
  font-size: 28px;
  font-weight: bold;
  color: #1abc9c;
}

.stat-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 15px;
  }

  .stat-content h3 {
    font-size: 24px;
  }
}
</style>