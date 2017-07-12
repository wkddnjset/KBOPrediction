import os
import sys
import argparse
import json
import tensorflow as tf
import numpy as np

from builder import SeLuModel
from builder import Runner
from constants import *
# from formatter import create_data
from formatter import format


DIRNAME = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='KBO Score Prediction Trainer')

parser.add_argument('file_name', type=str, help='The data file (must be in the same directory')
parser.add_argument('train_size', type=float, help='The proportion of the training set to the test set')
parser.add_argument('model_name', type=str, help='The name of the model')
parser.add_argument('learn_rate', type=float, help='The learning rate')
parser.add_argument('epoch', type=int, help='Training epoch')
parser.add_argument('sequence_length', type=float, help='Sequence length')
parser.add_argument('stack_num', type=float, help='The size of LSTM cell stack')

if __name__ == '__main__':
	args = parser.parse_args()
	"""
	Create data set and divide into test data set & train data set
	"""
	f = open(DIRNAME + "/" + args.file_name, 'r')
	print("Load JSON data")
	data = json.load(f)

	# TODO:// X: previous 'sequence_length' game results of home/away team Y: current game result [home, away]
	trainX, trainY, testX, testY = create_data(data, args.train_size, args.sequence_length) 

	## ======== Build model ======
	with tf.Session() as sess:
		kbo_pred_model = SeLuModel(
			sess, 
			args.model_name, 
			learn_rate=args.learn_rate,
			hidden_size=args.hidden_size,
			sequence_length=args.sequence_length,
			stack_num=args.stack_num
		)
		

		## ======== Train model ======
		print("Started the training...")
		kbo_runner = Runner()
		kbo_runner.train_run(
			kbo_pred_model, 
			trainX, 
			trainY,
			training_epoch=args.epoch
		)

		## ======== Run test =========
		accuracy = kbo_runner.get_accuracy(kbo_pred_model, testX, testY)

		print("Model Average Error: ")
		print(accuracy)

		## ======= Save the trained model ======
		print("Saving the trained model...")
		kbo_pred_model.save()
		print("Save complete.")








