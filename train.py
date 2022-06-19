import tensorflow as tf
import numpy as np
import networkx as nx
import random
import pickle
import copy
from collections import deque
import os
import math

os.environ['CUDA_VISIBLE_DEVICES'] = '3'
# Hyper Parameters for DAN
PRE_TRAIN = False
TEST = True
RESTORE = True
GAMMA = 1.0  # discount factor for target Q
INITIAL_EPSILON = 0.5  # starting value of epsilon
FINAL_EPSILON = 0.01  # final value of epsilon
batch_size = None  # size of minibatch
input_steps = None
user_size = 128
user_num = 15000
block_num = 16500
lstm_size = 384
num_layers = 2
TRAIN_BATCH_SIZE = 100  # 训练输入的batch 大小
INFERENCE_BATCH_SIZE = 1  # 推断的时候输入的batch 大小
PRE_EPISODE = 600
NEG_SAMPLES = 9
NEXT_ACTION_NUM = 3
train_set_size = 5000
EPISODE = 100  # Episode limitation
PRE_EPISODE = 300
TRAIN_BATCHES = 300  # Step limitation in an episode
anchor_num = 64
BATCH_SIZE = 100


def train_heuristics_network(self):
    self.time_step += 1
    # Step 1: obtain random minibatch from replay memory
    minibatch = random.sample(self.replay_buffer, BATCH_SIZE)
    state_batch = [data[0] for data in minibatch]
    action_batch = [data[1] for data in minibatch]
    reward_batch = [data[2] for data in minibatch]
    next_state_batch = [data[3] for data in minibatch]

    # Step 2: calculate y
    y_batch = []
    Q_value_batch = self.Q_value.eval(
        feed_dict={self.state_input: next_state_batch})
    for i in range(0, BATCH_SIZE):
        done = minibatch[i][4]
        if done:
            y_batch.append(reward_batch[i])
        else:
            y_batch.append(reward_batch[i] + GAMMA * np.max(Q_value_batch[i]))

            self.optimizer.run(feed_dict={
                self.y_input: y_batch,
                self.action_input: action_batch,
                self.state_input: state_batch
            })

def main():
    train_heuristics_network()


#    train_st_network(AstarRNN, 50)
#     Time_diff_attn(AstarRNN)
if __name__ == '__main__':
    main()

