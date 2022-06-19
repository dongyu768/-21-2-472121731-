from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt

''' embedding path with word2vec'''
def embedPath(pathName, window, embed_size, min_count=0, save2File=True):
    paths = []
    with open('../data/data_D/20161101_0', 'r') as f:
        for line in f.readlines():
            roads = list(line.strip().split(' '))
            paths.append(roads)
    embed_vec = Word2Vec(paths, window=window, min_count=min_count, vector_size=embed_size)
    if save2File:
        embed_vec.wv.save_word2vec_format("../data/embed.txt")
    return embed_vec

''' get embed.txt'''
def getEmbed(filePath):
    word2vec_dic = {}
    index2word = {}
    count = 0
    with open(filePath) as f:
        for line in f:
            values = line.split()
            word = values[0]
            word_vec = np.array(values[1:], dtype='float 32')
            word2vec_dic[word] = word_vec
            index2word[count] = word
            count = count+1
    return word2vec_dic, index2word

''' visualization of path length distribute'''
def visLenDistr(pathfile):
    lenSta = {} # {pathlen : times}
    with open(pathfile, 'r') as f:
        for line in f:
            path = line.split()
            pathlen = len(path)
            if pathlen not in lenSta.keys():
                lenSta[pathlen] = 1
            else:
                lenSta[pathlen] += 1
    sortedDic = {}
    for i in sorted(lenSta):
        sortedDic[i] = lenSta[i]
    x = sortedDic.keys()
    y = sortedDic.values()
    fig, ax = plt.subplots()
    ax.plot(x, y)
    # ax.scatter(x, y)
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 14,
             }
    ax.set_xlabel('Len', font1)
    ax.set_ylabel('Freq', font1)
    plt.show()

def main():
    # embedPath('../data/data_D/20161101', 3, 128)
    visLenDistr('../data/data_D/20161101')

if __name__ == '__main__':
    main()