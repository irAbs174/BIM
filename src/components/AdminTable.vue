<template>
  <div class="admin-table-container">
    <Loader v-if="loading" />
    <table v-else-if="data.length > 0" class="admin-table">
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.id">
          <td v-for="column in columns" :key="column.key">
            <span v-if="column.type === 'boolean'">
              <span v-if="item[column.key]" class="status-published">منتشر شده</span>
              <span v-else class="status-draft">پیش‌نویس</span>
            </span>
            <span v-else-if="column.type === 'date'">
              {{ formatDate(item[column.key]) }}
            </span>
            <span v-else>
              {{ getNestedValue(item, column.key) }}
            </span>
          </td>
          <td class="actions">
            <button @click="$emit('edit', item)" class="btn-edit">ویرایش</button>
            <button @click="$emit('delete', item)" class="btn-delete">حذف</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="no-data">هیچ داده‌ای یافت نشد</div>
  </div>
</template>

<script>
import Loader from './Loader.vue';

export default {
  name: 'AdminTable',
  components: {
    Loader
  },
  props: {
    data: {
      type: Array,
      required: true
    },
    columns: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    getNestedValue(obj, path) {
      return path.split('.').reduce((current, key) => current && current[key], obj);
    },
    formatDate(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleDateString('fa-IR');
    }
  }
}
</script>

<style scoped>
.admin-table-container {
  width: 100%;
  overflow-x: auto;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 16px;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.admin-table th,
.admin-table td {
  padding: 12px 15px;
  text-align: right;
  border-bottom: 1px solid #eee;
}

.admin-table th {
  background: #f8f9fa;
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.admin-table td {
  color: #666;
  font-size: 14px;
}

.admin-table tr:hover {
  background: #f8f9fa;
}

.status-published {
  color: #27ae60;
  font-weight: bold;
}

.status-draft {
  color: #f39c12;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.btn-edit,
.btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-edit {
  background: #3498db;
  color: white;
}

.btn-edit:hover {
  background: #2980b9;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

@media (max-width: 768px) {
  .admin-table th,
  .admin-table td {
    padding: 8px 10px;
    font-size: 12px;
  }

  .actions {
    flex-direction: column;
    gap: 4px;
  }

  .btn-edit,
  .btn-delete {
    padding: 4px 8px;
    font-size: 11px;
  }
}
</style>