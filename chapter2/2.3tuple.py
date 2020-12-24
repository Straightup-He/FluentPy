#-*- coding = utf-8 -*-
#@Time : 2020/12/1 11:53
#@Author : straightup

# 元组的拆包
# 分别提取元组中的数据
traveler_ids = [('USA', '31124266'), ('BRA', 'CE5672332'), ('ESP', 'XDA20865')]
for passport in traveler_ids:
    print('%s/%s' % passport)
"""
USA/31124266    BRA/CE5672332   ESP/XDA20865
"""
# _占位符
for country, _ in traveler_ids:
    print(country)
"""
USA BRA ESP
"""

# ------------------------ 具名元组 -----------------------------
from collections import namedtuple

# 定义一个城市类
# City = namedtuple('City', ['name', 'country', 'population', 'coordinates'])
City = namedtuple('City', 'name country population coordinates')

tokyo = City('Tokoy', 'JP', 36.933, (35.68, 139.69))

# 可通过字段名或位置获取信息
print(tokyo)  # City(name='Tokoy', country='JP', population=36.933, coordinates=(35.68, 139.69))
print(tokyo.population)  # 36.933
print(tokyo[1])  # JP

# 具名元组的专有属性
# _fields 获取类属性
print(City._fields)  # ('name', 'country', 'population', 'coordinates')




