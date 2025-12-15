<template>
  <div class="article-page" :class="{ 'dark-mode': isDark }">
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>در حال بارگیری مقاله...</p>
    </div>
    
    <!-- Error State -->
    <div v-if="error && !loading" class="error-container">
      <h2>خطا در بارگیری مقاله</h2>
      <p>{{ error }}</p>
      <router-link to="/media?tab=articles" class="back-link">بازگشت به لیست مقالات</router-link>
    </div>
    
    <!-- Article Content -->
    <article v-if="article && !loading" 
             class="article-container"
             itemscope 
             itemtype="https://schema.org/Article">
      
      <!-- Breadcrumb -->
      <nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
        <div class="container">
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <router-link to="/" itemprop="item">
              <span itemprop="name">خانه</span>
            </router-link>
            <meta itemprop="position" content="1" />
          </span>
          <span class="separator">/</span>
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <router-link to="/media?tab=articles" itemprop="item">
              <span itemprop="name">مقالات</span>
            </router-link>
            <meta itemprop="position" content="2" />
          </span>
          <span class="separator">/</span>
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span class="current" itemprop="name">{{ article.title }}</span>
            <meta itemprop="position" content="3" />
          </span>
        </div>
      </nav>
      
      <!-- Article Header -->
      <header class="article-header">
        <div class="container">
          <div class="article-category" itemprop="articleSection">{{ article.category }}</div>
          <h1 class="article-title" itemprop="headline">{{ article.title }}</h1>
          <p class="article-excerpt" itemprop="description">{{ article.excerpt }}</p>
          
          <div class="article-meta">
            <div class="author-info" itemprop="author" itemscope itemtype="https://schema.org/Person">
              <div class="author-avatar">{{ article.author_avatar || article.author?.charAt(0) || 'ن' }}</div>
              <div class="author-details">
                <span class="author-name" itemprop="name">{{ article.author || 'نامشخص' }}</span>
                <span class="author-role">{{ article.author_role || 'نویسنده' }}</span>
              </div>
            </div>
            <div class="meta-info">
              <time :datetime="article.created_at" class="meta-item" itemprop="datePublished">
                📅 {{ formatDate(article.created_at) }}
              </time>
              <span class="meta-item">⏱️ {{ article.read_time || '۵ دقیقه' }}</span>
              <span class="meta-item">👁️ {{ article.views || 0 }} بازدید</span>
            </div>
          </div>
        </div>
      </header>
      
      <!-- Article Image -->
      <div class="article-image-container">
        <ImageSlider
          v-if="article.images || article.image"
          :image="article.image"
          :images="article.images"
          :icon="article.icon"
          :gradient="article.gradient"
          class="article-main-image"
          itemprop="image"
        />
      </div>
      
      <!-- Article Body -->
      <div class="article-body">
        <div class="container">
          <div class="content-wrapper">
            <!-- Main Content -->
            <div class="article-content" itemprop="articleBody">
              <div v-if="article.full_content" v-html="article.full_content"></div>
              <div v-else>
                <p>{{ article.content || article.excerpt }}</p>
              </div>
            </div>
            
            <!-- Sidebar -->
            <aside class="article-sidebar">
              <!-- Table of Contents -->
              <div class="sidebar-widget toc-widget">
                <h3>فهرست مطالب</h3>
                <ul class="toc-list">
                  <li><a href="#section-1">مقدمه</a></li>
                  <li><a href="#section-2">محتوای اصلی</a></li>
                  <li><a href="#section-3">نتیجه‌گیری</a></li>
                </ul>
              </div>
              
              <!-- Share Widget -->
              <div class="sidebar-widget share-widget">
                <h3>اشتراک‌گذاری</h3>
                <div class="share-buttons">
                  <button @click="share('twitter')" class="share-btn twitter" aria-label="اشتراک در توییتر">
                    <span>🐦</span>
                  </button>
                  <button @click="share('linkedin')" class="share-btn linkedin" aria-label="اشتراک در لینکدین">
                    <span>💼</span>
                  </button>
                  <button @click="share('telegram')" class="share-btn telegram" aria-label="اشتراک در تلگرام">
                    <span>✈️</span>
                  </button>
                  <button @click="share('whatsapp')" class="share-btn whatsapp" aria-label="اشتراک در واتساپ">
                    <span>💬</span>
                  </button>
                </div>
              </div>
              
              <!-- Related Articles -->
              <div class="sidebar-widget related-widget" v-if="relatedArticles.length">
                <h3>مقالات مرتبط</h3>
                <div class="related-list">
                  <router-link 
                    v-for="related in relatedArticles" 
                    :key="related.id"
                    :to="`/article/${related.id}`"
                    class="related-item"
                  >
                    <div class="related-image">
                      <ImageSlider
                        :image="related.image"
                        :images="related.images"
                        :icon="related.icon"
                        :gradient="related.gradient"
                      />
                    </div>
                    <div class="related-content">
                      <h4>{{ related.title }}</h4>
                      <span class="related-date">{{ formatDate(related.created_at) }}</span>
                    </div>
                  </router-link>
                </div>
              </div>
            </aside>
          </div>
          
          <!-- Tags -->
          <div class="article-tags" v-if="article.tags && article.tags.length" itemprop="keywords">
            <span class="tags-label">برچسب‌ها:</span>
            <span v-for="tag in article.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
          
          <!-- Navigation -->
          <div class="article-navigation">
            <router-link 
              v-if="previousArticle" 
              :to="`/article/${previousArticle.id}`"
              class="nav-btn prev-btn"
            >
              <span class="nav-label">مقاله قبلی</span>
              <span class="nav-title">{{ previousArticle.title }}</span>
            </router-link>
            <router-link 
              v-if="nextArticle" 
              :to="`/article/${nextArticle.id}`"
              class="nav-btn next-btn"
            >
              <span class="nav-label">مقاله بعدی</span>
              <span class="nav-title">{{ nextArticle.title }}</span>
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- بخش نظرات -->
      <div class="container" v-if="article">
        <CommentSection
          content-type="article"
          :content-id="article.id"
          :is-dark="isDark"
        />
      </div>
    </article>
    
    <Footer v-if="!loading" />
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticle, getArticles, getSlider } from '../api/services'
import ImageSlider from '../components/ImageSlider.vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import CommentSection from '../components/CommentSection.vue'

const route = useRoute()
const router = useRouter()
const { isDark, toggleTheme } = inject('theme')

const article = ref(null)
const relatedArticles = ref([])
const previousArticle = ref(null)
const nextArticle = ref(null)
const loading = ref(true)
const error = ref(null)

// Format date to Persian
const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص'
  try {
    return new Date(dateString).toLocaleDateString('fa-IR')
  } catch (e) {
    return dateString
  }
}

// Share functionality
const share = (platform) => {
  const url = window.location.href
  const title = article.value?.title || ''
  
  const urls = {
    twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`,
    telegram: `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
    whatsapp: `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`
  }
  
  if (urls[platform]) {
    window.open(urls[platform], '_blank', 'width=600,height=400')
  }
}

// Enrich article with slider images
const enrichArticleWithSlider = async (articleData) => {
  if (articleData.slider_id) {
    try {
      const sliderResponse = await getSlider(articleData.slider_id)
      if (sliderResponse.data && sliderResponse.data.images) {
        return {
          ...articleData,
          images: sliderResponse.data.images
        }
      }
    } catch (err) {
      console.error('Error loading slider:', err)
    }
  }
  if (articleData.image && !articleData.images) {
    return {
      ...articleData,
      images: [articleData.image]
    }
  }
  return articleData
}

// Update meta tags for SEO
const updateMetaTags = () => {
  if (!article.value) return
  
  const title = `${article.value.title} | مهندسین مشاور دانش‌بنیان BIM`
  const description = article.value.excerpt || article.value.content || ''
  const image = article.value.image || '/og-image.jpg'
  
  document.title = title
  
  // Update or create meta tags
  const metaTags = [
    { name: 'description', content: description },
    { property: 'og:title', content: title },
    { property: 'og:description', content: description },
    { property: 'og:image', content: image },
    { property: 'og:url', content: window.location.href },
    { property: 'og:type', content: 'article' },
    { property: 'article:published_time', content: article.value.created_at },
    { property: 'article:author', content: article.value.author },
    { property: 'article:section', content: article.value.category },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: title },
    { name: 'twitter:description', content: description },
    { name: 'twitter:image', content: image }
  ]
  
  metaTags.forEach(tag => {
    const key = tag.name || tag.property
    const attr = tag.name ? 'name' : 'property'
    let element = document.querySelector(`meta[${attr}="${key}"]`)
    
    if (!element) {
      element = document.createElement('meta')
      element.setAttribute(attr, key)
      document.head.appendChild(element)
    }
    element.setAttribute('content', tag.content)
  })
  
  // Add canonical URL
  let canonical = document.querySelector('link[rel="canonical"]')
  if (!canonical) {
    canonical = document.createElement('link')
    canonical.setAttribute('rel', 'canonical')
    document.head.appendChild(canonical)
  }
  canonical.setAttribute('href', window.location.href)
}

// Fetch article and related data
const fetchArticle = async () => {
  try {
    loading.value = true
    error.value = null
    
    const articleId = route.params.id
    
    // Fetch main article
    const response = await getArticle(articleId)
    let articleData = response.data
    
    // Enrich with slider images
    articleData = await enrichArticleWithSlider(articleData)
    article.value = articleData
    
    // Update meta tags
    updateMetaTags()
    
    // Fetch all articles for related/navigation
    const allArticlesResponse = await getArticles({ page: 1, limit: 100 })
    const allArticles = allArticlesResponse.data || []
    
    // Find related articles (same category, excluding current)
    relatedArticles.value = allArticles
      .filter(a => a.id !== articleData.id && a.category === articleData.category)
      .slice(0, 3)
      .map(a => enrichArticleWithSlider(a))
    
    // Find previous and next articles
    const currentIndex = allArticles.findIndex(a => a.id === articleData.id)
    if (currentIndex > 0) {
      nextArticle.value = allArticles[currentIndex - 1]
    }
    if (currentIndex < allArticles.length - 1) {
      previousArticle.value = allArticles[currentIndex + 1]
    }
    
  } catch (err) {
    console.error('Error fetching article:', err)
    error.value = 'خطا در بارگیری مقاله'
  } finally {
    loading.value = false
  }
}

// Watch for route changes
watch(() => route.params.id, () => {
  if (route.params.id) {
    fetchArticle()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
/* بخش نظرات */
.container .comments-section {
  margin-top: 3rem;
  margin-bottom: 3rem;
}

.article-page {
  min-height: 100vh;
  background: white;
  color: #1a1a1a;
}

.dark-mode.article-page {
  background: #1a1a1a;
  color: #ffffff;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Loading & Error States */
.loading-container,
.error-container {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-container h2 {
  color: #e74c3c;
  margin-bottom: 1rem;
}

.back-link {
  margin-top: 1rem;
  padding: 0.8rem 1.5rem;
  background: #667eea;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
}

.back-link:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

/* Breadcrumb */
.breadcrumb {
  background: #f8f9fa;
  padding: 1rem 0;
  margin-top: 4rem;
}

.dark-mode .breadcrumb {
  background: #2d2d2d;
}

.breadcrumb .container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.breadcrumb a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb a:hover {
  color: #5568d3;
}

.separator {
  color: #999;
}

.current {
  color: #666;
}

.dark-mode .current {
  color: #ccc;
}

/* Article Header */
.article-header {
  padding: 3rem 0;
  text-align: center;
}

.article-category {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.article-title {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.3;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .article-title {
  color: white;
}

.article-excerpt {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.8;
  max-width: 800px;
  margin: 0 auto 2rem;
}

.dark-mode .article-excerpt {
  color: #ccc;
}

.article-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  font-weight: 700;
}

.author-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: right;
}

.author-name {
  font-weight: 600;
  font-size: 1rem;
}

.author-role {
  font-size: 0.85rem;
  color: #999;
}

.meta-info {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.meta-item {
  color: #666;
  font-size: 0.9rem;
}

.dark-mode .meta-item {
  color: #ccc;
}

/* Article Image */
.article-image-container {
  max-width: 1200px;
  margin: 0 auto 3rem;
  padding: 0 2rem;
}

.article-main-image {
  width: 100%;
  height: 500px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* Article Body */
.article-body {
  padding: 3rem 0;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 3rem;
  align-items: start;
}

.article-content {
  font-size: 1.1rem;
  line-height: 1.9;
  color: #333;
}

.dark-mode .article-content {
  color: #ddd;
}

.article-content :deep(h2) {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 2rem 0 1rem;
  color: #1a1a1a;
}

.dark-mode .article-content :deep(h2) {
  color: white;
}

.article-content :deep(h3) {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 1.5rem 0 0.8rem;
}

.article-content :deep(p) {
  margin-bottom: 1.5rem;
}

.article-content :deep(ul),
.article-content :deep(ol) {
  margin: 1.5rem 0;
  padding-right: 2rem;
}

.article-content :deep(li) {
  margin-bottom: 0.8rem;
}

.article-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  margin: 2rem 0;
}

.article-content :deep(blockquote) {
  border-right: 4px solid #667eea;
  padding: 1rem 1.5rem;
  margin: 2rem 0;
  background: #f8f9fa;
  border-radius: 8px;
  font-style: italic;
}

.dark-mode .article-content :deep(blockquote) {
  background: #2d2d2d;
}

/* Sidebar */
.article-sidebar {
  position: sticky;
  top: 6rem;
}

.sidebar-widget {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.dark-mode .sidebar-widget {
  background: #2d2d2d;
}

.sidebar-widget h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .sidebar-widget h3 {
  color: white;
}

/* TOC */
.toc-list {
  list-style: none;
  padding: 0;
}

.toc-list li {
  margin-bottom: 0.8rem;
}

.toc-list a {
  color: #667eea;
  text-decoration: none;
  transition: all 0.3s;
  display: block;
  padding: 0.5rem;
  border-radius: 6px;
}

.toc-list a:hover {
  background: #f0f0f0;
  padding-right: 1rem;
}

.dark-mode .toc-list a:hover {
  background: #3d3d3d;
}

/* Share Buttons */
.share-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.8rem;
}

.share-btn {
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.5rem;
  transition: all 0.3s;
  background: #f0f0f0;
}

.dark-mode .share-btn {
  background: #3d3d3d;
}

.share-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Related Articles */
.related-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.related-item {
  display: flex;
  gap: 1rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  padding: 0.5rem;
  border-radius: 8px;
}

.related-item:hover {
  background: #f0f0f0;
}

.dark-mode .related-item:hover {
  background: #3d3d3d;
}

.related-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.related-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.related-content h4 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-date {
  font-size: 0.8rem;
  color: #999;
}

/* Tags */
.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  padding: 2rem 0;
  border-top: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
  margin: 3rem 0;
  align-items: center;
}

.dark-mode .article-tags {
  border-color: #444;
}

.tags-label {
  font-weight: 600;
  color: #666;
}

.dark-mode .tags-label {
  color: #ccc;
}

.tag {
  padding: 0.5rem 1rem;
  background: #f0f0f0;
  color: #667eea;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s;
}

.dark-mode .tag {
  background: #3d3d3d;
}

.tag:hover {
  background: #667eea;
  color: white;
}

/* Article Navigation */
.article-navigation {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.nav-btn {
  padding: 1.5rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dark-mode .nav-btn {
  background: #2d2d2d;
  border-color: #444;
}

.nav-btn:hover {
  border-color: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.nav-label {
  font-size: 0.85rem;
  color: #999;
  font-weight: 600;
}

.nav-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #667eea;
}

.prev-btn .nav-label::before {
  content: '← ';
}

.next-btn .nav-label::after {
  content: ' →';
}

/* Responsive */
@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }
  
  .article-sidebar {
    position: static;
  }
  
  .sidebar-widget {
    margin-bottom: 1rem;
  }
}

@media (max-width: 768px) {
  .article-title {
    font-size: 1.8rem;
  }
  
  .article-excerpt {
    font-size: 1rem;
  }
  
  .article-meta {
    flex-direction: column;
    gap: 1rem;
  }
  
  .article-main-image {
    height: 300px;
  }
  
  .article-content {
    font-size: 1rem;
  }
  
  .share-buttons {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
