#!/bin/bash

# Testing Script for Media Archive & SEO Implementation
# Run this script to verify all changes are working correctly

echo "🧪 BIM Website - Media Archive & SEO Testing Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to check if file exists
check_file() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} File exists: $1"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} File missing: $1"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Function to check if string exists in file
check_string_in_file() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Found '$2' in $1"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} Missing '$2' in $1"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

echo "📁 Checking Files..."
echo "-------------------"

# Check new files
check_file "src/views/MediaArchive.vue"
check_file "public/robots.txt"
check_file "public/sitemap.xml"
check_file "SEO_GUIDE.md"
check_file "MEDIA_ARCHIVE_IMPLEMENTATION.md"
check_file "IMAGE_SETUP_GUIDE.md"
check_file "QUICK_REFERENCE.md"

echo ""
echo "🔍 Checking Router Configuration..."
echo "------------------------------------"

# Check router imports and routes
check_string_in_file "src/router/index.js" "MediaArchive"
check_string_in_file "src/router/index.js" "path: '/media'"
check_string_in_file "src/router/index.js" "redirect: '/media?tab=gallery'"
check_string_in_file "src/router/index.js" "redirect: '/media?tab=articles'"

echo ""
echo "🏷️  Checking Meta Tags..."
echo "-------------------------"

# Check meta tags in index.html
check_string_in_file "index.html" "og:title"
check_string_in_file "index.html" "og:description"
check_string_in_file "index.html" "og:image"
check_string_in_file "index.html" "twitter:card"
check_string_in_file "index.html" "application/ld+json"
check_string_in_file "index.html" "schema.org"

echo ""
echo "🔗 Checking Navbar Updates..."
echo "-----------------------------"

# Check navbar links
check_string_in_file "src/components/Navbar.vue" "/media?tab=gallery"
check_string_in_file "src/components/Navbar.vue" "/media?tab=articles"

echo ""
echo "📋 Checking SEO Files..."
echo "------------------------"

# Check robots.txt
check_string_in_file "public/robots.txt" "User-agent:"
check_string_in_file "public/robots.txt" "Sitemap:"
check_string_in_file "public/robots.txt" "Disallow: /admin/"

# Check sitemap.xml
check_string_in_file "public/sitemap.xml" "<urlset"
check_string_in_file "public/sitemap.xml" "/media"
check_string_in_file "public/sitemap.xml" "sitemap"

echo ""
echo "🎨 Checking MediaArchive Component..."
echo "-------------------------------------"

# Check MediaArchive.vue
check_string_in_file "src/views/MediaArchive.vue" "itemscope"
check_string_in_file "src/views/MediaArchive.vue" "schema.org/Article"
check_string_in_file "src/views/MediaArchive.vue" "schema.org/CreativeWork"
check_string_in_file "src/views/MediaArchive.vue" "BreadcrumbList"
check_string_in_file "src/views/MediaArchive.vue" "aria-label"

echo ""
echo "📊 Test Summary"
echo "==============="
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Replace 'yourdomain.com' with your actual domain"
    echo "2. Create og-image.jpg and logo.png in /public"
    echo "3. Run: npm run build"
    echo "4. Test in browser"
    echo "5. Validate with Google Rich Results Test"
    exit 0
else
    echo ""
    echo -e "${RED}⚠️  Some tests failed. Please review the errors above.${NC}"
    exit 1
fi
