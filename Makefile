UBA = "/home/francolq/tass2018/uba.txt"
INTERTASS = "/home/francolq/tass2019/InterTASS"

PREPRETRAIN_DATA = "./data/prepretrain/uba.txt"
PRETRAIN_DATA = "./data/pretrain/pretraining.tfrecord"
TRAIN_DATA = "./data/train"


BERT_MODEL = "./models/bert"
PRETRAIN_MODEL = "./models/pretrained/pretraining_output"
FINETUNED_MODEL = "./models/finetuned"


TRAINING_STEPS = 10000
SEQ_LENGTH = 64
BATCH_SIZE = 32

PREPROCESS = './scripts/preprocess'
TRAIN = './scripts/train'


.PHONY: uba
uba:
	@echo "Preprocessing dataset uba to create the prepretrain data."
	python3 $(PREPROCESS)/clean_uba.py $(UBA) $(PREPRETRAIN_DATA)


.PHONY: intertass
intertass:
	@echo "Preprocessing dataset Inter-TASS to create the training data."
	python3 $(PREPROCESS)/clean_intertass.py $(INTERTASS) $(TRAIN_DATA)


.PHONY: preprocess
preprocess: uba intertass


.PHONY: prepretrain
prepretrain:
	@echo "Creating the pretraining data from uba preprocessed dataset."


.PHONY: pretrain
pretrain:
	@echo "Pretraining using the pretraining data."


.PHONY: train
train:
	@echo "Fine tuning the model using the Inter-TASS dataset."


.PHONY: cleanuba
cleanuba:
	@echo "Cleaning the preprocessing outputs of uba preprocessing."


.PHONY: cleanintertass
cleanintertass:
	@echo "Cleaning the preprocessing outputs of intertass preprocessing."


.PHONY: cleanpreprocess
cleanpreprocess: cleanuba cleanintertass


.PHONY: cleanprepretrain
cleanprepretrain:
	@echo "Cleaning the pretraining data."


.PHONY: cleanpretrain
cleanpretrain:
	@echo "Cleaning the pretrained model."


.PHONY: cleantrain
cleantrain:
	@echo "Cleaning the finetuned model."


.PHONY: clean
clean: cleanpreprocess cleanprepretrain cleanpretrain cleantrain


.PHONY: all
all: uba intertass prepretrain pretrain train
