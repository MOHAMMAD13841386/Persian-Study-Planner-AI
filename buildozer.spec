[app]

# نام برنامه
title = برنامه‌ریز درسی فارسی

# نام پکیج (تغییر بده به دلخواه)
package.name = persianstudyapp

# دامنه پکیج (تغییر بده)
package.domain = com.yourname

# نسخه
version = 1.0
version.code = 1

# مسیر سورس
source.dir = .

# فایل اصلی
source.main = main.py

# کتابخانه‌های مورد نیاز
requirements = python3,kivy==2.1.0,numpy==1.21.0

# دسترسی‌های اندروید
android.permissions = INTERNET

# تنظیمات اندروید
android.api = 30
android.minapi = 21
android.sdk = 24
android.ndk = 23b

# جهت صفحه
orientation = portrait

# تمام صفحه
fullscreen = 0

# نوع بیلد
android.release_artifact = .apk

# معماری
android.arch = armeabi-v7a

# لوگ
log_level = 2
