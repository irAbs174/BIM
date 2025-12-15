# راهنمای SEO برای وب‌سایت BIM

این سند شامل تمام اقدامات انجام شده برای بهینه‌سازی موتور جستجو (SEO) در وب‌سایت است.

## 📋 فهرست مطالب
1. [صفحه یکپارچه مقالات و گالری](#صفحه-یکپارچه-مقالات-و-گالری)
2. [تگ‌های متا (Meta Tags)](#تگ‌های-متا)
3. [Schema.org Markup](#schemaorg-markup)
4. [Sitemap و Robots.txt](#sitemap-و-robotstxt)
5. [بهینه‌سازی عملکرد](#بهینه‌سازی-عملکرد)
6. [دستورالعمل‌های بیشتر](#دستورالعمل‌های-بیشتر)

---

## صفحه یکپارچه مقالات و گالری

### مسیر جدید
```
/media (صفحه اصلی)
/media?tab=articles (نمایش مقالات)
/media?tab=gallery (نمایش گالری)
```

### ویژگی‌ها:
- ✅ یک URL واحد برای هر دو بخش
- ✅ تب‌های قابل تعویض بدون رفرش صفحه
- ✅ Breadcrumb navigation با Schema.org
- ✅ عناوین و توضیحات بهینه شده
- ✅ تصاویر با alt text
- ✅ محتوای ساختاریافته

### ریدایرکت URL‌های قدیمی
```javascript
/articles → /media?tab=articles
/gallery → /media?tab=gallery
```

---

## تگ‌های متا

### تگ‌های اصلی در `index.html`:

#### Primary Meta Tags
```html
<title>مهندسین مشاور دانش‌بنیان BIM | مدل‌سازی اطلاعات ساختمان</title>
<meta name="title" content="...">
<meta name="description" content="...">
<meta name="keywords" content="BIM, مدل‌سازی اطلاعات ساختمان, ...">
<meta name="author" content="مهندسین مشاور دانش‌بنیان BIM">
<meta name="robots" content="index, follow">
```

#### Open Graph (Facebook)
```html
<meta property="og:type" content="website">
<meta property="og:url" content="https://b1m.ir/">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="...">
<meta property="og:locale" content="fa_IR">
```

#### Twitter Cards
```html
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="...">
<meta property="twitter:title" content="...">
<meta property="twitter:description" content="...">
<meta property="twitter:image" content="...">
```

### تگ‌های داینامیک در هر صفحه:
صفحه MediaArchive به صورت خودکار تگ‌های متا را بر اساس تب فعال به‌روز می‌کند.

---

## Schema.org Markup

### Organization Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "مهندسین مشاور دانش‌بنیان BIM",
  "url": "https://b1m.ir",
  "logo": "https://b1m.ir/logo.png",
  "contactPoint": { ... }
}
```

### Website Schema
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "مهندسین مشاور دانش‌بنیان BIM",
  "url": "https://b1m.ir",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "..."
  }
}
```

### Article Schema (در هر مقاله)
```html
<article itemscope itemtype="https://schema.org/Article">
  <h2 itemprop="headline">عنوان مقاله</h2>
  <time itemprop="datePublished" datetime="...">تاریخ</time>
  <span itemprop="author">نویسنده</span>
  <div itemprop="articleSection">دسته‌بندی</div>
  <p itemprop="description">خلاصه مقاله</p>
</article>
```

### CreativeWork Schema (در هر پروژه گالری)
```html
<div itemscope itemtype="https://schema.org/CreativeWork">
  <h2 itemprop="name">عنوان پروژه</h2>
  <p itemprop="description">توضیحات</p>
  <time itemprop="dateCreated">تاریخ</time>
</div>
```

### Breadcrumb Schema
```html
<nav itemscope itemtype="https://schema.org/BreadcrumbList">
  <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
    <a itemprop="item" href="/"><span itemprop="name">خانه</span></a>
    <meta itemprop="position" content="1" />
  </span>
</nav>
```

---

## Sitemap و Robots.txt

### Sitemap.xml
فایل `/public/sitemap.xml` شامل:
- صفحه اصلی (priority: 1.0)
- صفحه مقالات و گالری (priority: 0.9)
- تب مقالات (priority: 0.8)
- تب گالری (priority: 0.8)

**به‌روزرسانی:** هر هفته یا هنگام افزودن محتوای جدید

### Robots.txt
فایل `/public/robots.txt`:
```
User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://b1m.ir/sitemap.xml
```

---

## بهینه‌سازی عملکرد

### تصاویر
- ✅ استفاده از فرمت WebP (توصیه می‌شود)
- ✅ Lazy loading برای تصاویر
- ✅ Alt text برای همه تصاویر
- ✅ Responsive images

### کد
- ✅ Code splitting
- ✅ Lazy loading components
- ✅ Minification در production
- ✅ Tree shaking

### شبکه
- ✅ Preconnect به منابع خارجی
- ✅ Preload فونت‌ها
- ✅ HTTP/2
- ✅ Compression (gzip/brotli)

---

## دستورالعمل‌های بیشتر

### 1. ثبت در Google Search Console
```
1. به https://search.google.com/search-console بروید
2. وب‌سایت را اضافه کنید
3. مالکیت را تأیید کنید
4. Sitemap را ثبت کنید: https://b1m.ir/sitemap.xml
```

### 2. ثبت در Google Analytics
```javascript
// اضافه کردن Google Analytics به index.html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 3. اضافه کردن Canonical URLs
در هر صفحه:
```html
<link rel="canonical" href="https://b1m.ir/current-page">
```

### 4. بهینه‌سازی سرعت
```bash
# تست سرعت
npm run build
npm run preview

# استفاده از ابزارها:
# - Google PageSpeed Insights
# - GTmetrix
# - WebPageTest
```

### 5. SSL Certificate
مطمئن شوید وب‌سایت از HTTPS استفاده می‌کند.

### 6. Mobile-Friendly
تمام صفحات responsive هستند و در موبایل به خوبی کار می‌کنند.

### 7. Accessibility (A11y)
- ✅ ARIA labels
- ✅ Semantic HTML
- ✅ Keyboard navigation
- ✅ Screen reader support

---

## چک‌لیست SEO

### قبل از انتشار:
- [ ] تمام متادیتاها را بررسی کنید
- [ ] Sitemap را به‌روز کنید
- [ ] robots.txt را بررسی کنید
- [ ] تمام لینک‌های داخلی را تست کنید
- [ ] Canonical URLs را بررسی کنید
- [ ] Schema.org markup را تست کنید (با Google Rich Results Test)
- [ ] سرعت بارگذاری را بررسی کنید
- [ ] Mobile responsiveness را تست کنید
- [ ] 404 pages را بررسی کنید

### بعد از انتشار:
- [ ] در Google Search Console ثبت کنید
- [ ] در Google Analytics ثبت کنید
- [ ] Sitemap را submit کنید
- [ ] Social media profiles را به‌روز کنید
- [ ] Backlinks بسازید
- [ ] محتوای منظم منتشر کنید

---

## ابزارهای مفید

### تست و بررسی:
1. **Google Search Console**: https://search.google.com/search-console
2. **Google PageSpeed Insights**: https://pagespeed.web.dev/
3. **Google Rich Results Test**: https://search.google.com/test/rich-results
4. **Google Mobile-Friendly Test**: https://search.google.com/test/mobile-friendly
5. **Schema.org Validator**: https://validator.schema.org/

### تحلیل:
1. **Google Analytics**: https://analytics.google.com/
2. **Google Tag Manager**: https://tagmanager.google.com/
3. **Hotjar** (User behavior): https://www.hotjar.com/

### ابزارهای SEO:
1. **Ahrefs**
2. **SEMrush**
3. **Moz**
4. **Screaming Frog SEO Spider**

---

## نکات مهم

### کلمات کلیدی فارسی:
```
- BIM
- مدل‌سازی اطلاعات ساختمان
- طراحی معماری
- طراحی سازه
- تاسیسات مکانیکی
- تاسیسات الکتریکی
- نظارت ساختمانی
- مهندسین مشاور
- Revit
- AutoCAD
```

### بهینه‌سازی محتوا:
1. عناوین واضح و توصیفی
2. پاراگراف‌های کوتاه و خوانا
3. استفاده از لیست‌ها
4. تصاویر با کیفیت
5. لینک‌های داخلی
6. محتوای منحصر به فرد
7. به‌روزرسانی منظم

### Local SEO (برای ایران):
```html
<meta property="og:locale" content="fa_IR">
<meta name="geo.region" content="IR">
<meta name="geo.placename" content="Tehran">
```

---

## پشتیبانی و سوالات

برای سوالات بیشتر یا کمک در بهینه‌سازی SEO، به مستندات زیر مراجعه کنید:
- [Google Search Central](https://developers.google.com/search)
- [Schema.org Documentation](https://schema.org/)
- [Vue.js SEO Guide](https://vuejs.org/guide/scaling-up/ssr.html)

---

**آخرین به‌روزرسانی:** 15 دسامبر 2025
