<template>
  <div class="comments-section" :class="{ 'dark-mode': isDark }">
    <h3 class="section-title">
      نظرات
      <span class="comment-count" v-if="comments.length > 0">({{ comments.length }})</span>
    </h3>

    <!-- فرم ثبت نظر -->
    <div class="comment-form" v-if="!submitted">
      <h4 class="form-title">نظر خود را بنویسید</h4>
      
      <form @submit.prevent="submitComment">
        <div class="form-group">
          <label for="name">نام و نام خانوادگی *</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            placeholder="نام خود را وارد کنید"
            required
            maxlength="100"
          />
        </div>

        <div class="form-group">
          <label for="email">ایمیل *</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="example@email.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="rating">امتیاز شما *</label>
          <StarRating v-model="formData.rating" />
        </div>

        <div class="form-group">
          <label for="content">نظر شما *</label>
          <textarea
            id="content"
            v-model="formData.content"
            placeholder="نظر خود را در مورد این مطلب بنویسید..."
            required
            minlength="10"
            rows="5"
          ></textarea>
          <small class="char-count">حداقل 10 کاراکتر</small>
        </div>

        <div class="form-actions">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading || !isFormValid"
          >
            {{ loading ? 'در حال ارسال...' : 'ثبت نظر' }}
          </button>
        </div>
      </form>
    </div>

    <!-- پیام موفقیت -->
    <div class="success-message" v-if="submitted">
      <div class="success-icon">✓</div>
      <h4>نظر شما با موفقیت ثبت شد!</h4>
      <p>نظر شما پس از بررسی و تایید توسط ادمین نمایش داده خواهد شد.</p>
      <button @click="resetForm" class="btn btn-outline">ثبت نظر جدید</button>
    </div>

    <!-- لیست نظرات تایید شده -->
    <div class="comments-list" v-if="comments.length > 0">
      <h4 class="list-title">نظرات کاربران</h4>
      
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment-card"
      >
        <div class="comment-header">
          <div class="comment-author">
            <div class="author-avatar">
              {{ comment.name.charAt(0) }}
            </div>
            <div class="author-info">
              <h5 class="author-name">{{ comment.name }}</h5>
              <StarRating
                :model-value="comment.rating"
                :readonly="true"
                :show-label="false"
              />
            </div>
          </div>
          <div class="comment-date">
            {{ formatDate(comment.created_at) }}
          </div>
        </div>
        
        <div class="comment-content">
          {{ comment.content }}
        </div>
      </div>
    </div>

    <!-- پیام خالی -->
    <div class="empty-state" v-if="!loading && comments.length === 0 && !submitted">
      <p>هنوز نظری ثبت نشده است. اولین نفری باشید که نظر می‌دهید!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import StarRating from './StarRating.vue'
import { createComment, getComments } from '../api/services'
import { success as showSuccess, error as showError } from '../composables/useToast'

const props = defineProps({
  contentType: {
    type: String,
    required: true,
    validator: (value) => ['article', 'project'].includes(value)
  },
  contentId: {
    type: Number,
    required: true
  },
  isDark: {
    type: Boolean,
    default: false
  }
})

const comments = ref([])
const loading = ref(false)
const submitted = ref(false)

const formData = ref({
  name: '',
  email: '',
  content: '',
  rating: 0
})

const isFormValid = computed(() => {
  return (
    formData.value.name.trim().length > 0 &&
    formData.value.email.trim().length > 0 &&
    formData.value.content.trim().length >= 10 &&
    formData.value.rating > 0
  )
})

const fetchComments = async () => {
  loading.value = true
  try {
    const response = await getComments({
      content_type: props.contentType,
      content_id: props.contentId,
      approved_only: true
    })
    comments.value = response || []
  } catch (error) {
    console.error('Error fetching comments:', error)
    showError('خطا در دریافت نظرات')
  } finally {
    loading.value = false
  }
}

const submitComment = async () => {
  if (!isFormValid.value) return

  loading.value = true
  try {
    await createComment({
      name: formData.value.name.trim(),
      email: formData.value.email.trim(),
      content: formData.value.content.trim(),
      rating: formData.value.rating,
      content_type: props.contentType,
      content_id: props.contentId
    })
    
    submitted.value = true
    showSuccess('نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده خواهد شد')
  } catch (error) {
    console.error('Error submitting comment:', error)
    showError('خطا در ثبت نظر. لطفاً دوباره تلاش کنید')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    name: '',
    email: '',
    content: '',
    rating: 0
  }
  submitted.value = false
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'امروز'
  if (diffDays === 1) return 'دیروز'
  if (diffDays < 7) return `${diffDays} روز پیش`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} هفته پیش`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} ماه پیش`
  return `${Math.floor(diffDays / 365)} سال پیش`
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.comments-section {
  margin-top: 4rem;
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.comments-section.dark-mode {
  background: linear-gradient(135deg, #2a2d35ff 0%, #26282dff 100%);
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1f2937;
}

.dark-mode .section-title {
  color: #f9fafb;
}

.comment-count {
  font-size: 1rem;
  color: #6b7280;
  font-weight: 400;
}

/* فرم نظر */
.comment-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.dark-mode .comment-form {
  background: #191a1cff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.form-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.dark-mode .form-title {
  color: #f9fafb;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.dark-mode .form-group label {
  color: #d1d5db;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-family: inherit;
  font-size: 1rem;
  transition: all 0.2s;
  background: white;
  color: #1f2937;
}

.dark-mode .form-group input,
.dark-mode .form-group textarea {
  background: #1f2937;
  border-color: #4b5563;
  color: #f9fafb;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.char-count {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.form-actions {
  display: flex;
  justify-content: flex-start;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-outline {
  background: white;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.btn-outline:hover {
  background: #3b82f6;
  color: white;
}

/* پیام موفقیت */
.success-message {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 2rem;
}

.success-icon {
  width: 60px;
  height: 60px;
  background: white;
  color: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  margin: 0 auto 1rem;
}

.success-message h4 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.success-message p {
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

/* لیست نظرات */
.comments-list {
  margin-top: 3rem;
}

.list-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.dark-mode .list-title {
  color: #f9fafb;
}

.comment-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
  transition: all 0.2s;
}

.dark-mode .comment-card {
  background: #374151;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.comment-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.comment-author {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  flex-shrink: 0;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.author-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.dark-mode .author-name {
  color: #f9fafb;
}

.comment-date {
  font-size: 0.875rem;
  color: #6b7280;
}

.dark-mode .comment-date {
  color: #9ca3af;
}

.comment-content {
  color: #4b5563;
  line-height: 1.7;
  white-space: pre-wrap;
}

.dark-mode .comment-content {
  color: #d1d5db;
}

/* پیام خالی */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.dark-mode .empty-state {
  color: #9ca3af;
}

.empty-state p {
  font-size: 1rem;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .comments-section {
    padding: 1.5rem;
    margin-top: 3rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .comment-form {
    padding: 1.5rem;
  }

  .form-title {
    font-size: 1.1rem;
  }

  .comment-header {
    flex-direction: column;
    gap: 0.5rem;
  }

  .comment-date {
    align-self: flex-start;
  }

  .btn {
    width: 100%;
  }
}
</style>
