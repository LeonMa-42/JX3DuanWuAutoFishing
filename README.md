# JX3DuanWuAutoFishing

本工具用于剑网3端午钓鱼活动,支持原地复活自动进入钓鱼状态。

## 使用方法

1. 在config.ini中设置出杆技能坐标、收杆技能坐标、上钩提示点坐标、上钩提示点颜色、HP检测点坐标、HP检测点颜色、原地复活按钮点坐标、鱼篓坐标。
2. 将视角拉远，角色头部大概与鱼篓重合点击鱼篓进入钓鱼状态
3. exe: 右键钓鱼工具以管理员身份运行; python: 以管理员身份运行命令提示符后，进入脚本目录，输入 `python main.py`

## 图示

![截图](https://user-images.githubusercontent.com/17703150/122660729-069ae680-d1b6-11eb-90a1-bb85590ebc05.png)

## 打包为EXE

1. pip install pyinstaller
2. pyinstaller -F -i ico.ico main.py
