@echo off
REM Xóa tất cả thư mục __pycache__ và file .pyc trong dự án
for /d /r . %%d in (__pycache__) do if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc
echo Đã dọn dẹp xong __pycache__ và file .pyc!
pause
