# تنظیمات تصاویر برای SEO

## تصاویر مورد نیاز

### 1. OG Image (Open Graph Image)
**مسیر:** `/public/og-image.jpg`

**مشخصات:**
- ابعاد: 1200 × 630 پیکسل
- فرمت: JPG یا PNG
- حجم: کمتر از 1 مگابایت
- محتوا: لوگو شرکت + نام شرکت + یک تصویر مرتبط

**استفاده:**
این تصویر هنگام اشتراک‌گذاری لینک وب‌سایت در شبکه‌های اجتماعی (فیسبوک، توییتر، لینکدین، تلگرام، واتساپ) نمایش داده می‌شود.

### 2. Logo
**مسیر:** `/public/logo.png`

**مشخصات:**
- ابعاد: 512 × 512 پیکسل (مربع)
- فرمت: PNG با پس‌زمینه شفاف
- حجم: کمتر از 500 کیلوبایت

**استفاده:**
برای Schema.org markup و نمایش در نتایج جستجو.

### 3. Favicon
**مسیر:** `/public/favicon.png` (موجود است)

**مشخصات:**
- ابعاد: 32 × 32 یا 64 × 64 پیکسل
- فرمت: PNG یا ICO

## نحوه ساخت OG Image

### روش 1: استفاده از Canva
1. به https://www.canva.com بروید
2. یک طرح با ابعاد 1200 × 630 ایجاد کنید
3. عناصر زیر را اضافه کنید:
   - لوگو شرکت (گوشه بالا)
   - نام شرکت (با فونت واضح)
   - شعار یا توضیح کوتاه
   - یک تصویر پس‌زمینه مرتبط با BIM/ساختمان
4. رنگ‌های شرکتی را استفاده کنید (#667eea, #764ba2)
5. دانلود به عنوان JPG

### روش 2: استفاده از Figma/Photoshop
```
ابعاد: 1200 × 630 پیکسل
Safe Zone: 1200 × 600 پیکسل (60px padding از بالا و پایین)

Layout:
┌──────────────────────────────────┐
│  Logo                            │
│                                  │
│   مهندسین مشاور دانش‌بنیان BIM   │
│   Building Information Modeling  │
│                                  │
│   [Background Image]             │
└──────────────────────────────────┘
```

### روش 3: استفاده از ابزار آنلاین
- https://www.ogimage.xyz/
- https://www.bannerbear.com/
- https://placid.app/

## تصاویر اضافی برای مقالات و گالری

### تصاویر مقالات:
**فرمت:** WebP (توصیه می‌شود) یا JPG
**ابعاد توصیه شده:** 1200 × 675 پیکسل (16:9)
**حجم:** کمتر از 300 کیلوبایت

### تصاویر گالری:
**فرمت:** WebP (توصیه می‌شود) یا JPG
**ابعاد توصیه شده:** 1200 × 900 پیکسل (4:3)
**حجم:** کمتر از 400 کیلوبایت

## بهینه‌سازی تصاویر

### ابزارهای فشرده‌سازی:
1. **TinyPNG**: https://tinypng.com/
2. **Squoosh**: https://squoosh.app/
3. **ImageOptim** (Mac): https://imageoptim.com/

### دستور خط فرمان (برای تبدیل به WebP):
```bash
# نصب cwebp
brew install webp  # MacOS
apt-get install webp  # Linux

# تبدیل تصویر
cwebp input.jpg -q 80 -o output.webp
```

## مثال OG Image

```html
<!-- در index.html -->
<meta property="og:image" content="https://b1m.ir/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="مهندسین مشاور دانش‌بنیان BIM - مدل‌سازی اطلاعات ساختمان">
```

## تست کردن OG Image

### ابزارهای تست:
1. **Facebook Sharing Debugger**: https://developers.facebook.com/tools/debug/
2. **Twitter Card Validator**: https://cards-dev.twitter.com/validator
3. **LinkedIn Post Inspector**: https://www.linkedin.com/post-inspector/
4. **Open Graph Check**: https://www.opengraph.xyz/

## Alt Text برای تصاویر

### نمونه‌های خوب:
```html
<!-- مقاله -->
<img src="article-bim.jpg" alt="نمای سه‌بعدی مدل BIM یک ساختمان مسکونی">

<!-- گالری -->
<img src="project-01.jpg" alt="پروژه مدل‌سازی BIM برج تجاری در تهران">
```

### نمونه‌های بد:
```html
<!-- خیلی کلی -->
<img src="image.jpg" alt="تصویر">

<!-- خیلی طولانی -->
<img src="image.jpg" alt="این تصویر نشان می‌دهد که چگونه ما با استفاده از نرم‌افزار Revit و...">
```

## Lazy Loading

```vue
<!-- در Vue Components -->
<img 
  :src="image" 
  :alt="imageAlt"
  loading="lazy"
  decoding="async"
>
```

## Responsive Images

```vue
<picture>
  <source 
    srcset="image-large.webp" 
    media="(min-width: 1024px)" 
    type="image/webp"
  >
  <source 
    srcset="image-medium.webp" 
    media="(min-width: 768px)" 
    type="image/webp"
  >
  <img 
    src="image-small.jpg" 
    alt="توضیحات تصویر"
    loading="lazy"
  >
</picture>
```

## چک‌لیست تصاویر

- [ ] OG image ساخته شده (1200 × 630)
- [ ] Logo آپلود شده (512 × 512)
- [ ] Favicon موجود است
- [ ] تمام تصاویر فشرده شده‌اند
- [ ] Alt text برای همه تصاویر
- [ ] Lazy loading فعال است
- [ ] تصاویر responsive هستند
- [ ] فرمت WebP استفاده شده (در صورت امکان)
- [ ] OG tags تست شده
- [ ] تصاویر در mobile به خوبی نمایش داده می‌شوند

---

**نکته مهم:** پس از آپلود og-image.jpg، URL را در index.html به‌روزرسانی کنید:
```html
<meta property="og:image" content="https://b1m.ir/og-image.jpg">
```
