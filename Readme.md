餐饮评论打分系统

学号：10175101250
姓名：李嘉睿

网站名称：YumScore!

技术：
前端：jquery + bootstrap
后端：Django框架（模板、模型、视图）

依赖：
Django版本：2.1
python版本：3.7
python包：pymysql、PIL、pillow、django

下载数据集：
https://www.yelp.com/dataset/download

管理员账号：root
管理员密码：root

部署方法（具体方法见部署pdf文件）：
1. 通过pycharm打开项目
2. 在mysite/settings.py文件中修改mysql数据库的用户名和密码，同时修改数据存放的数据库名称
3. 登入mysql，建立该数据库
4. 使用命令构建数据模式
	python manage.py makemigrations
	python manage.py migrate
5. 下载数据集并解压
6. 修改mysite/script.py中数据集解压后json文件的位置
7. 执行脚本文件将数据入库
8. 通过网址127.0.0.1:8000/scoringsystem/即登录网址主页
9. 管理站点是127.0.0.1:8000/admin/