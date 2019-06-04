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
	python $(TRAIN)/create_pretraining_data.py \
    --input_file=$(UBA_CLEANED) \
    --output_file=$(PRETRAIN_DATA) \
    --vocab_file=$(BERT_MODEL)/vocab.txt \
    --do_lower_case=False \
    --max_seq_length=$(SEQ_LENGTH) \
    --max_predictions_per_seq=20 \
    --masked_lm_prob=0.15 \
    --random_seed=12345 \
    --dupe_factor=5 \
    2>&1 | tee ./log/prepretrain


.PHONY: pretrain
pretrain:
	@echo "Pretraining using the pretraining data."
	python $(TRAIN)/run_pretraining.py \
    --input_file=$PRETRAIN_DATA \
    --output_dir=$PRETRAIN_MODEL \
    --do_train=True \
    --do_eval=True \
    --bert_config_file=$BERT_MODEL/bert_config.json \
    --init_checkpoint=$BERT_MODEL/bert_model.ckpt \
    --train_batch_size=$BATCH_SIZE \
    --max_seq_length=$SEQ_LENGTH \
    --max_predictions_per_seq=20 \
    --num_train_steps=$TRAINING_STEPS \
    --num_warmup_steps=10 \
    --learning_rate=2e-5 \
    2>&1 | tee ./log/pretrain


.PHONY: train
train:
	@echo "Fine tuning the model using the Inter-TASS dataset."
	python $(TRAIN)/run_classifier.py \
    --task_name=TASS \
    --do_train=true \
    --do_eval=true \
    --data_dir=$TRAIN_DATA \
    --vocab_file=$BERT_MODEL/vocab.txt \
    --bert_config_file=$BERT_MODEL/bert_config.json \
    --init_checkpoint=$PRETRAIN_MODEL/model.ckpt-$TRAINING_STEPS \
    --max_seq_length=$SEQ_LENGTH \
    --train_batch_size=$BATCH_SIZE \
    --learning_rate=2e-5 \
    --num_train_epochs=2.0 \
    --output_dir=$FINETUNED_MODEL \
    2>&1 | tee ./log/train


.PHONY: cleanuba
cleanuba:
	@echo "Cleaning the preprocessing outputs of uba preprocessing."
	rm $(PREPRETRAIN_DATA)


.PHONY: cleanintertass
cleanintertass:
	@echo "Cleaning the preprocessing outputs of intertass preprocessing."
	rm -fr $(TRAIN_DATA)/*


.PHONY: cleanpreprocess
cleanpreprocess: cleanuba cleanintertass


.PHONY: cleanprepretrain
cleanprepretrain:
	@echo "Cleaning the pretraining data."
	rm $(PRETRAIN_DATA)


.PHONY: cleanpretrain
cleanpretrain:
	@echo "Cleaning the pretrained model."
	rm -fr $(PRETRAIN_MODEL)


.PHONY: cleantrain
cleantrain:
	@echo "Cleaning the finetuned model."
	rm $(FINETUNED_MODEL)/*

.PHONY: help
help:
	@echo "To run all the commands in order:"
	@echo "    make preprocess  # Or make intertass uba"
	@echo "    make prepretrain "
	@echo "    make pretrain"
	@echo "    make train"
	@echo ""
	@echo "Equivalently:"
	@echo "    make all"
	@echo ""
	@echo "To clean just type clean followed by the command to clean:"
	@echo "    make cleanpreprocess"
	@echo ""
	@echo "To clean all:"
	@echo "    make clean"
	@echo ""
	@echo "The dependency graph is as follows:"
	@echo ""
	@echo "    RAW INTERTASS ------------------[intertass]------> CLEANED INTERTASS"
	@echo ""
	@echo "    RAW UBA ------------------------[uba]------------> CLEANED UBA"
	@echo ""
	@echo "    CLEANED UBA --------------------[prepretrain]----> PRETRAIN_DATA"
	@echo ""
	@echo "    PRETRAIN_DATA + BERT_MODEL -----[pretrain]-------> PRETRAIN_MODEL"
	@echo ""
	@echo "    PRETRAIN_MODEL + TRAIN_DATA ----[train]----------> FINETUNED_MODEL"


.PHONY: clean
clean: cleanpreprocess cleanprepretrain cleanpretrain cleantrain


.PHONY: all
all: uba intertass prepretrain pretrain train
