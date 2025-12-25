<template>
  <div class="file-upload">
    <div class="upload-area" @click="triggerFileInput" @drop="handleDrop" @dragover.prevent>
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        @change="handleFileSelect"
        style="display: none"
      >

      <div v-if="!file" class="upload-placeholder">
        <div class="upload-icon">📁</div>
        <p>{{ label || 'فایل را اینجا رها کنید یا کلیک کنید' }}</p>
        <small v-if="accept">فرمت‌های مجاز: {{ accept }}</small>
      </div>

      <div v-else class="file-preview">
        <div class="file-info">
          <span class="file-name">{{ file.name }}</span>
          <span class="file-size">({{ formatFileSize(file.size) }})</span>
        </div>
        <button type="button" @click.stop="removeFile" class="btn-remove">×</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUpload',
  props: {
    modelValue: {
      type: [File, String],
      default: null
    },
    accept: {
      type: String,
      default: '*'
    },
    label: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      file: null
    }
  },
  watch: {
    modelValue: {
      handler(newVal) {
        if (newVal instanceof File) {
          this.file = newVal;
        } else if (typeof newVal === 'string') {
          // Handle URL case - could show filename from URL
          this.file = null;
        } else {
          this.file = null;
        }
      },
      immediate: true
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.setFile(file);
      }
    },
    handleDrop(event) {
      event.preventDefault();
      const file = event.dataTransfer.files[0];
      if (file) {
        this.setFile(file);
      }
    },
    setFile(file) {
      this.file = file;
      this.$emit('update:modelValue', file);
    },
    removeFile() {
      this.file = null;
      this.$emit('update:modelValue', null);
      this.$refs.fileInput.value = '';
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  }
}
</script>

<style scoped>
.file-upload {
  width: 100%;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
}

.upload-area:hover {
  border-color: #1abc9c;
  background: #f0f9f8;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.upload-icon {
  font-size: 48px;
  color: #ccc;
}

.upload-placeholder p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.upload-placeholder small {
  color: #999;
  font-size: 12px;
}

.file-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 10px 15px;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.file-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.file-name {
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.file-size {
  color: #666;
  font-size: 12px;
}

.btn-remove {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.btn-remove:hover {
  background: #c0392b;
}

@media (max-width: 480px) {
  .upload-area {
    padding: 15px;
  }

  .upload-icon {
    font-size: 36px;
  }

  .file-preview {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .btn-remove {
    align-self: flex-end;
  }
}
</style>