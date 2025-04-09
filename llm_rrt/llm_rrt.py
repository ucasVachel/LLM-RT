import json
import math
import heapq
import os
from shapely.geometry import Point, LineString, Polygon
import random
import time

from env import env, plotting
from model import ChatGPT, Llama3, Deepseek
from utils import list_parse
from pather.llm_rrt.prompt import *

class LLMRRT:
    """RRT algorithm with LLM for initializing start and goal."""

    GPT_METHOD = "PARSE"
    GPT_LLMASTAR_METHOD = "LLM-RRT"

    def __init__(self, llm='gpt', prompt='standard'):
        self.llm = llm
        if self.llm == 'gpt':
            self.model = ChatGPT(method=self.GPT_LLMASTAR_METHOD)
        elif self.llm == 'llama':
            self.model = Llama3()
        elif self.llm == 'deepseek':
            self.model == Deepseek()
        else:
            raise ValueError("Invalid LLM model. Choose 'gpt' or 'llama'.")

        assert prompt in ['standard', 'cot', 'repe'], "Invalid prompt type. Choose 'standard', 'cot', or 'repe'."
        self.prompt = prompt
        self.random_flag = False


    def _initialize_parameters(self, query):
        """Initialize environment parameters from input data."""
        self.step_size = 6  # 每次扩展的步长
        self.max_iterations = 100  # 最大迭代次数
        self.tree = {}  # 用字典存储树 {current_node: parent_node}
        self.visited = []

        self.s_start = (query['start_goal'][0][0], query['start_goal'][0][1])
        self.s_goal = (query['start_goal'][1][0], query['start_goal'][1][1])

        self.cross_barriers = query['cross_barriers']  # 可穿越的障碍
        self.avoid_barriers = query['avoid_barriers']  # 不可穿越的障碍
        self.range_x = query['range_x']
        self.range_y = query['range_y']

        self.Env = env.Env(self.range_x[1], self.range_y[1], self.cross_barriers, self.avoid_barriers)  # 环境类
        self.plot = plotting.Plotting(self.s_start, self.s_goal, self.Env)

        self.tree[self.s_start] = None  # 初始化树，起点没有父节点

    def _initialize_llm_paths(self):
        """Initialize paths using LLM suggestions."""
        start, goal = list(self.s_start), list(self.s_goal)
        query = self._generate_llm_query(start, goal)

        if self.llm == 'gpt':
            response = self.model.ask(prompt=query, max_tokens=100)
            print("response:", response)
        elif self.llm == 'llama':
            response = self.model.ask(prompt=query)
            print("response:", response)
        elif self.llm == 'Kimi':
            response = self.model.ask(prompt=query)
            print("response:", response)
        elif self.llm == 'DeepSeek':
            response = self.model.ask(prompt=query)
            print("response:", response)
        else:
            raise ValueError("Invalid LLM model.")

        nodes = list_parse(response)
        self.target_list = self._filter_valid_nodes(nodes)

        if not self.target_list or self.target_list[0] != self.s_start:
            self.target_list.insert(0, self.s_start)
        if not self.target_list or self.target_list[-1] != self.s_goal:
            self.target_list.append(self.s_goal)
        # print(self.target_list)
        self.i = 1
        self.s_target = self.target_list[1]
        print(self.target_list[0], self.s_target)

    def _generate_llm_query(self, start, goal):
        """Generate the query for the LLM."""
        if self.llm == 'gpt':
            return gpt_prompt[self.prompt].format(start=start, goal=goal, barriers=self.avoid_barriers)
        elif self.llm == 'llama':
            return llama_prompt[self.prompt].format(start=start, goal=goal,
                                                  barriers=self.avoid_barriers)

    def _filter_valid_nodes(self, nodes):
        """Filter out invalid nodes based on environment constraints."""
        return [(node[0], node[1]) for node in nodes
                if self.range_x[0] + 1 < node[0] < self.range_x[1] - 1
                and self.range_y[0] + 1 < node[1] < self.range_y[1] - 1]

    def searching(self, query, filedir, filepath='temp.png', name='rrt'):
        """
        A* searching algorithm.
        :return: Path and search metrics.
        """
        self.filepath = filepath
        self.name = name

        if not os.path.exists(filedir):
            os.makedirs(filedir)

        self._initialize_parameters(query)

        # self.i = 1
        # self.target_list = [(2, 26), (9, 19), (19, 13), (31, 13), (31, 10), (39, 10), (39, 6), (24, 6), (25, 2), (47, 2)]
        # self.s_target = self.target_list[1]
        self._initialize_llm_paths()

        # 查看llm输出点关键点
        # self.plot.llmPoint(self.target_list[1:-1])
        # time.sleep(3)
        # return 9pic
        # #

        for _ in range(self.max_iterations):
            if self.random_flag:
                sample = self.sample_point()  # 随机采样点
                # self.random_flag = False
            else:
                sample = self.s_target  # 跟已有点

            nearest = self.nearest_node(sample)  # 树中距离采样点最近的节点

            if self._euclidean_distance(nearest, sample) <= self.step_size:
                new_node = sample
            else:
                new_node = self.steer(nearest, sample)  # 扩展新的节点

            # 记录
            self.visited.append((nearest, new_node))

            if not self.is_out_of_bounds(new_node) and not self.is_collision(nearest, new_node):  # 如果扩展路径无碰撞
                self.tree[new_node] = nearest  # 加入树

                # 到达终点
                if self._euclidean_distance(new_node, self.s_goal) <= self.step_size:
                    self.tree[self.s_goal] = new_node  # 将目标点连接到树
                    self.visited.append((new_node, self.s_goal))
                    break

                # 到达了阶段点还没到终点
                if self._euclidean_distance(new_node, self.s_target) <= self.step_size and self._euclidean_distance(new_node, self.s_goal) > self.step_size:
                    if self.s_target != new_node:
                        self.tree[self.s_target] = new_node
                        self.visited.append((new_node, self.s_target))
                    # new_node = self.s_target
                    self._update_target()

            else:
                self.random_flag = True
                print(self.s_target)

        path = self.extract_path()

        result = {
            "operation": len(self.visited),
            "length": sum(self._euclidean_distance(path[i], path[i + 1]) for i in range(len(path) - 1)),
            "llm_output": self.target_list,
            "path":path
        }
        self.plot.plot_llm(self.target_list[1:-1])
        self.plot.animation(path, self.visited, True, self.name, self.filepath)
        return result

    def nearest_node(self, sample):
        """找到树中距离采样点最近的节点"""
        return min(self.tree.keys(), key=lambda node: self._euclidean_distance(node, sample))

    def steer(self, nearest, sample):
        """在最近节点和采样点之间扩展"""
        direction = math.atan2(sample[1] - nearest[1], sample[0] - nearest[0])
        new_x = round(nearest[0] + self.step_size * math.cos(direction))
        new_y = round(nearest[1] + self.step_size * math.sin(direction))
        return (new_x, new_y)

    def is_out_of_bounds(self, node):
        x, y = node
        return not (self.range_x[0] <= x <= self.range_x[1] and self.range_y[0] <= y <= self.range_y[1])

    def is_collision(self, start, end):
        """检查线段是否与障碍物碰撞"""
        line = LineString([start, end])

        # 检查 avoid_barriers (不可穿越障碍)
        for obs in self.avoid_barriers:
            barrier = Polygon(obs)
            if line.intersects(barrier):
                return True

        # 检查 end 是否落在 cross_barriers 上
        for obs in self.cross_barriers:
            if Point(end).intersects(Polygon(obs)):
                return True

        return False

    def sample_point(self):
        """随机采样一个点"""
        x = random.uniform(self.range_x[0], self.range_x[1])
        y = random.uniform(self.range_y[0], self.range_y[1])
        return (x, y)

    def extract_path(self):
        """根据树提取路径"""
        path = [self.s_goal]
        current = self.s_goal

        while current != self.s_start:
            if current in self.tree:
                current = self.tree[current]
                path.append(current)
            else:
                break
                print("没到终点")


        path.reverse()
        return path

    @staticmethod
    def _euclidean_distance(p1, p2):
        """计算两点之间的欧几里得距离"""
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def _update_target(self):
        """Update the current target in the path."""
        self.i += 1
        if self.i < len(self.target_list):
            self.s_target = self.target_list[self.i]