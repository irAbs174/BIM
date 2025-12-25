<template>
  <div class="admin-form">
    <form @submit.prevent="handleSubmit">
      <div class="form-grid">
        <div
          v-for="field in getFields()"
          :key="field.key"
          class="form-group"
        >
          <label :for="field.key">{{ field.label }}</label>

          <!-- Text Input -->
          <input
            v-if="field.type === 'text'"
            :id="field.key"
            v-model="formData[field.key]"
            :type="field.inputType || 'text'"
            :placeholder="field.placeholder"
          >

          <!-- Textarea -->
          <textarea
            v-else-if="field.type === 'textarea'"
            :id="field.key"
            v-model="formData[field.key]"
            :placeholder="field.placeholder"
            :rows="field.rows || 4"
          ></textarea>

          <!-- Select -->
          <select
            v-else-if="field.type === 'select'"
            :id="field.key"
            v-model="formData[field.key]"
          >
            <option value="">انتخاب کنید</option>
            <option
              v-for="option in field.options"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>

          <!-- Checkbox -->
          <div v-else-if="field.type === 'checkbox'" class="checkbox-group">
            <input
              :id="field.key"
              v-model="formData[field.key]"
              type="checkbox"
            >
            <label :for="field.key" class="checkbox-label">{{ field.label }}</label>
          </div>

          <!-- Date Input -->
          <input
            v-else-if="field.type === 'date'"
            :id="field.key"
            v-model="formData[field.key]"
            type="date"
          >

          <!-- File Upload -->
          <FileUpload
            v-else-if="field.type === 'file'"
            :id="field.key"
            v-model="formData[field.key]"
            :accept="field.accept"
            :label="field.label"
          />
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-save" :disabled="saving">
          {{ saving ? 'در حال ذخیره...' : 'ذخیره' }}
        </button>
        <button type="button" @click="$emit('cancel')" class="btn-cancel">
          لغو
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import FileUpload from './FileUpload.vue'

export default {
  name: 'AdminForm',
  components: {
    FileUpload
  },
  props: {
    contentType: {
      type: String,
      required: true
    },
    item: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      formData: {},
      saving: false
    }
  },
  mounted() {
    this.initializeForm();
  },
  watch: {
    item: {
      handler() {
        this.initializeForm();
      },
      deep: true
    }
  },
  methods: {
    initializeForm() {
      const fields = this.getFields();
      this.formData = {};

      fields.forEach(field => {
        if (this.item && this.item[field.key] !== undefined) {
          this.formData[field.key] = this.item[field.key];
        } else {
          this.formData[field.key] = field.default || '';
        }
      });
    },
    getFields() {
      // Define fields based on content type
      switch (this.contentType) {
        case 'articles':
          return [
            { key: 'title_fa', label: 'عنوان (فارسی)', type: 'text', placeholder: 'عنوان مقاله به فارسی' },
            { key: 'title_en', label: 'عنوان (انگلیسی)', type: 'text', placeholder: 'Article title in English' },
            { key: 'content_fa', label: 'محتوا (فارسی)', type: 'textarea', placeholder: 'محتوای مقاله به فارسی', rows: 6 },
            { key: 'content_en', label: 'محتوا (انگلیسی)', type: 'textarea', placeholder: 'Article content in English', rows: 6 },
            { key: 'slug', label: 'اسلاگ', type: 'text', placeholder: 'article-slug' },
            { key: 'category', label: 'دسته‌بندی', type: 'text', placeholder: 'دسته‌بندی مقاله' },
            { key: 'tags', label: 'برچسب‌ها', type: 'text', placeholder: 'برچسب1, برچسب2' },
            { key: 'publish_date', label: 'تاریخ انتشار', type: 'date' },
            { key: 'is_published', label: 'منتشر شود', type: 'checkbox' },
            { key: 'featured_image', label: 'تصویر شاخص', type: 'file', accept: 'image/*' }
          ];
        case 'contacts':
          return [
            { key: 'name', label: 'نام', type: 'text', placeholder: 'نام تماس گیرنده' },
            { key: 'email', label: 'ایمیل', type: 'text', placeholder: 'email@example.com' },
            { key: 'phone', label: 'شماره تلفن', type: 'text', placeholder: '۰۹۱۲۱۲۳۴۵۶۷' },
            { key: 'message', label: 'پیام', type: 'textarea', placeholder: 'پیام کاربر', rows: 6 },
            {
              key: 'status',
              label: 'وضعیت',
              type: 'select',
              options: [
                { value: 'new', label: 'جدید' },
                { value: 'read', label: 'خوانده شده' },
                { value: 'replied', label: 'پاسخ داده شده' }
              ]
            }
          ];
        default:
          return [
            { key: 'title_fa', label: 'عنوان (فارسی)', type: 'text' },
            { key: 'title_en', label: 'عنوان (انگلیسی)', type: 'text' },
            { key: 'description_fa', label: 'توضیحات (فارسی)', type: 'textarea' },
            { key: 'description_en', label: 'توضیحات (انگلیسی)', type: 'textarea' }
          ];
      }
    },
    async handleSubmit() {
      this.saving = true;
      try {
        await this.$emit('save', this.formData);
      } catch (error) {
        console.error('Save error:', error);
      } finally {
        this.saving = false;
      }
    }
  }
}
</script>

<style scoped>
.admin-form {
  max-width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
  font-size: 14px;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 10px 12px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #1abc9c;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.checkbox-label {
  font-weight: normal !important;
  margin-bottom: 0 !important;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-save,
.btn-cancel {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-save {
  background: #1abc9c;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #16a085;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
}

.btn-cancel:hover {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-save,
  .btn-cancel {
    width: 100%;
  }
}
</style>