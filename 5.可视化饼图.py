import pandas
import matplotlib.pyplot as plt #可视化图表
# 防止乱码
plt.rcParams['font.family'] = ['Microsoft Yahei', 'SimHei', 'sans-serif']
data = pandas.read_excel("job.xlsx")
data['学历'].value_counts().plot.pie(
    figsize=(8, 8),  # 图像大小
    autopct='%1.1f%%',  # 显示百分比
    pctdistance=0.9,    # 数据标签距离圆心的位置
    # 因为我只有40条数据，所以学历只有4中
    # 34页完整数据，里面就写6个参数 explode=(0,0,0,0,0.1,0.2)
    explode=(0,0,0.1,0.2),    # 突出显示块
    startangle=90,   # 旋转角度
)
# 图表显示
plt.show()
