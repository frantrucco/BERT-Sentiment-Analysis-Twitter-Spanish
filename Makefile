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

uba:
	@echo "Preprocessing dataset uba to create the prepretrain data."
	python3 $(PREPROCESS)/clean_uba.py $(UBA) $(PREPRETRAIN_DATA)

intertass:
	@echo "Preprocessing dataset Inter-TASS to create the training data."
	python3 $(PREPROCESS)/clean_intertass.py $(INTERTASS) $(TRAIN_DATA)

preprocess: uba intertass

prepretrain:
	@echo "Creating the pretraining data from uba preprocessed dataset."

pretrain:
	@echo "Pretraining using the pretraining data."

train:
	@echo "Fine tuning the model using the Inter-TASS dataset."

cleanuba:
	@echo "Cleaning the preprocessing outputs of uba preprocessing."

cleanintertass:
	@echo "Cleaning the preprocessing outputs of intertass preprocessing."

cleanprepretrain:
	@echo "Cleaning the pretraining data."

cleanpretrain:
	@echo "Cleaning the pretrained model."

cleantrain:
	@echo "Cleaning the finetuned model."

clean: cleanuba cleanintertass cleanprepretrain cleanpretrain	\
       cleanintertass cleantrain

all: uba intertass prepretrain pretrain train

.PHONY: all clean uba intertass preprocess prepretrain pretrain train	\
        cleanuba cleanintertass cleanprepretrain cleanpretrain			\
        cleantrain
