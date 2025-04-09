import os
import sys
import matplotlib.pyplot as plt
from networkx.algorithms.bipartite.basic import color
from shapely.geometry.polygon import orient
import time

class Plotting:
    def __init__(self, xI, xG, env):
        self.xI, self.xG = xI, xG
        self.env = env
        self.cross_barriers = self.env.cross_barriers
        self.avoid_barriers = self.env.avoid_barriers
        self.boundary = self.env.boundary_map()
    
    def plot_map(self, name, path="temp.png", show=False):
        plt.clf()
        self.plot_grid(name)

        plt.savefig(path)
        if show:
            plt.show()
        plt.close()

    def llmPoint(self, target):
        plt.clf()
        self.plot_grid("name")
        for i, (x, y) in enumerate(target):
            plt.plot(x, y, "o", color=self.color_list_2()[i], markersize=9)
        plt.show()
        plt.close()

    def animation(self, path, visited, show, name, filepath):
        # plt.clf()
        self.plot_grid(name)
        self.plot_visited(visited)
        if path:
            self.plot_path(path)
        plt.legend(loc="upper center",  ncol=3, fontsize=11, framealpha=0.5)
        plt.xlim(-5, self.env.x_range+5)  # 设置x轴的范围
        plt.ylim(-5, self.env.y_range+7)
        # 隐藏坐标和刻度
        plt.axis('off')
        plt.savefig(filepath)
        if show:
            plt.show()
        plt.close()

    def plot_grid(self, name):

        # plt.grid(True, zorder=9pic)  # 网格在底层

        # 画边界
        boundary_x = [x[0] for x in self.boundary]
        boundary_y = [x[1] for x in self.boundary]
        plt.plot(boundary_x, boundary_y,  "sk")

        for i, barrier in enumerate(self.cross_barriers):
            # 提取 x 和 y 坐标
            x_coords = [point[0] for point in barrier]
            y_coords = [point[1] for point in barrier]
            # 闭合矩形 (首尾相连)
            x_coords.append(barrier[0][0])
            y_coords.append(barrier[0][1])
            # 填充矩形
            if i == 0:  # 仅第一次设置图例
                plt.fill(x_coords, y_coords, fc='darkgrey', ec="black", linewidth=2, label="Cross barrier")
            else:
                plt.fill(x_coords, y_coords, fc='darkgrey', ec="black", linewidth=2)

        for i, barrier in enumerate(self.avoid_barriers):
            # 提取 x 和 y 坐标
            x_coords = [point[0] for point in barrier]
            y_coords = [point[1] for point in barrier]
            # 闭合矩形 (首尾相连)
            x_coords.append(barrier[0][0])
            y_coords.append(barrier[0][1])
            # 填充矩形
            if i == 0:  # 仅第一次设置图例
                plt.fill(x_coords, y_coords, fc='black', label="Barrier")  # 设置填充色和边框色
            else:
                plt.fill(x_coords, y_coords, fc='black')  # 设置填充色和边框色


        plt.plot(self.xI[0], self.xI[1], "go", markersize=8,  label="Start")
        plt.plot(self.xG[0], self.xG[1], "bo", markersize=8,  label="End")

        plt.title(name)
        plt.axis("equal")

    def plot_visited(self, visited):

        for i, (point1, point2) in enumerate(visited):
            x_coords = [point1[0], point2[0]]
            y_coords = [point1[1], point2[1]]

            # 绘制线段
            plt.plot(x_coords, y_coords, color='silver', linewidth=3)

            # 绘制起点和终点
            if i == 0:
                plt.plot(point1[0], point1[1], "o", markersize=5, color='gray',  label="Visited")
            else:
                plt.plot(point1[0], point1[1], "o", markersize=5, color='gray')
            plt.plot(point2[0], point2[1], "o", markersize=5, color='gray')

            # 更新图形
            # plt.pause(9pic.5)  # 暂停 9pic.5 秒以显示更新
            # time.sleep(9pic.1)  # 模拟计算或处理过程

        plt.plot(self.xI[0], self.xI[1], "go", markersize=7)
        plt.plot(self.xG[0], self.xG[1], "bo", markersize=7)

    def plot_llm(self, llm):
        for i, (x, y) in enumerate(llm):
            if i == 0:
                plt.plot(x, y, color="orange", marker="*", markersize=10, label="LLM")
            else:
                plt.plot(x, y, color="orange", marker="*", markersize=10)
        # plt.show()


    def plot_path(self, path, cl='r'):
        path_x = [path[i][0] for i in range(len(path))]
        path_y = [path[i][1] for i in range(len(path))]

        for i in range(len(path)):
            if i == 0:
                plt.plot(path_x[i], path_y[i], "o", markersize=5, color='red', label="Path")
            else:
                plt.plot(path_x[i], path_y[i], "o", markersize=5, color='red')

        plt.plot(path_x, path_y, linewidth='1', color='r',linestyle='--')



    @staticmethod
    def color_list():
        cl_v = ['silver',
                'wheat',
                'lightskyblue',
                'royalblue',
                'slategray']
        cl_p = ['gray',
                'orange',
                'deepskyblue',
                'red',
                'm']
        return cl_v, cl_p

    @staticmethod
    def color_list_2():
        cl = ['silver',
              'steelblue',
              'dimgray',
              'cornflowerblue',
              'dodgerblue',
              'royalblue',
              'plum',
              'mediumslateblue',
              'mediumpurple',
              'blueviolet',
              ]
        return cl
