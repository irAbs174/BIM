<template>
  <div class="admin-content-manager">
    <AdminSidebar @navigate="handleNavigation" />
    <div class="main-content">
      <div class="content-header">
        <h1>{{ getContentTypeLabel() }}</h1>
        <button @click="showAddForm" class="btn-primary">افزودن {{ getContentTypeLabel(true) }}</button>
      </div>

      <div class="content-body">
        <!-- List View -->
        <div v-if="!showForm" class="list-view">
          <AdminTable
            :data="items"
            :columns="getColumns()"
            :loading="loading"
            @edit="editItem"
            @delete="deleteItem"
          />
        </div>

        <!-- Form View -->
        <div v-else class="form-view">
          <AdminForm
            :contentType="contentType"
            :item="editingItem"
            @save="saveItem"
            @cancel="cancelForm"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminSidebar from './AdminSidebar.vue'
import AdminTable from './AdminTable.vue'
import AdminForm from './AdminForm.vue'
import {
  adminArticleService,
  adminProjectService,
  adminServiceService,
  adminTeamService,
  adminCertificateService,
  adminLicenseService,
  adminContactService
} from '../services/api'

export default {
  name: 'AdminContentManager',
  components: {
    AdminSidebar,
    AdminTable,
    AdminForm
  },
  data() {
    return {
      contentType: '',
      items: [],
      loading: false,
      showForm: false,
      editingItem: null
    }
  },
  provide() {
    return {
      navigateTo: this.navigateTo
    }
  },
  inject: ['navigateTo'],
  mounted() {
    this.checkAuth();
    this.determineContentType();
    this.loadItems();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        this.navigateTo('/admin/login');
      }
    },
    determineContentType() {
      const path = window.location.pathname;
      if (path.includes('/articles')) {
        this.contentType = 'articles';
      } else if (path.includes('/projects')) {
        this.contentType = 'projects';
      } else if (path.includes('/services')) {
        this.contentType = 'services';
      } else if (path.includes('/team')) {
        this.contentType = 'team';
      } else if (path.includes('/certificates')) {
        this.contentType = 'certificates';
      } else if (path.includes('/licenses')) {
        this.contentType = 'licenses';
      } else if (path.includes('/contacts')) {
        this.contentType = 'contacts';
      }
    },
    getService() {
      switch (this.contentType) {
        case 'articles': return adminArticleService;
        case 'projects': return adminProjectService;
        case 'services': return adminServiceService;
        case 'team': return adminTeamService;
        case 'certificates': return adminCertificateService;
        case 'licenses': return adminLicenseService;
        case 'contacts': return adminContactService;
        default: return null;
      }
    },
    async loadItems() {
      this.loading = true;
      try {
        const service = this.getService();
        if (service) {
          const response = await service.getAll();
          this.items = response.data;
        }
      } catch (error) {
        console.error('Error loading items:', error);
      } finally {
        this.loading = false;
      }
    },
    getContentTypeLabel(singular = false) {
      const labels = {
        articles: singular ? 'مقاله' : 'مقالات',
        projects: singular ? 'پروژه' : 'پروژه‌ها',
        services: singular ? 'خدمت' : 'خدمات',
        team: singular ? 'عضو' : 'تیم',
        certificates: singular ? 'گواهینامه' : 'گواهینامه‌ها',
        licenses: singular ? 'مجوز' : 'مجوزها',
        contacts: singular ? 'تماس' : 'تماس‌ها'
      };
      return labels[this.contentType] || 'محتوا';
    },
    getColumns() {
      // Define columns based on content type
      switch (this.contentType) {
        case 'articles':
          return [
            { key: 'title_fa', label: 'عنوان' },
            { key: 'category', label: 'دسته‌بندی' },
            { key: 'is_published', label: 'وضعیت', type: 'boolean' },
            { key: 'publish_date', label: 'تاریخ انتشار', type: 'date' }
          ];
        case 'contacts':
          return [
            { key: 'name', label: 'نام' },
            { key: 'email', label: 'ایمیل' },
            { key: 'status', label: 'وضعیت' },
            { key: 'submitted_at', label: 'تاریخ', type: 'date' }
          ];
        default:
          return [{ key: 'title_fa', label: 'عنوان' }];
      }
    },
    showAddForm() {
      this.editingItem = null;
      this.showForm = true;
    },
    editItem(item) {
      this.editingItem = item;
      this.showForm = true;
    },
    cancelForm() {
      this.showForm = false;
      this.editingItem = null;
    },
    async saveItem(itemData) {
      try {
        const service = this.getService();
        if (this.editingItem) {
          await service.update(this.editingItem.id, itemData);
        } else {
          await service.create(itemData);
        }
        this.cancelForm();
        this.loadItems();
      } catch (error) {
        console.error('Error saving item:', error);
      }
    },
    async deleteItem(item) {
      if (confirm('آیا مطمئن هستید که می‌خواهید این مورد را حذف کنید؟')) {
        try {
          const service = this.getService();
          await service.delete(item.id);
          this.loadItems();
        } catch (error) {
          console.error('Error deleting item:', error);
        }
      }
    },
    handleNavigation(route) {
      this.navigateTo(route);
    }
  }
}
</script>

<style scoped>
.admin-content-manager {
  display: flex;
  min-height: 100vh;
  background: #f5f5f5;
  direction: rtl;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-right: 250px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.content-header h1 {
  margin: 0;
  color: #333;
}

.btn-primary {
  background: #1abc9c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.btn-primary:hover {
  background: #16a085;
}

.content-body {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.list-view,
.form-view {
  padding: 20px;
}

@media (max-width: 768px) {
  .main-content {
    margin-right: 0;
    padding: 15px;
  }

  .content-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .content-header h1 {
    font-size: 20px;
  }
}
</style>