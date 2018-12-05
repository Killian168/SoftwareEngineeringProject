from __future__ import division
from __future__ import print_function

import sys
import argparse
import cv2
import editdistance
from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess

# Defines all files neccessary and all their relative paths
class FilePaths:
	"filenames and paths to data"
	fnCharList = '../model/charList.txt'
	fnAccuracy = '../model/accuracy.txt'
	fnTrain = '../data/'
	fnInfer = '../data/test.png'
	fnCorpus = '../data/corpus.txt'

# Trains the model on the chosen dataset
def train(model, loader):
	"train NN"
	epoch = 0 # Hold the number of times the NN has been trained
	bestCharErrorRate = float('inf') # Holds the best error rate
	noImprovementSince = 0 # Holds the number of epochs since last improvement
	earlyStopping = 10 # Stop training after this many epochs have been reached with no improvement
	while True:
		epoch += 1
		print('Epoch:', epoch)

		# Actually train the algorithm
		print('Train NN')
		loader.trainSet()

		# Iterates throught the dataset until there is none left
		# Each iteration provides a loss that is backproped throughout the
		# System
		while loader.hasNext():
			iterInfo = loader.getIteratorInfo()
			batch = loader.getNext()
			loss = model.trainBatch(batch)
			print('Batch:', iterInfo[0],'/', iterInfo[1], 'Loss:', loss)

		# Validate the model
		charErrorRate = validate(model, loader)
		
		# If it is the best validation accuracy so far then save the params
		if charErrorRate < bestCharErrorRate:
			print('Character error rate improved, save model')
			bestCharErrorRate = charErrorRate # Set bestCharErrorRate for future comparisions
			noImprovementSince = 0 # Reset to 0
			model.save() # Save the current model
			open(FilePaths.fnAccuracy, 'w').write('Validation character error rate of saved model: %f%%' % (charErrorRate*100.0))
		else:
			print('Character error rate not improved')
			noImprovementSince += 1

		# Stop training If there has been no improvements in teh last 10 epochs
		if noImprovementSince >= earlyStopping:
			print('No more improvement since %d epochs. Training stopped.' % earlyStopping)
			break

# Validates the model after a round of training
def validate(model, loader):
	print('Validate NN')
	loader.validationSet()
	
	# Init all to 0
	numCharErr = 0
	numCharTotal = 0
	numWordOK = 0
	numWordTotal = 0

	# Main loop to validate against truth
	while loader.hasNext():
    	
		# Gets next batch
		iterInfo = loader.getIteratorInfo()
		print('Batch:', iterInfo[0],'/', iterInfo[1])
		batch = loader.getNext()
		recognized = model.inferBatch(batch)
		
		# If the word is recognised or not
		print('Ground truth -> Recognized')	
		for i in range(len(recognized)):
			numWordOK += 1 if batch.gtTexts[i] == recognized[i] else 0
			numWordTotal += 1
			dist = editdistance.eval(recognized[i], batch.gtTexts[i])
			numCharErr += dist
			numCharTotal += len(batch.gtTexts[i])
			print('[OK]' if dist==0 else '[ERR:%d]' % dist,'"' + batch.gtTexts[i] + '"', '->', '"' + recognized[i] + '"')
	
	# print validation result
	charErrorRate = numCharErr / numCharTotal
	wordAccuracy = numWordOK / numWordTotal
	print('Character error rate: %f%%. Word accuracy: %f%%.' % (charErrorRate*100.0, wordAccuracy*100.0))
	return charErrorRate


def infer(model, fnImg):
	"recognize text in image provided by file path"
	img = preprocess(cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE), Model.imgSize)
	batch = Batch(None, [img] * Model.batchSize) # fill all batch elements with same input image
	recognized = model.inferBatch(batch) # recognize text
	print('Recognized:', '"' + recognized[0] + '"') # all batch elements hold same result


# Main function for the program
def main():
	"main function"
	# Command line args for control of the program
	parser = argparse.ArgumentParser()
	# Train the algorithm
	parser.add_argument("--train", help="train the NN", action="store_true")
	# Validate the algorithm as is against the test dataset
	parser.add_argument("--validate", help="validate the NN", action="store_true")
	# Use beamsearch add on for better accuracy
	parser.add_argument("--beamsearch", help="use beam search instead of best path decoding", action="store_true")
	# Use wordbeamsearch for better accuracy on words
	parser.add_argument("--wordbeamsearch", help="use word beam search instead of best path decoding", action="store_true")
	args = parser.parse_args()

	# If either beamsearch or wordbeamsearch set to that decoder
	decoderType = DecoderType.BestPath
	if args.beamsearch:
		decoderType = DecoderType.BeamSearch
	elif args.wordbeamsearch:
		decoderType = DecoderType.WordBeamSearch

	# If args is train or validate on IAM dataset
	if args.train or args.validate:
		# Load training data, create TF model
		loader = DataLoader(FilePaths.fnTrain, Model.batchSize, Model.imgSize, Model.maxTextLen)

		# Save characters of model for inference mode
		open(FilePaths.fnCharList, 'w').write(str().join(loader.charList))
		
		# Save words contained in dataset into file
		open(FilePaths.fnCorpus, 'w').write(str(' ').join(loader.trainWords + loader.validationWords))

		# Execute training or validation
		if args.train:
			model = Model(loader.charList, decoderType)
			train(model, loader)
		elif args.validate:
			model = Model(loader.charList, decoderType, mustRestore=True)
			validate(model, loader)

	# Infer text on test image
	else:
		print(open(FilePaths.fnAccuracy).read())
		model = Model(open(FilePaths.fnCharList).read(), decoderType, mustRestore=True)
		infer(model, FilePaths.fnInfer)


if __name__ == '__main__':
	main()

