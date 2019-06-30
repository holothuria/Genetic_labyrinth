
import random
import copy

from data_vo import *
from individual import *


class ga_main():
	
	vo = None
	population = []
	
	# 最優秀個体
	top_individual = None
	
	
	def __init__(self, vo):
		
		# voの設定
		self.vo = vo
		
		# 個体群の生成
		for i in range(100):
			individual = Individual()
			individual.gene_creater(vo.get_start_position())
			self.population.append(individual)
			
			self.fitness_calc(self.population[i])
		
	
	
	# 選出メソッド
	def selection(self):
		
		# 個体群プールの生成
		population_ark = []
		
		# 最優秀個体のセットとリセット
		population_ark.append(self.top_individual)
		self.top_individual = None
		
		# 優秀な個体の選出
		for i in range(len(self.population) - 1):
			individualList = []
			
			# 個体群からランダムに10個体を選択する
			for j in range(10):
				individualList.append(self.population[random.randint(0, len(self.population) - 1)])
				
			population_ark.append(self.tournament(individualList).clone())
		
		next_population = []
		
		# 遺伝子の変異
		for i in range(len(population_ark) // 2):
			
			individual_pair = []
			# 個体プールから順に2個体を選出する(直前に順番含めランダムのため、こちらで再度ランダムにする必要はない)
			for j in range(2):
				individual_pair.append(population_ark.pop(len(population_ark) - 1))
				
			# 個体ペアを交叉及び突然変異させる
			for individual in self.crossover(individual_pair):
				# 突然変異させる
				self.mutation(individual)
				
				# 適応度の再計算
				self.fitness_calc(individual)
				
				# 次世代個体群に追加
				next_population.append(individual)
		
		# 確定した次世代個体群を新たな個体群として設定
		self.population = next_population
		
		
	
	
	# 最優秀を決めるメソッド
	def tournament(self, individualList):
		
		now_top_individual = None
		
		for individual in individualList:
			
			# 現在の最優秀個体と適応度を比較し、上回っていれば入れ替える
			if (now_top_individual is None) or (now_top_individual.get_fitness() < individual.get_fitness()):
				now_top_individual = individual
		return now_top_individual
		
	
	
	# 交叉メソッド
	def crossover(self, individual_pair):
		
		# それぞれを暫定的に雄雌として格納
		gene_male = individual_pair[0].get_gene()
		gene_female = individual_pair[1].get_gene()
		
		# 交叉
		for i in range(5):
			# 雄側の1つ目の交叉起点の確認
			male_cross_pos_1 = random.randint(1, len(gene_male) - 1)
			
			try:
				# 雄側と一致する、雌側の1つ目の交叉起点の確認
				female_cross_pos_1 = gene_female.index(gene_male[male_cross_pos_1])
				
			except ValueError as e:
				# 交叉起点が一致しなかった場合は再検索
				continue
			
			# 2つ目の交差点検索
			for j in range(10):
				
				# 雄側の2つ目の交叉起点の確認
				male_cross_pos_2 = random.randint(1, len(gene_male) - 1)
				
				try:
					# 雄側と一致する、雌側の2つ目の交叉起点の確認
					female_cross_pos_2 = gene_female.index(gene_male[male_cross_pos_2])
					
				except ValueError as e:
					# 交叉起点が一致しなかった場合は再検索
					continue
					
				# 交差点の位置関係が正しいか確認し、位置関係が逆であれば再検索
				if male_cross_pos_1 <= male_cross_pos_2:
					if female_cross_pos_2 <= female_cross_pos_1:
						continue
				if male_cross_pos_2 <= male_cross_pos_1:
					if female_cross_pos_1 <= female_cross_pos_2:
						continue
				
				
				# 1つ目の座標の方が小さくなるように変更
				if male_cross_pos_2 <= male_cross_pos_1:
					tmp = male_cross_pos_2
					male_cross_pos_2 = male_cross_pos_1
					male_cross_pos_1 = tmp
				if female_cross_pos_2 <= female_cross_pos_1:
					tmp = female_cross_pos_2
					female_cross_pos_2 = female_cross_pos_1
					female_cross_pos_1 = tmp
				
					
				# 位置関係が正しければ、交叉を行う
				male_gene_lead = gene_male[:male_cross_pos_1]
				male_gene_middle = gene_male[male_cross_pos_1:male_cross_pos_2]
				male_gene_end = gene_male[male_cross_pos_2:]
				female_gene_lead = gene_female[:female_cross_pos_1]
				female_gene_middle = gene_female[female_cross_pos_1:female_cross_pos_2]
				female_gene_end = gene_female[female_cross_pos_2:]
				
				# 中央部のみ雌雄を入れ替えて格納
				new_male_gene = male_gene_lead + female_gene_middle + male_gene_end
				new_female_gene = female_gene_lead + male_gene_middle + female_gene_end
				
				# 交叉した雌雄を格納
				individual_pair[0].set_gene(new_male_gene)
				individual_pair[1].set_gene(new_female_gene)
				
				# 交叉した個体ペアを返却
				return individual_pair
		
		
		# 交叉せず個体ペアを返却
		return individual_pair

	
	# 突然変異メソッド
	def mutation(self, individual):
		
		# 挿入
		while True:
			if random.randint(0, 99) <= 80:
				break
			individual.end_insertion()
		
		# 欠損
		while True:
			if len(individual.get_gene()) <= random.randint(15, 99):
				break
			individual.missing()
		
	
	
	# 適応度計算メソッド
	def fitness_calc(self, individual):
		
		# 適応度の計算
		now_fitness = -100
		
		maze = self.vo.get_maze()
		goal_pos = self.vo.get_goal_position()
		
		count = 0
		route = []
		try:
			for position in individual.get_gene():
				if position == goal_pos:
					# ゴールできた場合は、「幅 * 高さ - 現在の歩数」が適応度
					now_fitness = 100 - count
					
					# 経路に追加してループを終了
					route.append(copy.copy(position))
					break
				
				try:
					if maze[position[1]][position[0]] == 1:
						# 壁だったらゴールできなかった例外を送出
						raise NonGoalError("in wall")
				except IndexError as e:
					# 範囲外ならゴールできなかった例外を送出
					raise NonGoalError("out index")
					
				if position[1] < 0 or position[0] < 0:
					# 負の値ならゴールできなかった例外を送出
					raise NonGoalError("out of minus")
				
					
				# 経路に現在座標を追加
				route.append(copy.copy(position))
				count += 1
			
			else:
				# どこにも辿り着かなかった場合
				# ゴールできなかった例外を送出
				raise NonGoalError("on the way")
				
		except NonGoalError as nge:
			# ゴールできなかった例外
			# ゴールできなかった場合、「そこからの壁を考慮しない最短経路 * -1」が適応度
			error_before_pos = individual.get_gene()[count - 1]
			now_fitness = -1 * (abs(error_before_pos[0] - goal_pos[0]) + abs(error_before_pos[1] - goal_pos[1]))
			
			# 行き止まり対策の適応度減算
			end_pos = route[len(route) - 1]
			if (end_pos[0] == 0) and (0 < end_pos[1]):
				if maze[end_pos[1] - 1][end_pos[0]] == 1:
					# 左端にいる時、上側が壁なら適応度-3(ゴールが上にある前提)
					now_fitness -= 3
					
			elif (end_pos[0] == 1) and (0 < end_pos[1]):
				if (maze[end_pos[1] - 1][end_pos[0] - 1] == 1) and (maze[end_pos[1] - 1][end_pos[0]] == 1) and (maze[end_pos[1] - 1][end_pos[0] + 1] == 1):
					# 左端から1歩手前にいる時、上側3マスが壁なら適応度-3(ゴールが上にある前提)
					now_fitness -= 3
					
			elif (end_pos[1] == 0) and (0 < end_pos[0]):
				if maze[end_pos[1]][end_pos[0] - 1] == 1:
					# 上端にいる時、左側が壁なら適応度-3(ゴールが左にある前提)
					now_fitness -= 3
					
			elif (end_pos[1] == 1) and (0 < end_pos[0]):
				if (maze[end_pos[1] - 1][end_pos[0] - 1] == 1) and (maze[end_pos[1]][end_pos[0] - 1] == 1) and (maze[end_pos[1] + 1][end_pos[0] - 1] == 1):
					# 左端から1歩手前にいる時、上側3マスが壁なら適応度-3(ゴールが上にある前提)
					now_fitness -= 3
					
			if (end_pos[0] == len(self.vo.get_maze()[0]) - 1) and (end_pos[1] == len(self.vo.get_maze()) - 1):
				# 右下隅は適応度-5 (ゴールが左上にある前提)
					now_fitness -= 5
			elif (end_pos[0] == 9) and (end_pos[1] == 0):
				# 右上隅は適応度-5 (ゴールが左上にある前提)
					now_fitness -= 5
			elif (end_pos[0] == 0) and (end_pos[1] == len(self.vo.get_maze()) - 1):
				# 左下隅は適応度-5 (ゴールが左上にある前提)
					now_fitness -= 5
				
			elif (0 < end_pos[0]) and (0 < end_pos[1]) and (end_pos[0] < len(self.vo.get_maze()[0]) - 1) and (end_pos[1] < len(self.vo.get_maze()) - 1):
				# 最終到達地点が端にない時
				
				# 上下左右の壁判定リスト作成
				wall_cheak_list = []
				wall_cheak_list.append(maze[end_pos[1] - 1][end_pos[0]])
				wall_cheak_list.append(maze[end_pos[1]][end_pos[0] + 1])
				wall_cheak_list.append(maze[end_pos[1]][end_pos[0] - 1])
				wall_cheak_list.append(maze[end_pos[1] + 1][end_pos[0]])
				
				if 3 <= wall_cheak_list.count(1):
					# 上下左右の内3つ以上が壁の場合は適応度 -5。どうあがいても未来はないので重め
					now_fitness -= 5
				elif 2 <= wall_cheak_list.count(1):
					# 上下左右の内2つ以上が壁の場合は適応度 -1。あんまり影響なさそうだけど一応減算
					now_fitness -= 1
					
			if str(nge.args[0]) == "on the way":
				# どこにも辿りつかなった場合。進捗より前適応の方が大事なので、適応度-3
				now_fitness -= 3
				
			
			
		
		# 個体に適応度をセットする
		individual.set_fitness(now_fitness)
		
		# 最優秀個体と適応度を比較し、上回っていれば入れ替える
		if (self.top_individual is None) or (self.top_individual.get_fitness() < now_fitness):
			self.top_individual = individual.clone()
			
			# 最優秀経路の詰め替え
			self.vo.set_top_route(route)
	
	



# ゴールできなかった例外
class NonGoalError(Exception):
	pass

