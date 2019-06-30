
import random
import copy

class Individual():
	
	fitness = -100
	gene = []
	
		
	def __init__(self):
		pass
	
	
	def set_gene(self, gene):
		self.gene = gene
	
	def get_gene(self):
		return self.gene
	
	def set_fitness(self, fitness):
		self.fitness = fitness
	
	def get_fitness(self):
		return self.fitness
	
	
	
	# ランダムに初期遺伝子を決定するメソッド
	def gene_creater(self, start_position):
		self.gene = [start_position]
		for i in range(random.randint(20,70)):
			self.end_insertion()
	
	
	# 遺伝子の最後に遺伝子を追加するメソッド
	def end_insertion(self):
		# 最後の座標を取得
		add_gene = copy.copy(self.gene[len(self.gene) - 1])
		
		# 取得した座標から、ランダムに上下左右に移動
		direction = random.randint(0,3)
		if direction == 0:
			add_gene[0] = add_gene[0] - 1
			
		elif direction == 1:
			add_gene[0] = add_gene[0] + 1
			
		elif direction == 2:
			add_gene[1] = add_gene[1] - 1
			
		elif direction == 3:
			add_gene[1] = add_gene[1] + 1
			
		# 移動した座標を遺伝子に追加
		self.gene.append(add_gene)
	
	# 遺伝子のどこかを欠損させるメソッド
	def missing(self):
		
		# 欠損位置をランダムに決定
		missing_gene_id = random.randint(1, (len(self.gene) - 1))
		
		# 指定位置の遺伝子を欠損させる
		missing_gene = self.gene.pop(missing_gene_id)
		
		# 差分の取得
		diff_x = self.gene[missing_gene_id - 1][0] - missing_gene[0]
		diff_y = self.gene[missing_gene_id - 1][1] - missing_gene[1]
		
		# 欠損位置より後ろの遺伝子を、差分の量だけずらす
		for i in range(missing_gene_id, len(self.gene)):
			self.gene[i][0] += diff_x
			self.gene[i][1] += diff_y
	
	
	# クローンメソッド
	def clone(self):
		new_individual = Individual()
		
		new_individual.set_fitness(self.fitness)
		new_individual.set_gene(copy.deepcopy(self.gene))
		
		
		return new_individual
	
	
