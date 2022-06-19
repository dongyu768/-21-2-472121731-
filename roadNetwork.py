import pandas as pd
import json

''' reduce data twice'''
def reduceData(filePath, outputFile):
    data = pd.read_csv(filePath, header=None, index_col=False)
    data.columns = ['Vid', 'Oid', 'TimeStamp', 'Lng', 'Lat']
    data = data[data.index % 2 == 0]
    print("the length of data:", len(data))
    data.to_csv(outputFile, index=False, header=False)

'''path_20161101'''
def getPath(filePath, outputFile):
    data = pd.read_csv(filePath, header=None, index_col=False)
    data.columns = ['Vid', 'Oid', 'TimeStamp', 'Lng', 'Lat']
    # Vehicles = {}
    Orders = {}
    for line in data.itertuples():
        path = [line.TimeStamp, [line.Lng, line.Lat]]
        if line.Oid not in Orders.keys():
            Orders[line.Oid] = []
        Orders[line.Oid].append(path)
    print('write path...')
    with open(outputFile, 'w') as file_obj:
        json.dump(Orders, file_obj)

'''get mapmatching format'''
def mapMatching(pathName, outputName):
    # barefoot
    '''
    required formats
    [
    	{"id":"x001","time":1410324847000,"point":"POINT (11.564388282625075 48.16350662940509)"},
    	...
    ]
    '''
    with open(pathName, 'r') as f:
        path_dic = json.load(f)
        path_jsons = []
        print(len(path_dic.values()))
        for order in path_dic.values():
            path_json = []
            for j in range(len(order)):
                path = {}
                # print(order[j])
                path["id"] = "x001"
                path["time"] = int(str(order[j][0]) + '000')
                path["point"] = "POINT (" + str(order[j][1][0]) + " " + str(
                    order[j][1][1]) + ")"
                # print(path)
                path_json.append(path)
                # print(path_json)
            # break
            path_jsons.append(path_json)
        print('the number of order:', len(path_jsons))
        with open(outputName, 'w') as f:
            json.dump(path_jsons, f)

def getPathFile(fileName, saveName):
    pathfile = open(saveName, 'w')
    with open(fileName, 'r') as f:
        for line in f.readlines():
            path = ''
            if line == 'SUCCESS\n': continue
            line = eval(line)
            testSame = []
            for i in range(len(line)):
                if line[i]['road'] in testSame: continue
                testSame.append(line[i]['road'])
                path = path + str(line[i]['road']) + ' '
            if len(testSame) == 1: continue
            pathfile.write(path)
            pathfile.write('\n')

def getSegments():
    import osm2gmns as og
    net = og.getNetFromPBFFile(
        'E:/Program Files/osmosis-0.48.3/bin/chengdu.osm.pbf')
    og.outputNetToCSV(net, output_folder='output')

def main():
    ''''''
    '''reudce data'''
    # according the test, it is best match when reducation times equal 4
    # reduceData('../data/data_S/gps_20161101_S', '../data/data_S/gps_20161101_S_1') # 16077759  1.6GB
    # reduceData('../data/data_S/gps_20161101_S_1', '../data/data_S/gps_20161101_S_2') # 8038880 787MB
    # reduceData('../data/data_S/gps_20161101_S_2', '../data/data_S/gps_20161101_S_3')
    # reduceData('../data/data_S/gps_20161101_S_3', '../data/data_S/gps_20161101_S_4')

    '''get Path'''
    # getPath('../data/data_S/gps_20161101_S_2', '../data/data_D/path_20161101')
    # getPath('../data/data_S/gps_20161101_S_3', '../data/data_D/path_20161101_3')
    # getPath('../data/data_S/gps_20161101_S_4', '../data/data_D/path_20161101_4')
    '''mapMatching'''
    # mapMatching('../data/data_D/path_20161101', '../data/data_D/path_20161101_M')
    # mapMatching('../data/data_D/path_20161101_3','../data/data_D/path_20161101_M_onlyone_3')
    # mapMatching('../data/data_D/path_20161101_4', '../data/data_D/path_20161101_M_onlyone_4')
    # mapMatching('../data/data_D/path_20161101_4', '../data/data_D/path_20161101_M_4')
    '''read path_20161101_M_4'''
    # with open('../data/data_D/path_20161101_M_4', 'r') as f:
    #     matchlist = json.load(f)
    #     print(json.dumps(matchlist[1]))
    '''get paths'''
    getPathFile('../data/data_D/path_20161101_MD_4.log', '../data/data_D/20161101')
if __name__ == '__main__':
    main()