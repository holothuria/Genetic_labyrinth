

import time
import threading

from ga_main import *
from data_vo import *
from graphic import *



# 30回繰り返す
for i in range(30):
	
	
	# valueObject作成
	vo = data_vo()
	
	# 学習オブジェクト作成
	ga_obj = ga_main(vo)
	
	# 描画オブジェクト作成
	draw_obj = graphic(vo)
	
	
	
	# 終わるまで永遠に繰り返す
	count = 0
	while True:
		
		count += 1
		
		ga_obj.selection()
		time.sleep(0.01)
		if (0 < ga_obj.top_individual.get_fitness()):
			print(count)
			break
		




