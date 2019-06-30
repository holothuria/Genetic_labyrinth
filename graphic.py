
import os


from data_vo import *
from ga_main import *

class graphic():
	
	# ValueObject
	vo = None
	
	# 描画用迷宮配列
	draw_maze = None
	
	
	def __init__(self, vo):
		
		# voの設定
		self.vo = vo
	
	
	# 描画メソッド
	def draw(self):
		
		self.draw_maze = copy.deepcopy(self.vo.get_maze())
		
		self.route_make()
		draw_str = self.maze_str_make()
		
		print(draw_str)
		
	
	# 描画文字列の作成メソッド
	def maze_str_make(self):
		
		draw_str = []
		draw_str.append("   ")
		
		count = 0
		for i in self.draw_maze[0]:
			draw_str.append(" " + str(count))
			count += 1
		draw_str.append("\n   ")
		
		count = 0
		for i in self.draw_maze[0]:
			if count != self.vo.get_goal_position()[0]:
				draw_str.append("―")
			else:
				draw_str.append("Ｇ")
			count += 1
		
		draw_str.append("\n")
		
		count = 0
		for maze_line in self.draw_maze:
			draw_str.append(" " + str(count) + "|")
			for maze_chip in maze_line:
				if maze_chip == 1:
					draw_str.append("■")
				elif maze_chip == 2:
					draw_str.append("・")
				elif maze_chip == 3:
					draw_str.append("◎")
				else:
					draw_str.append("　")
			draw_str.append("|\n")
			count += 1
		
		draw_str.append("   ")
		count = 0
		for i in self.draw_maze[0]:
			if count != self.vo.get_start_position()[0]:
				draw_str.append("―")
			else:
				draw_str.append("Ｓ")
			count += 1
			
		os.system("cls")
		return "".join(draw_str)
	
	
	# 描画用迷宮リストに足跡を刻むメソッド
	def route_make(self):
		for i, chip in enumerate(self.vo.get_top_route()):
			if i != (len(self.vo.get_top_route()) - 1):
				self.draw_maze[chip[1]][chip[0]] = 2
			else:
				self.draw_maze[chip[1]][chip[0]] = 3

	