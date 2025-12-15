<template>
  <div class="admin-comments">
    <div class="header">
      <h2>مدیریت نظرات</h2>
      <div class="stats-summary">
        <div class="stat-card">
          <span class="stat-label">کل نظرات</span>
          <span class="stat-value">{{ stats.total }}</span>
        </div>
        <div class="stat-card approved">
          <span class="stat-label">تایید شده</span>
          <span class="stat-value">{{ stats.approved }}</span>
        </div>
        <div class="stat-card pending">
          <span class="stat-label">در انتظار</span>
          <span class="stat-value">{{ stats.pending }}</span>
        </div>
        <div class="stat-card rating">
          <span class="stat-label">میانگین امتیاز</span>
          <span class="stat-value">{{ stats.average_rating }} ⭐</span>
        </div>
      </div>
    </div>

    <!-- فیلترها -->
    <div class="filters">
      <div class="filter-group">
        <label>وضعیت:</label>
        <select v-model="filter.status">
          <option value="all">همه</option>
          <option value="approved">تایید شده</option>
          <option value="pending">در انتظار تایید</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>نوع محتوا:</label>
        <select v-model="filter.contentType">
          <option value="">همه</option>
          <option value="article">مقالات</option>
          <option value="project">پروژه‌ها</option>
        </select>
      </div>
      
      <button @click="fetchComments" class="btn-refresh">
        🔄 بروزرسانی
      </button>
    </div>

    <!-- جدول نظرات -->
    <div class="table-container">
      <table v-if="!loading && comments.length > 0">
        <thead>
          <tr>
            <th>شناسه</th>
            <th>نام</th>
            <th>ایمیل</th>
            <th>نظر</th>
            <th>امتیاز</th>
            <th>نوع</th>
            <th>وضعیت</th>
            <th>تاریخ</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comment in comments" :key="comment.id">
            <td>{{ comment.id }}</td>
            <td>{{ comment.name }}</td>
            <td>{{ comment.email }}</td>
            <td class="comment-content">
              {{ truncateText(comment.content, 50) }}
              <button 
                v-if="comment.content.length > 50" 
                @click="showFullComment(comment)"
                class="view-more"
              >
                بیشتر...
              </button>
            </td>
            <td>
              <div class="rating-display">
                <span class="stars">{{ '⭐'.repeat(comment.rating) }}</span>
                <span class="rating-number">({{ comment.rating }})</span>
              </div>
            </td>
            <td>
              <span class="badge" :class="comment.content_type">
                {{ comment.content_type === 'article' ? 'مقاله' : 'پروژه' }}
              </span>
            </td>
            <td>
              <span 
                class="status-badge" 
                :class="{ approved: comment.approved, pending: !comment.approved }"
              >
                {{ comment.approved ? 'تایید شده' : 'در انتظار' }}
              </span>
            </td>
            <td class="date-cell">{{ formatDate(comment.created_at) }}</td>
            <td class="actions">
              <button
                @click="toggleApprove(comment)"
                :class="['btn-action', comment.approved ? 'btn-warning' : 'btn-success']"
                :title="comment.approved ? 'لغو تایید' : 'تایید'"
              >
                {{ comment.approved ? '✗' : '✓' }}
              </button>
              <button
                @click="deleteCommentAction(comment.id)"
                class="btn-action btn-danger"
                title="حذف"
              >
                🗑
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>در حال بارگیری نظرات...</p>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && comments.length === 0" class="empty-state">
        <p>نظری یافت نشد</p>
      </div>
    </div>

    <!-- Modal نمایش نظر کامل -->
    <div v-if="selectedComment" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button @click="closeModal" class="modal-close">×</button>
        <h3>جزئیات نظر</h3>
        
        <div class="comment-detail">
          <div class="detail-row">
            <strong>نام:</strong>
            <span>{{ selectedComment.name }}</span>
          </div>
          <div class="detail-row">
            <strong>ایمیل:</strong>
            <span>{{ selectedComment.email }}</span>
          </div>
          <div class="detail-row">
            <strong>امتیاز:</strong>
            <span class="stars">{{ '⭐'.repeat(selectedComment.rating) }} ({{ selectedComment.rating }}/5)</span>
          </div>
          <div class="detail-row">
            <strong>نوع:</strong>
            <span>{{ selectedComment.content_type === 'article' ? 'مقاله' : 'پروژه' }} #{{ selectedComment.content_id }}</span>
          </div>
          <div class="detail-row">
            <strong>تاریخ:</strong>
            <span>{{ new Date(selectedComment.created_at).toLocaleString('fa-IR') }}</span>
          </div>
          <div class="detail-row full">
            <strong>متن نظر:</strong>
            <p class="comment-text">{{ selectedComment.content }}</p>
          </div>
        </div>
        
        <div class="modal-actions">
          <button
            @click="toggleApprove(selectedComment); closeModal()"
            :class="['btn', selectedComment.approved ? 'btn-warning' : 'btn-success']"
          >
            {{ selectedComment.approved ? 'لغو تایید' : 'تایید نظر' }}
          </button>
          <button
            @click="deleteCommentAction(selectedComment.id); closeModal()"
            class="btn btn-danger"
          >
            حذف نظر
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getComments, approveComment, deleteComment, getCommentStats } from '../api/services'

const comments = ref([])
const stats = ref({
  total: 0,
  approved: 0,
  pending: 0,
  average_rating: 0
})
const loading = ref(false)
const selectedComment = ref(null)

const filter = ref({
  status: 'all',
  contentType: ''
})

const filteredComments = computed(() => {
  let result = comments.value

  // فیلتر وضعیت
  if (filter.value.status === 'approved') {
    result = result.filter(c => c.approved)
  } else if (filter.value.status === 'pending') {
    result = result.filter(c => !c.approved)
  }

  // فیلتر نوع محتوا
  if (filter.value.contentType) {
    result = result.filter(c => c.content_type === filter.value.contentType)
  }

  return result
})

const fetchComments = async () => {
  loading.value = true
  try {
    const allComments = await getComments({
      approved_only: false
    })
    comments.value = allComments || []
    
    // آمار
    const statsData = await getCommentStats()
    stats.value = statsData
  } catch (error) {
    console.error('Error fetching comments:', error)
  } finally {
    loading.value = false
  }
}

const toggleApprove = async (comment) => {
  try {
    const updated = await approveComment(comment.id)
    comment.approved = updated.approved
    
    // به‌روزرسانی آمار
    if (updated.approved) {
      stats.value.approved++
      stats.value.pending--
    } else {
      stats.value.approved--
      stats.value.pending++
    }
  } catch (error) {
    console.error('Error toggling approval:', error)
    alert('خطا در تغییر وضعیت نظر')
  }
}

const deleteCommentAction = async (commentId) => {
  if (!confirm('آیا از حذف این نظر اطمینان دارید؟')) {
    return
  }
  
  try {
    await deleteComment(commentId)
    comments.value = comments.value.filter(c => c.id !== commentId)
    stats.value.total--
    
    const deletedComment = comments.value.find(c => c.id === commentId)
    if (deletedComment && deletedComment.approved) {
      stats.value.approved--
    } else if (deletedComment) {
      stats.value.pending--
    }
  } catch (error) {
    console.error('Error deleting comment:', error)
    alert('خطا در حذف نظر')
  }
}

const showFullComment = (comment) => {
  selectedComment.value = comment
}

const closeModal = () => {
  selectedComment.value = null
}

const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.admin-comments {
  padding: 2rem;
  direction: rtl;
}

.header {
  margin-bottom: 2rem;
}

.header h2 {
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-card.approved {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-card.pending {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-card.rating {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
}

/* فیلترها */
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #374151;
}

.filter-group select {
  padding: 0.5rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-family: inherit;
}

.btn-refresh {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

/* جدول */
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f9fafb;
}

th {
  padding: 1rem;
  text-align: right;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

tr:hover {
  background: #f9fafb;
}

.comment-content {
  max-width: 300px;
}

.view-more {
  color: #3b82f6;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
  padding: 0;
  margin-right: 0.25rem;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stars {
  font-size: 1rem;
}

.rating-number {
  font-size: 0.875rem;
  color: #6b7280;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.badge.article {
  background: #dbeafe;
  color: #1e40af;
}

.badge.project {
  background: #dcfce7;
  color: #166534;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge.approved {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.pending {
  background: #fed7aa;
  color: #92400e;
}

.date-cell {
  font-size: 0.875rem;
  color: #6b7280;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-action {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-action:hover {
  transform: scale(1.1);
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-warning {
  background: #f59e0b;
  color: white;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  padding: 4rem 2rem;
  text-align: center;
  color: #6b7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 1rem;
  left: 1rem;
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}

.modal-close:hover {
  background: #e5e7eb;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.comment-detail {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem;
}

.detail-row.full {
  grid-template-columns: 1fr;
}

.detail-row strong {
  color: #374151;
}

.comment-text {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
  line-height: 1.7;
  white-space: pre-wrap;
  margin-top: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .admin-comments {
    padding: 1rem;
  }

  .stats-summary {
    grid-template-columns: 1fr;
  }

  .table-container {
    overflow-x: auto;
  }

  table {
    min-width: 800px;
  }

  .detail-row {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
