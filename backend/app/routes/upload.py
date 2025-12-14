from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import shutil
from pathlib import Path

from app.database import get_db
from app import models, auth

router = APIRouter(prefix="/api/upload", tags=["Upload"])

# مسیر ذخیره فایل‌ها
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# انواع فایل مجاز
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_file(file: UploadFile):
    """اعتبارسنجی فایل آپلودی"""
    # بررسی پسوند
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فرمت فایل مجاز نیست. فرمت‌های مجاز: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    return file_ext


def save_upload_file(upload_file: UploadFile, request=None) -> str:
    """ذخیره فایل و برگرداندن URL"""
    # اعتبارسنجی
    file_ext = validate_file(upload_file)
    
    # ایجاد نام یونیک
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # ذخیره فایل
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ذخیره فایل: {str(e)}"
        )
    
    # برگرداندن URL مطلق
    backend_url = None
    
    # ابتدا بررسی کنید BACKEND_URL environment variable (دقیق‌ترین روش)
    backend_url = os.getenv("BACKEND_URL")
    
    # اگر BACKEND_URL تعیین نشده است و request موجود است، از headers استفاده کنید
    if not backend_url and request:
        # از X-Forwarded-Proto و X-Forwarded-Host استفاده کنید (برای proxy)
        forwarded_proto = request.headers.get("X-Forwarded-Proto", request.url.scheme)
        forwarded_host = request.headers.get("X-Forwarded-Host", request.url.netloc)
        
        # اگر Host localhost است، مطمئن باشید از HTTPS استفاده نمی‌کنیم
        if "localhost" not in forwarded_host:
            backend_url = f"{forwarded_proto}://{forwarded_host}"
    
    # Fallback
    if not backend_url:
        backend_url = "http://localhost:8000"
    
    print(f"📤 Upload: saving to {backend_url}/uploads/{unique_filename}")
    
    return f"{backend_url}/uploads/{unique_filename}"


@router.post("", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    request: Request = None,
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """آپلود تصویر (فقط ادمین)"""
    try:
        file_url = save_upload_file(file, request)
        
        return {
            "success": True,
            "message": "تصویر با موفقیت آپلود شد",
            "url": file_url
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )


@router.post("/batch", response_model=dict)
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    request: Request = None,
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """آپلود چند تصویر برای اسلایدر (فقط ادمین)"""
    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="حداکثر 10 تصویر می‌توانید آپلود کنید"
        )
    
    uploaded_urls = []
    errors = []
    
    for file in files:
        try:
            file_url = save_upload_file(file, request)
            uploaded_urls.append(file_url)
        except HTTPException as e:
            errors.append({"filename": file.filename, "error": str(e.detail)})
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})
    
    return {
        "success": len(uploaded_urls) > 0,
        "message": f"{len(uploaded_urls)} تصویر با موفقیت آپلود شد",
        "urls": uploaded_urls,
        "errors": errors if errors else None
    }


@router.delete("", response_model=dict)
async def delete_image(
    url: str,
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف تصویر (فقط ادمین)"""
    # استخراج نام فایل از URL
    filename = url.split("/")[-1]
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فایل یافت نشد"
        )
    
    try:
        file_path.unlink()
        return {
            "success": True,
            "message": "تصویر با موفقیت حذف شد"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در حذف فایل: {str(e)}"
        )
