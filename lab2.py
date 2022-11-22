
data_set = []  # 初始化
try:
    file = open('data2.txt', 'r')
    for line in file:
        line = line.replace('\n', '')  # 去掉换行符
        info = line.split(',')
        print(info)
        data_set.append(info)
finally:
    file.close()
print("输入Apriori算法的最小支持度：")
min_sup = float(input())
print("输入Apriori算法的最小置信度：")
min_con = float(input())

# 获取下一个频繁项集
def get_next_fre_item_set(data_set, fre_item_set, can_item_len, min_sup_num):
    fre_items = list(fre_item_set.keys())

    next_fre_item_set = {}
    for i in range(len(fre_items) - 1):
        for j in range(i + 1, len(fre_items)):
            tempi = set()
            if isinstance(fre_items[i], str):
                tempi.add(fre_items[i])
            else:
                tempi = set(list(fre_items[i]))

            tempj = set()
            if isinstance(fre_items[j], str):
                tempj.add(fre_items[j])
            else:
                tempj = set(list(fre_items[j]))

            tempi.update(tempj)

            if len(tempi) > can_item_len:
                continue
            if tempi in list(set(item) for item in next_fre_item_set.keys()):
                continue
            for record in data_set:
                if tempi.issubset(set(record)):
                    if tempi in list(set(item) for item in next_fre_item_set.keys()):
                        next_fre_item_set[tuple(tempi)] += 1
                    else:
                        next_fre_item_set[tuple(tempi)] = 1

    for key in list(next_fre_item_set.keys()):
        if next_fre_item_set[key] < min_sup_num:
            del next_fre_item_set[key]

    if len(list(next_fre_item_set.keys())) < 1:
        return None
    else:
        return next_fre_item_set

# 获取频繁项集
def get_fre_item_sets(data_sets, min_sup):
    num_record = len(data_sets)
    min_sup_num = min_sup * num_record
    fre_item_sets = []
    fre_item_sets.append({})

    # 统计每个元素的频次
    for record in data_sets:
        for item in record:
            if item in fre_item_sets[0].keys():
                fre_item_sets[0][item] += 1
            else:
                fre_item_sets[0][item] = 1

    # 删除低于最小支持度的项
    for item in list(fre_item_sets[0].keys()):
        if fre_item_sets[0][item] < min_sup_num:
            del fre_item_sets[0][item]

    can_item_len = 2
    while True:
        if len(fre_item_sets[can_item_len - 2]) < 2:
            break
        else:
            next_fre_item_set = get_next_fre_item_set(data_set, fre_item_sets[can_item_len - 2], can_item_len,
                                                      min_sup_num)
            if next_fre_item_set == None:
                break
            else:
                fre_item_sets.append(next_fre_item_set)
            can_item_len += 1
    return fre_item_sets

# 计算置信度
def calculate_confidence(fre_item_sets, subset, fre_item):
    len_mother = len(subset)
    len_son = len(fre_item)
    mother_key = None
    son_key = None
    if len_mother == 1:
        mother_key = subset[0]
    else:
        mother_keys = list(fre_item_sets[len_mother - 1].keys())
        for i in range(len(mother_keys)):
            if set(subset) == set(mother_keys[i]):
                mother_key = mother_keys[i]
                break
    son_keys = list(fre_item_sets[len_son - 1].keys())
    for i in range(len(son_keys)):
        if set(fre_item) == set(son_keys[i]):
            son_key = son_keys[i]
            break
    return fre_item_sets[len_son - 1][son_key] / fre_item_sets[len_mother - 1][mother_key]

# 获取关联规则
def get_association_rules(fre_item_sets, min_con):
    def subsets(itemset):
        N = len(itemset)
        subsets = []
        for i in range(1, 2 ** N - 1):
            tmp = []
            for j in range(N):
                if (i >> j) % 2 == 1:
                    tmp.append(itemset[j])
            subsets.append(tmp)
        return subsets

    association_rules = []
    for i in range(1, len(fre_item_sets)):
        fre_item_set = fre_item_sets[i]
        for fre_item in list(fre_item_set.keys()):
            tmp = {}
            all_subsets = subsets(fre_item)
            for s1 in range(len(all_subsets) - 1):
                for s2 in range(s1 + 1, len(all_subsets)):
                    subset1 = all_subsets[s1]
                    subset2 = all_subsets[s2]
                    if len(subset1) + len(subset2) == len(fre_item) and len(set(subset1) & set(subset2)) == 0:
                        confidence = calculate_confidence(fre_item_sets, subset1, fre_item)
                        if confidence > min_con:
                            temp = str(subset1) + ' > ' + str(subset2)
                            tmp[temp] = confidence
                        confidence = calculate_confidence(fre_item_sets, subset2, fre_item)
                        if confidence > min_con:
                            temp = str(subset2) + ' > ' + str(subset1)
                            tmp[temp] = confidence
            if tmp.keys():
                association_rules.append(tmp)
    return association_rules

fre_item_sets = get_fre_item_sets(data_set, min_sup)

for i in fre_item_sets:
    print("获取的频繁项集为：\n",i)

association_rules = get_association_rules(fre_item_sets, min_con)

for i in association_rules:
    print("获取的关联规则为:\n",i)
