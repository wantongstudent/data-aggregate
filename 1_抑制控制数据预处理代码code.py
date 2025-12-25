import os
# import openpyxl
import csv
import chardet
file_path = "./原文件"
def get_files(path):
    files_ = os.listdir(path)#猴子
    files_.sort()
    print(files_)
    csv_files = []
    for item in files_:
        p = "{}/{}".format(path,item)
        files = os.listdir(p)
        files.sort()
        for file in files:
            csv_files.append("{}/{}/{}".format(path,item,file))
    return csv_files
csv_files = get_files(file_path)
print(csv_files)
def read_csv_file(file):
    print(file)
    with open(file, 'rb') as file_:
        raw_data = file_.read()
        result = chardet.detect(raw_data)
        encoding_ = result['encoding']
    with open(file, 'r', encoding=encoding_) as csvfile:
        reader = csv.reader(csvfile)
        # print(reader)
        # 遍历每一行数据
        infos = [file.split("/")[2]]
        flag = False
        for row in reader:
            # print(row)
            # 处理每一行数据
            if len(row) == 0:
                continue
            if row[0] == "汇总信息" or row[0] == "总结信息":
                flag = True
                continue
            if flag:
                infos.append(row)
    return infos
             
infos = read_csv_file(csv_files[0])
print(infos)
infos_all = []
for file in csv_files:
    infos_all.append(read_csv_file(file))
print(infos_all)
names = []
for infos in infos_all:
    print(infos)
    # print(infos[1])
    name = infos[1][1]
    names.append(name)
names = list(set(names))
names.sort()
print(names)
cols = ["姓名"]
for infos in infos_all:
    print(infos)
    for idx,info in enumerate(infos):
        if idx == 0 or idx == 1 :
            continue
        col = "{}_{}".format(infos[0],info[0])
        if col in cols:
            continue
        cols.append(col)
    
print(len(cols))
print(cols)
#初始化
results_all = {}
for name in names:
    results_all[name] = {}
    for col in cols[1:]:
        results_all[name][col] = "#"
print(results_all)
#填充
for infos in infos_all:
    # print(infos)
    name = infos[1][1]
    for info in infos[2:]:
        key = "{}_{}".format(infos[0],info[0])
        results_all[name][key] = info[1]
print(results_all)
#转换
datas = []
datas.append(cols)
for name in names:
    row = [name]
    for key in results_all[name]:
        row.append(results_all[name][key])
    datas.append(row)
print(datas)
#保存
with open('汇总.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(datas)