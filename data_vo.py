

class data_vo():
	
	# スタートとゴールの座標設定
	start_position = [8, 9]
	goal_position = [1, 0]
	
	# 迷路の幅
	maze_width = 10
	maze_height = 10
	
	# 現在の最優秀経路
	top_route = ()
	
	# 迷路生成
	maze = [
	[0,0,1,0,0,0,0,1,0,0],
	[0,0,1,0,1,1,0,1,0,0],
	[0,0,1,0,0,0,0,1,0,0],
	[0,0,0,0,0,1,0,0,0,0],
	[0,0,0,0,0,1,0,0,0,0],
	[1,1,1,0,0,1,1,1,1,0],
	[0,0,1,0,0,1,1,0,0,0],
	[0,0,0,0,0,1,1,1,1,1],
	[0,0,1,1,1,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0]]

	
	def __init__(self):
		pass
	
	def get_start_position(self):
		return self.start_position
	
	def get_goal_position(self):
		return self.goal_position
	
	def set_maze(self, maze):
		self.maze = maze
	
	def get_maze(self):
		return self.maze
	
	def set_top_route(self, top_route):
		self.top_route = top_route
	
	def get_top_route(self):
		return self.top_route
