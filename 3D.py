from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import  matplotlib.font_manager as fm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
from itertools import chain
from numpy.random import rand
from pylab import figure
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation
from mpl_toolkits.mplot3d.art3d import Line3DCollection

#定义3D注释函数
class Annotation3D(Annotation):
    '''Annotate the point xyz with text s'''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz        

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)

def annotate3D(ax, s, *args, **kwargs):
    '''add anotation text s to to Axes3d ax'''
    tag = Annotation3D(s, *args, **kwargs)
    ax.add_artist(tag)

fig = plt.figure()
ax = Axes3D(fig)

# X,Y数据录入
X = np.array([1,2,3])
Y = np.array([1,2,3])
X, Y = np.meshgrid(X, Y)
print("网格化后的X=",X)
print("X维度信息",X.shape)
print("网格化后的Y=",Y)
print("Y维度信息", Y.shape)

# Z轴数据,曲面数据
Z = np.array(
    [
    [0.5,	0.25,	0.333],   #1 4 7
    [0.4,	1,	0.125],   #2 5 8
    [0.5,	0.5,	0.2],   #3 6 9
    
    ]
             )

I = np.array([1,2,3])
J = np.array([1,2,3])
I, J = np.meshgrid(I, J)

# H轴数据（投影点）
H = np.array(
    [
    [0,0,0],
    [0,0,0],
    [0,0,0],

    ]
             )

print("维度调整前的Z轴数据维度喵",Z.shape)
Z = Z.T
print("维度调整后的Z轴数据维度喵",Z.shape)

# 绘制三维曲面图
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='lightskyblue', alpha = 0.6)

#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimSun'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#设置三个坐标轴信息
#ax.set_xlabel('X$_i$', color='b',fontsize=15)
#ax.set_ylabel('X$_j$', color='g',fontsize=15)
ax.set_zlabel('各一级变量得分', color='black',fontsize=10)

# 隐藏坐标轴
plt.xticks([])
plt.yticks([])

ax.scatter(X, Y, Z, c='r', marker = '.') #画散点图
ax.scatter(I, J, H, c='b', marker = '.') #画散点图

ax.set_zticks(np.arange(0,2,step=0.1))
ax.set_zlim(0,1) #设置显示范围，否则，scatter函数会miss掉zticks，详情：https://stackoverflow.com/questions/48392010/matplotlib-pyplot-incorrectly-setting-axes-ticks-when-using-scatter

# 调整视角
ax.view_init(
             elev=23,    # 仰角
             azim=-132    # 方位角
            )

#连接线的实现
XX = X.flatten()
YY = Y.flatten()
ZZ = Z.flatten()
II = I.flatten()
JJ = J.flatten()
HH = H.flatten()

for i in range(9):
    ax.plot([XX[i], II[i]], [YY[i],JJ[i]],zs=[ZZ[i],HH[i]],color = 'r',linewidth=0.3)
#2021,2,2,23:32,终于实现了连线功能！原来是要修改为一维数组,另外详见：https://stackoverflow.com/questions/11541123/how-can-i-make-a-simple-3d-line-with-matplotlib

#把一维数组又转化成二维矩阵
m = np.vstack((XX,YY,ZZ)).T
n = np.vstack((II,JJ,HH)).T

XYZ = zip( XX, YY, ZZ )
IJH = zip( II, JJ, HH )

#使用自定义的3D标注函数对坐标点进行标注
for j, xyz_ in enumerate(XYZ): 
  annotate3D(ax, s=str(ZZ[j]), xyz=xyz_, fontsize=12, xytext=(0,10),color = 'r', textcoords='offset points', ha='right',va='top')    

for j, xyz_ in enumerate(IJH):
  annotate3D(ax,'${X_%d}$' %(j+1), xyz=xyz_,color='b', fontsize=10, xytext=(-5,1), textcoords='offset points', ha='right',va='bottom')    
#2020,2,6,0:38,主体功能大致实现！

plt.draw()
plt.show()
plt.savefig('3D.jpg')