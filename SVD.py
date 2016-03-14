#!/usr/bin/python
#-*- coding: UTF-8 -*-

import math
import random
import cPickle as pickle
import collections

iter_number = 10 
def ReadFile(fileName):
	'''open file'''
	fi = open(fileName, 'r')
	txt = fi.readlines()
	fi.close()
	return txt

#calculate the overall average
def Average(fileName):
	#fi = open(fileName, 'r')
	result = 0.0
	cnt = 0
	for line in fileName:
		cnt += 1
		arr = line.split()
		#result += int(arr[2].strip())
		result += float(arr[2].strip())
	#print cnt
	return result / cnt
	#return result / N

def InerProduct(v1, v2):
	result = 0.0
	for i in range(len(v1)):
		result += v1[i] * v2[i]
		
	return result

#****************need to chage score span***************
def PredictScore(av, bu, bi, pu, qi):
#    R(user, movie) = avg + b(user) + b(movie) + P(user) * Q(movie)
#  avg：全局平均分
#  b(user)：用户user的偏离程度(bias)
#  b(movie)：电影movie的偏离程度(bias) 对应歌曲
#  P(user)：用户user的因子爱好程度
#  Q(movie)：电影movie的因子程度 对应歌曲
	pScore = av + bu + bi + InerProduct(pu, qi)
	#if pScore <  0.121667:
	#	pScore =  0.121667
	#elif pScore > 1.547411:
	#	pScore = 1.547411
		
	return pScore

step_record = open('model/step_record','w')
def SVD(configureFile, testDataFile, trainDataFile, modelSaveFile):
	#get the configure
	fi = open(configureFile, 'r')
	line = fi.readline()
	arr = line.split()
	averageScore = float(arr[0].strip())
	userNum = int(arr[1].strip())
	itemNum = int(arr[2].strip())
	factorNum = int(arr[3].strip())
	learnRate = float(arr[4].strip())
	regularization = float(arr[5].strip())
	fi.close()
	
	bi = [0.0 for i in range(itemNum)]
	bu = [0.0 for i in range(userNum)]
	temp = math.sqrt(factorNum)
	qi = [[(0.1 * random.random() / temp) for j in range(factorNum)] for i in range(itemNum)]	
	pu = [[(0.1 * random.random() / temp)  for j in range(factorNum)] for i in range(userNum)]
	print("initialization end\nstart training\n")
	
	#train model
	preRmse = 1000000.0
	for step in range(iter_number):
		#fi = open(trainDataFile, 'r')
		print step
		count = 0
		step_record.write('loop '+str(step)+'\n')
		for line in trainDataFile:
			count = count + 1
			if count % 10000 == 0:
				print count
			arr = line.split()
			uid = int(arr[0].strip())
			iid = int(arr[1].strip())
			#print uid
			#score = int(arr[2].strip())			
			score = float(arr[2].strip())			
			prediction = PredictScore(averageScore, bu[uid], bi[iid], pu[uid], qi[iid])
				
			eui = score - prediction
			if step == iter_number:
				step_record.write(str(score)+'\t'+str(prediction)+'\n')
			#update parameters
			#bu[uid] += learnRate * (eui - regularization * bu[uid])
			#bi[iid] += learnRate * (eui - regularization * bi[iid])	
			for k in range(factorNum):
				temp = pu[uid][k]	#attention here, must save the value of pu before updating
				pu[uid][k] += learnRate * (eui * qi[iid][k] - regularization * pu[uid][k])
				qi[iid][k] += learnRate * (eui * temp - regularization * qi[iid][k])
		#fi.close()
		#learnRate *= 0.9
		#curRmse = Validate(testDataFile, averageScore, bu, bi, pu, qi)
		#print("test_RMSE in step %d: %f" %(step, curRmse))
		#if curRmse >= preRmse:
		#	break
		#else:
		#	preRmse = curRmse
    
	#write the model to files
	fo = file(modelSaveFile, 'wb')
	pickle.dump(bu, fo, True)
	pickle.dump(bi, fo, True)
	pickle.dump(qi, fo, True)
	pickle.dump(pu, fo, True)
	fo.close()
	print("model generation over")
	
#validate the model
def Validate(testDataFile, av, bu, bi, pu, qi):
	cnt = 0
	rmse = 0.0
	#fi = open(testDataFile, 'r')		
	for line in testDataFile:
		cnt += 1
		arr = line.split()
		uid = int(arr[0].strip())
		iid = int(arr[1].strip())
		pScore = PredictScore(av, bu[uid], bi[iid], pu[uid], qi[iid])
			
		#tScore = int(arr[2].strip())
		tScore = float(arr[2].strip())
		rmse += (tScore - pScore) * (tScore - pScore)
	#fi.close()
	return math.sqrt(rmse / cnt)

record = open('model/uid_record','w')
#use the model to make predict
def Predict(configureFile, modelSaveFile, testDataFile, resultSaveFile, resFile):
	#get parameter
	fi = open(configureFile, 'r')
	line = fi.readline()
	arr = line.split()
	averageScore = float(arr[0].strip())
	userNum = int(arr[1].strip())
	itemNum = int(arr[2].strip())
	fi.close()

	#get model
	fi = file(modelSaveFile, 'rb')
	bu = pickle.load(fi)
	bi = pickle.load(fi)
	qi = pickle.load(fi)
	pu = pickle.load(fi)
	fi.close()
	#out total score
	fp = open(resFile,'w')

	for uid in range(userNum):
		record.write(str(uid)+'\n')
		#print uid
		dict_score = {}
		for iid in range(itemNum):
			rui = PredictScore(averageScore, bu[uid], bi[iid], pu[uid], qi[iid])
			dict_score[iid] = rui
			#print iid,rui

		sort_score = collections.OrderedDict(sorted(dict_score.items(), key=lambda t:t[1], reverse=True))
        
		#key_list = sort_score.keys()
		#print key_list[0]
		word = []
		word.append(str(uid))
		film_num = 0
		for iid in sort_score:
			film_num += 1
			if film_num > 20:#recommend 20 tags
			    break
			s = sort_score[iid]
			word.append(str(iid))
			word.append(str(s))
		stri = '\t'.join(word)
		if stri:
		    fp.write(stri+'\n')
	print "total score finished !"


	#predict
	#fi = open(testDataFile, 'r')
	fo = open(resultSaveFile, 'w')
	for line in testDataFile:
		arr = line.split()
		uid = int(arr[0].strip())
		iid = int(arr[1].strip())
		pScore = PredictScore(averageScore, bu[uid], bi[iid], pu[uid], qi[iid])
		fo.write("%f\n" %pScore)
	#fi.close()
	fo.close()
	print("predict over")
			

if __name__ == '__main__':
	configureFile = 'conf/svd.conf'
	#configureFile = 'svd_conf'
	#trainDataFile = 'training.txt'
	trainDataFile = ReadFile('trainData/svd_train') #训练数据集
	validateDataFile = ReadFile('trainData/svd_validate') #验证数据集
	#testDataFile = 'test.txt'
	testDataFile = ReadFile('testData/svd_test') #测试数据集，即要实现的预测数据集
	modelSaveFile = 'model/svd_model.pkl'
	resultSaveFile = 'predict/svd_prediction'
	resFile = 'predict/svd_input_prediction'
	#print("%f" %Average(trainDataFile))
	SVD(configureFile, validateDataFile, trainDataFile, modelSaveFile)
	Predict(configureFile, modelSaveFile, testDataFile, resultSaveFile, resFile)
	
