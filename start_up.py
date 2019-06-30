

import time
import threading

from ga_main import *
from data_vo import *
from graphic import *

# valueObject作成
vo = data_vo()

# 学習オブジェクト作成
ga_obj = ga_main(vo)

# 描画オブジェクト作成
draw_obj = graphic(vo)


while True:
	
	# 描画
	draw_obj.draw()
	print(vo.get_top_route())
	print(ga_obj.top_individual.get_fitness())
	print(ga_obj.top_individual.get_gene())
	
	# 15世代繰り返す
	for i in range(15):
		
		ga_obj.selection()
		time.sleep(0.2)




