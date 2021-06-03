# 使用文档

### 1. 经纬度解析

- ##### 准备需要解析的数据

  将需要解析的投递或揽收记录`example.csv`文件放置在`input`文件夹下，并在`input`文件夹下的`file_path.txt`文件中第一行填入需要解析的文件名`example.csv`。

  注意，`example.csv`只是个例子，实际文件名是怎么样的就在`file_path.txt`中填什么文件名。

  - 投递数据的文件格式保证如下，否则程序无法处理

  | 邮件号 | 业务种类 | 地址 | 重量 | 体积重量 | 大客户代码 | 收寄机构代码 | 机构名称 | 收寄日期 | 揽收员 |
  | ------ | -------- | ---- | ---- | -------- | ---------- | ------------ | -------- | -------- | ------ |

  - 揽收数据的文件格式保证如下，否则程序无法处理

  | 投递日期 | 邮件号 | 业务种类 | 重量 | 投递机构 | 机构名称 | 投递员 | 道段 | 投递地址 | 投递方式 | 退回妥投_收件人地址 |
  | -------- | ------ | -------- | ---- | -------- | -------- | ------ | ---- | -------- | -------- | ------------------- |

- ##### 配置记忆位置

  将`buffer`文件夹中的`num1.txt`文件内容改为1。`num1.txt`保存的是`addr_to_lat_lng_1.py`的记忆位置，如果因为异常情况解析中断，程序可从记忆位置开始。因此，如果需要从记忆位置开始，就不必进行这一步。

- ##### 开始解析

  运行`addr_to_lat_lng_1.py`，程序开始解析`file_path.txt`文件中第1行的文件经纬度。出现**Done！**则解析完成。同理，运行`addr_to_lat_lng_2.py`程序对应解析`file_path.txt`文件中第2行的文件经纬度，记得修改buffer中`num2.txt`为1。

  这样解析经纬度的程序一共有4个，使用的是企业高德地图api解析经纬度。

### 2. 合并经纬度文件

运行`combine.py`，程序会生成包含经纬度的记录文件至`output`文件夹下。

合并完的记录文件在原数据的基础上增加了lat和lng两列经纬度属性，并进一步规范了后续代价计算时需要的属性列。

### 3. 代价计算

- ##### 准备工作

  我们需要修改在第2步中生成的记录文件名，揽收文件命名为`lanshou.csv`，投递文件命名为`toudi.csv`。这两个文件即为代价计算所需要的输入文件。

- ##### 开始计算代价

  运行`data.py`，提示输入六个问题的选项，按是和否分别输入y或者n，以空格分开，输入完成之后按下回车。示例如下

  ```
  确保揽收数据输入格式：投递日期,邮件号,业务种类,重量,投递机构,投递员,投递地址,客户号,lng,lat
  确保投递数据输入格式：投递日期,邮件号,业务种类,重量,投递机构,投递员,道段,投递地址,投递方式,lng,lat
  正在读取揽收数据，投递数据...
  读取完成，揽收数据共199条记录，投递数据共199条记录
  是否筛除机构文件之外的记录？
  是否筛除机构管理员的记录？
  是否筛除周末的记录？
  是否筛除围栏之外的记录？
  是否在街道中进行随机分布？
  是否对不完整地址进行随机分布？
  请输入(y/n)，以空格符号分开：y y y y y y
  ```

  程序将输出机构现在的人日均代价`output/cost/res_all.csv`，机构代价`output/cost/res_man.csv`。

### 4. 热力图



### 附录

##### Python库

| arrow       |
| ----------- |
| **numpy**   |
| **pandas**  |
| **pyyaml**  |
| **shapely** |

##### 可修改参数

数据处理的参数设置在`config.yaml`文件中修改，可修改参数为`velocity`和`ratio`，其它尽量不要修改，除非你确定你知道你正在干什么：

```python
('velocity', type=int, default=10, help='Velocity: 揽投员运行速度')
('ratio', type=int, default=24, help='Ratio: 将系数转换为时间/h,设置为24则有平均一件0.05h')
('department', type=str, default='input/info/江门机构.xlsx', help='Department: 需要处理的机构部门文件路径')
('id2name', type=str, default='input/info/工号-作业姓名.xlsx', help='Id2name: 工号-作业姓名文件路径')
('partition', type=str, default='input/info/江门区域划分表.xls', help='Select: CBD等区域划分文件的路径')
('select', type=str, default='input/info/江门机构.xlsx', help='Select: 机构部门经纬度文件的路径')
('weilan', type=str, default='input/info/机构围栏表.xlsx', help="Weilan: 机构围栏表文件路径")
('weilans', type=str, default='input/info/机构围栏坐标点表.csv', help="Weilan: 机构围栏坐标点表文件路径")
```

补充：基础快包一个件算出来权重1.2，1.2 / 24=0.5h，也就是平均一件3min。