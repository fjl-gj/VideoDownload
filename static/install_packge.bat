cd /d %~dp0

cd ../

set path=%cd%


for /f  %%i in ('dir "%path%"\\static\\lib_  /b') do (
move "%path%\\static\lib_\\%%i"   "%path%"
echo "%path%\\static\\lib_\\%%i"   "%path%"
)

"%path%\\python"  "%path%"\\static\\apt_get.py

"%path%\\Scripts\\pip" install --upgrade pip

"%path%\\\Scripts\\pip" install  -t "%path%"   -i https://pypi.douban.com/simple/  -r "%path%\\static\\requirements"
