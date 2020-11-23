#!/bin/bash

echo "Begin training!"


# echo "=======================Bert=========================="
# echo "==Bert_spc=="
# python train.py --model_name bert_spc --dataset review --num_epoch 40
# python train.py --model_name bert_spc --dataset review --num_epoch 40 --pretrained_bert_name '/root/TextMining/text_mining/transformers/examples/resources/text_bert'


# echo "==lct_bert=="
# python train.py --model_name lcf_bert --dataset review --num_epoch 40
# python train.py --model_name lcf_bert --dataset review --num_epoch 40 --pretrained_bert_name '/root/TextMining/text_mining/transformers/examples/resources/text_bert'

# echo "==aen=="
# python train.py --model_name aen_bert --dataset review --num_epoch 40
# python train.py --model_name aen_bert --dataset review --num_epoch 40 --pretrained_bert_name '/root/TextMining/text_mining/transformers/examples/resources/text_bert'


echo "=======================NON Bert=========================="
echo "==mgan=="
python train.py --model_name mgan --dataset review2 --num_epoch 200 --embed_type word2vec_gen


echo "==aoa=="
python train.py --model_name aoa --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==tnet=="
python train.py --model_name tnet_lf --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==Cabasc=="
python train.py --model_name cabasc --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==memnet=="
python train.py --model_name memnet --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==ian=="
python train.py --model_name ian --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==atae_lstm=="
python train.py --model_name atae_lstm --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==td-lstm=="
python train.py --model_name td_lstm --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==tc-lstm=="
python train.py --model_name tc_lstm --dataset review2 --num_epoch 200 --embed_type word2vec_gen

echo "==LSTM=="
python train.py --model_name lstm --dataset review2 --num_epoch 200 --embed_type word2vec_gen



echo "finished!"