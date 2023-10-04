# VideoDown Project （OLD）

如果按照往常开发中的环境项目结构，加上需要的依赖，一套运行环境下来大概在`400MB`左右

其中`PySide6` 就有`150MB`

使用嵌入式`Python`，结合打包封装，具有一定操作性，打包后大小 `40MB`，封装完`20MB`

注意一定需要：requirements 虚拟环境依赖文件包

### 第一步、梳理项目结构

```python
projects
├─gui_py
|  ├─download
│  └─.*.py
├─static
│  ├─settings
|  ├─.*.json
|  ├─.*.bat
|  ├─requirements
|  └─img
|     └─svg_icons
└─main.py

```

**结构说明：项目拆分为三个部分**

**第一部分 `gui_py`文件，为具体脚本或项目内容结构，包含`py`，`gui`文件等，**

**包含一些脚本整个项目配置文件，**

​	**注意事项：路径使用的路径需要使用`os`模块对项目操作，**

​	**例如引入外部`static`文件内容可以为以下三种形式**

```python
os.path.dirname(os.path.abspath(__file__))
os.path.abspath(os.getcwd())
"static/ima/svg_icons/..."
```

​	**错误形式例如**

```python
"projects/static/ima/svg_icons/..."
```

**第二部分 `static`文件，为静态资源，包含配置文件，数据文件，日志文件，图片视频等静态资源文件**



**第三部分 `main.py`文件，为入口执行文件**

​	**示例：是一段入口文件，单独剥离出来即可**

```python

import os
import sys

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////


from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from app.gui.core.json_settings import Settings
from app.gui.uis.windows.main_window import UiMainWindow, SetupMainWindow
from app.gui.uis.windows.main_window import MainFunctions


# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ...
        ...

    ......


app = QApplication(sys.argv)
app.setWindowIcon(QIcon("icon.ico"))
window = MainWindow()

# EXEC APP
# ///////////////////////////////////////////////////////////////
sys.exit(app.exec())
```

### 第二步、Nuitka，打包

1、安装`Nuitka`打包工具

```python
pip install nuitka

# 如果安装比较慢，可以尝试使用镜像源
pip install -i https://pypi.douban.com/simple/   nuitka
```

2、安装`mingw64`

 网站：`https://sourceforge.net/projects/mingw-w64/`

具体文件下载

```
32位下载：https://sourceforge.net/projects/mingw-w64/files/
找到MinGW-W64 GCC-8.1.0
点击 i686-win32-sjlj 下载
```

![32位下载](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123160214602.png)

```
64位下载：https://sourceforge.net/projects/mingw-w64/files/
找到MinGW-W64 GCC-8.1.0
点击 x86_64-win32-sjlj 下载
```

![64位下载](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123160139926.png)

下载后解压，配置环境变量，不会配置环境变量可以看看文章

`https://blog.csdn.net/qq_42475194/article/details/108548359`

直接看第六步

环境路径为

```
bin目录路径
```

![环境路径](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123160649638.png![image-20211123160916006](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123160916006.png)

![环境变量](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123160821598.png![image-20211123160952885](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123160952885.png)

3、使用`Nuitka`打包

```python
nuitka 
--standalone  
--include-data-dir=static=static 
--mingw64 
--show-progress 
--nofollow-import-to
--follow-import-to=gui  
--windows-icon-from-ico=E:\Download_DL\......\static\images\icon.ico   
--output-dir=E:\Download_DL\......\build  
main.py
```

可复制直接使用命令

```python
nuitka --standalone  --include-data-dir=static=static --mingw64 --show-progress --nofollow-imports --follow-import-to=gui  --windows-icon-from-ico=E:\Download_DL\...\icon.ico  --nofollow-import-to=PySide6,pyside6,shiboken6 --output-dir=E:\Download_DL\...\build  main.py
 
 # 修改--windows-icon-from-ico
 # 修改--follow-import-to=
 # 修改--output-dir=
 # 修改  main.py
```

命令说明：

```
standalone  ：分发文件，打包出来的内容指向 .dist 文件
扩展：其中如果是单个文件，可以使用：onefile
```

![image-20211123161703773](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123161703773.png)

```
include-data-dir ：复制包含所有文件的整个文件夹,顾名思义，打包完后，该文件会保留在打包内容中
扩展：复制目录中的部分或全部文件：include-data-file=<source>=<target>
官方表示还有更好的自动检测包数据并复制：-include-package-data (但未测试)

我这里将自己的静态文件保存，static=static 
```



```
mingw64：c构建 如果在运行中提示下载缓存工具，可以点击Yes
```



```
show-progress：显示进度
```

```
nofollow-import-to：有选择地排除需要编译导入的模块
例如我们在main.py文件中 导入PySide6
那么在编译时候，会将PySide6进行提取，但这是不完全的，所以可以在编译完后删除，或者是在`main.py`文件中调整导入
```

```
follow-import-to：指定需要导入的文件夹，也就是 本次目录结构中的 gui 文件
```

```
windows-icon-from-ico: exe图标icon
```

```
output-dir ： 打包后放在那个地方，这里就是指定输出路径
```

以上是打包DEBUG环境

后面配置好依赖，启动`exe`程序会开启命令行和`exe`桌面应用

```
正式使用需要加上： --windows-disable-console
没有控制台的 Windows 程序不会出错，
出于调试目的，删除--windows-disable-console或使用上述选项--windows-force-stdout-spec和 --windows-force-stderr-spec路径 --windows-onefile-tempdir-spec
```



正式命令

```python
nuitka 
--standalone
--mingw64
--windows-disable-console
--include-data-dir=static=static 
--show-progress 
--nofollow-import-to
--follow-import-to=gui  
--windows-icon-from-ico=E:\Download_DL\......\static\images\icon.ico   
--output-dir=E:\Download_DL\......\build  
main.py
```

配置时间不会很慢，大概三分钟以内，会将python环境编译成`pyd`和`dll`相关文件

![编译完成](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123164137440.png)

```
以上不一一展示，编译完成后，路径打开后缀为.dist文件夹
.build 文件可以放置一边不用操作
然后找到主运行程序。
```

![image-20211123164304109](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123164304109.png)

![image-20211123164347596](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123164347596.png)

编译过的文件结构如下

```python
main.dist
├─static
│  ├─settings
|  ├─.*.json
|  ├─.*.bat
|  ├─requirements
|  └─img
|     └─svg_icons
├─main.exe
├─......dll
└─......dll

# 现有的结构为 main.dist  为项目基础
# static 为静态文件保持不变
# main.exe为主程序入口
# 一些编译好的dll和pyd文件
# 内置环境已经完成，开始集成依赖环境
```



4、配置依赖环境

```python
'''
配置依赖环境建议使用脚本形式操作
windwos环境，可以使用基本的dos操作方法，
加上Python嵌入式环境，基本可以操作
先配置 pip 命令
再配置 安装操作
'''
```

进入`Python`官方下载网站

```
https://www.python.org/downloads/windows/

找到对应版本的python
 Windows x86-64 embeddable zip file  64位
 Windows x86 embeddable zip file     32位
```

![嵌入式Python包](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123165320130.png)

我下载的64位，因为`PySide6`暂时只支持64位下载

```
下载后解压文件夹
```

![Python嵌入式文件](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123165555647.png)

```python
实际上 只需要复制几个文件即可，因为再进行编译配置的时候，已经将Python的基本环境配置好，
只需要配置一些安装pip的配置环境即可
```

![简单配置文件](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123165854233.png)

```
此时将文件复制到static文件夹中，新建立一个lib_文件，将文件拷贝到此文件夹中

名称都可以随意 site-packge
```

![基础环境](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123171113068.png)

```
获取`apt_get.py`文件

打开`https://bootstrap.pypa.io/get-pip.py`

直接复制内容 保存到本地文件
```



```
开始编写bat脚本
文件放置再static 目录下
```

```
# 此时目录结构如下

main.dist
├─static
│  ├─lib_
|  |  ├─python.cat
|  |  ├─python.exe
|  |  ├─python38._pth
|  |  ├─python38.zip
|  |  └─pythonw.exe
|  ├─apt_get.py
|  ├─install_packge.bat
|  ├─requirements
|  └─img
|     └─svg_icons
├─main.exe
├─......dll
└─......dll

# 其中install_packge.bat 脚本为windows环境下执行脚本，逻辑上通用，配置环境
```

**脚本如下**

```bat
cd /d %~dp0

cd ../

set path=%cd%


for /f  %%i in ('dir %path%\\static\\lib_  /b') do (
move "%path%\\static\lib_\\%%i"   "%path%"
echo "%path%\\static\\lib_\\%%i"   "%path%"
)

%path%\\python  %path%\\static\\apt_get.py

%path%\\Scripts\\pip install --upgrade pip

%path%\\\Scripts\\pip install  -t  %path%   -i https://pypi.douban.com/simple/  -r  %path%\\static\\requirements

pause
```

说明

```bat
cd /d %~dp0    : %~dp0 表示当前环境目录  cd 表示切换目录
cd ../         : 表示切换上一层目录 也就是根目录
set path=%cd%  ： %cd% 表示当前路径， 定义变量path 将 路径赋值给path

for /f  %%i in ('dir %path%\\static\\lib_  /b') do (
move "%path%\\static\lib_\\%%i"   "%path%"
echo "%path%\\static\\lib_\\%%i"   "%path%"
)

这里几段for循环操作 主要目的是为了循环遍历文件，然后将文件移动至指定文件夹下 也就是根目录(main.dist)下：
%path%\\python  %path%\\static\\apt_get.py  ：使用python 命令 运行apt_get.py文件 安装pip文件

%path%\\\Scripts\\pip install  -t  %path%  -r  %path%\\static\\requirements  ：使用安装好的 pip 安装依赖文件

重点：-t  %path%  指定pip 安装环境至 指定路径


pause : 可加可不加， 目的是为了暂停命令行，查看具体情况
```

此时可以测试使用脚本，直接点击运行

![image-20211123173432937](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123173432937.png)

![依赖文件](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123173718644.png)

```
根目录下，一些需要的依赖文件
```



```
测试 点击 exe 程序查看是否可以运行，如果可以运行，即可将static 文件作为 开发中迭代更新文件，进行保存

此时若打开 exe 程序 会弹出命令行的框，那么在编译时候加上
--windows-disable-console
即可
```



### 第三步、inno  setup 封装

1、 下载安装 `inno setup`

```
https://jrsoftware.org/isdl.php
选择Random site 或有快捷方式即可
正常安装即可
```

![image-20211123174327809](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123174327809.png)



2、配置项目

```
安装成功后
开始配置项目
```

**创建新文件**

![创建新文件](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123174659827.png)

**点击Next**

![欢迎创建 安装脚本](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123174820291.png)

**应用信息**

```
Application name：      应用名称 必填
Application version：   应用版本 必填
Application publisher： 应用创作人或公司 非必填
Application website：   应用web站点     非必填 (没有就不用填写)
```

![应用信息](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123174928161.png)

**应用文件**

```python
'''
Application destination base folder: 应用程序目标基础文件夹
Application folder name:             应用程序文件夹名称   这里是表示安装后，应用名称
Allow user to ghange the application folder：允许用户改变应用程序文件夹
也就是表述 在安装的时候，选择安装目录，原本安装到C盘，可以更改到D盘
other
The application doesn't need a folder：应用程序不需要文件夹
'''
```

![image-20211123175305818](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123175305818.png)

应用程序文件

```
Application main executable file： 应用程序主可执行文件  选择exe文件
Allow user to start the application after Setup has finished：
允许用户在安装完成后启动应用程序
The application doesn't have a main executable file ：应用程序没有主可执行文件

下方添加主目录 也就是本程序的main.dist文件夹
```

![应用程序文件](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123180235886.png)

```
Associate a file type to the main executable ：将文件类型与主可执行文件关联
Application file type name：应用程序文件类型名称
Application file type extensionexel：应用程序文件类型
这里填写为exe即可
```

![image-20211123180551217](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123180551217.png)

应用程序的快捷方式

```
Create a shortcut to the main executable in the Start Menu Programs foldert ：
在"开始菜单程序"文件夹中创建主可执行文件的快捷方式

Application Start Menu folder name: 应用程序开始菜单文件夹名称

Allow user to change the Start Menu folder name :允许用户改变开始菜单文件夹名称

Allow uSer to disable Start Menu folder creation :允许用户改变开始菜单文件夹名称
Create an Internet shortcut in the Start Menu folder :在“开始菜单”文件夹中创建Internet快捷方式
Create an Uninstall shor tcut in the Start Menu folder ：在开始菜单文件夹中创建一个卸载快捷方式
Other shortcuts to the main executable: 主可执行文件的其他快捷方式
Allow user to create a desktop shortcut ：允许用户创建桌面快捷方式
```

![image-20211123180617849](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123180617849.png)

应用程序文档

```
Please specify which documentation files should be shown by Setup during installation：
请指定安装过程中安装程序应该显示哪些文档文件

license file ：许可文件
Information file shown hefore installation：安装前显示的信息文件
Information file shown after installation ：安装后显示的信息文件
```

![image-20211123181120985](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123181120985.png)

**安装运行方式**

```
Administrative install mode (install for all users)：管理安装模式(为所有用户安装)
Non administrative install mode finstall for current user only)：非管理安装模式安装仅适用于当前用户)

Allow user to gverride the install mode via the command line：允许用户通过命令行控制安装模式
Ask the user to choose the install mode at startup： 要求用户在启动时选择安装模式
```

![安装运行方式](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123181815888.png)

**语言配置**

```
注意中文配置，可以网上获取
https://jrsoftware.org/files/istrans/
然后保存至Inno Setup 6\Languages 文件夹下
```

![image-20211123181847821](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123181847821.png)

![image-20211123182455513](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123182455513.png)

**编译器设置**

```
Custom compiler outout folder: 自定义编译器输出文件夹:
Compiler outout hase file name: 编译器输出hase文件名
Custom Setun icon file： 自定义Setun图标文件
Setup password:设置密码
```

![image-20211123182821113](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123182821113.png)

**`Inno`设置预处理器**

```
Yes, use #define compiler directives ：是的，使用#define编译器指令
```

![image-20211123182846569](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123182846569.png)

Finish

![image-20211123183030930](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123183030930.png)

```
Inno Setup CompilerWould you like to compile the new script now?:
你现在想编译新脚本吗?

这里选择否
```

保存配置文件

![image-20211123183225816](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123183225816.png)

再[RUN]中加入需要执行的脚本文件

```
Filename: "{app}\static\install_packge.bat"; StatusMsg: "InstallDependency package file"; Flags: skipifsilent
```

![image-20211123183527294](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123183527294.png)

加入完保存

最后运行编译

![image-20211123183742634](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123183742634.png)

![image-20211123183747417](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123183747417.png)

点击取消即可

![image-20211123183848575](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123183848575.png)

然后找到封装好的应用

![image-20211123184142233](C:\Users\Administration\AppData\Roaming\Typora\typora-user-images\image-20211123184142233.png)
