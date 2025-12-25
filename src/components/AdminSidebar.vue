<template>
  <div class="admin-sidebar">
    <div class="sidebar-header">
      <h3>پنل مدیریت</h3>
    </div>
    <nav class="sidebar-nav">
      <ul>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin')"
            :class="{ active: isActive('/admin') }"
          >
            <span class="icon">📊</span>
            داشبورد
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/articles')"
            :class="{ active: isActive('/admin/articles') }"
          >
            <span class="icon">📝</span>
            مقالات
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/projects')"
            :class="{ active: isActive('/admin/projects') }"
          >
            <span class="icon">🏗️</span>
            پروژه‌ها
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/services')"
            :class="{ active: isActive('/admin/services') }"
          >
            <span class="icon">🛠️</span>
            خدمات
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/team')"
            :class="{ active: isActive('/admin/team') }"
          >
            <span class="icon">👥</span>
            تیم
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/certificates')"
            :class="{ active: isActive('/admin/certificates') }"
          >
            <span class="icon">🏆</span>
            گواهینامه‌ها
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/licenses')"
            :class="{ active: isActive('/admin/licenses') }"
          >
            <span class="icon">📄</span>
            مجوزها
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/contacts')"
            :class="{ active: isActive('/admin/contacts') }"
          >
            <span class="icon">💬</span>
            تماس‌ها
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="$emit('navigate', '/admin/settings')"
            :class="{ active: isActive('/admin/settings') }"
          >
            <span class="icon">⚙️</span>
            تنظیمات
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'AdminSidebar',
  methods: {
    isActive(route) {
      return window.location.pathname === route;
    }
  }
}
</script>

<style scoped>
.admin-sidebar {
  position: fixed;
  right: 0;
  top: 0;
  width: 250px;
  height: 100vh;
  background: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  background: #1abc9c;
  color: white;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  text-align: center;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav li {
  border-bottom: 1px solid #f5f5f5;
}

.sidebar-nav li:last-child {
  border-bottom: none;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: #333;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 14px;
}

.sidebar-nav a:hover {
  background: #f8f9fa;
  color: #1abc9c;
}

.sidebar-nav a.active {
  background: #1abc9c;
  color: white;
}

.icon {
  margin-left: 10px;
  font-size: 16px;
}

@media (max-width: 768px) {
  .admin-sidebar {
    width: 200px;
  }

  .sidebar-nav a {
    padding: 12px 15px;
    font-size: 13px;
  }

  .icon {
    margin-left: 8px;
  }
}
</style>