# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/08 8:19
@Author  : ArithmeticJia
@Site    :
@File    : blog_recommend.py
@Software: PyCharm
'''
from math import sqrt
from colorama import Fore
import numpy as np

"""
建立影评评分字典
六种电影类型：a,b,c,d,e,f
七个用户：Cathy,Sophie,Susie,Antonio,Marco,Jack,Leo
"""
critics = {'Cathy': {'a': 2.5, 'b': 3.5, 'c': 3, 'd': 3.5, 'e': 2.5, 'f': 3},
           'Sophie': {'a': 3, 'b': 3.5, 'c': 1.5, 'd': 5, 'e': 1.5, 'f': 3},
           'Susie': {'a': 2.5, 'b': 3, 'd': 3.5, 'f': 4},
           'Antonio': {'b': 3.5, 'c': 3, 'd': 4, 'e': 2.5, 'f': 4.5},
           'Marco': {'a': 3, 'b': 4, 'c': 2, 'd': 3, 'e': 2, 'f': 3},
           'Jack': {'a': 3, 'b': 4, 'd': 5, 'e': 3.5, 'f': 3},
           'Leo': {'b': 4.5, 'd': 4, 'e': 1.0}}


def sim_distance(prefs, person1, person2):
    """
    计算相似度（欧氏距离）
    :param prefs:
    :param person1:
    :param person2:
    :return: person1和person2的基于距离的相似度
    """
    si = {item: 1 for item in prefs[person1] if item in prefs[person2]}
    if len(si) == 0: return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in si])
    # sum_of_squares= sum([pow(prefs[person1][item]-prefs[person2][item],2)
    #                      for item in prefs[person1] if item in prefs[person2]])
    # print(sum_of_squares)
    return 1 / (1 + sqrt(sum_of_squares))


sim_dis = sim_distance(critics, 'Cathy', 'Antonio')  # 基于欧氏距离的相似度
print(Fore.RED, "欧氏距离：", sim_dis, Fore.RESET)


def sim_pearson(prefs, person1, person2):
    """
    计算person1和person2的皮尔逊相关系数
    :param prefs: 数据源
    :param person1:
    :param person2:
    :return: 两person的Pearson相关系数
    """
    si = {item: 1 for item in prefs[person1] if item in prefs[person2]}
    # for item in prefs[person1]:
    #     if item in prefs[person2]: si[item] = 1
    n = len(si)
    if n == 0: return 1
    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])

    sum1Sq = sum([pow(prefs[person1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[person2][it], 2) for it in si])

    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    num = pSum - (sum1 * sum2 / n)  # 协方差cov
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))  # 标准差std

    # print(sum1, sum2, sum1Sq, sum2Sq, pSum)
    if den == 0: return 0
    # print(num, den)
    return num / den


sim_pear = sim_pearson(critics, 'Cathy', 'Sophie')
print(Fore.RED, "皮尔逊相关度：", sim_pear, Fore.RESET)


def test():
    """
    测试皮尔逊相关度
    :return:
    """
    person_1 = [2.5, 3.5, 3, 3.5, 2.5, 3]
    person_2 = [3, 3.5, 1.5, 5, 1.5, 3]
    sum1 = sum(person_1)
    sum2 = sum(person_2)
    # 协方差
    cov = sum([(person_1[i] - sum1 / len(person_1)) * (person_2[i] - sum1 / len(person_2)) for i in
               range(0, len(person_1))]) / (len(person_1) - 1)
    print("cov:", cov)
    # std1 = sum([pow(i - sum1 / len(person_1), 2) for i in person_1])/len(person_1)
    # print(sqrt(std1),np.std(person_1))
    # std2 = sum([pow(i - sum2 / len(person_2), 2) for i in person_2])/len(person_2)
    # print(sqrt(std2), np.std(person_2), sqrt(((np.array(person_2) - np.mean(np.array(person_2)))**2).sum()/(len(person_2))))
    # # 标准差
    # std = sqrt(std1 * std2)
    # print(std,np.std(person_1)*np.std(person_2))
    # pearson =  cov/std
    # print(pearson)
    std = np.std(person_1, ddof=1) * np.std(person_2, ddof=1)
    print(std)
    pearson = cov / std
    print(pearson)


# test()


def topmatches(prefs, person, n, similarity=sim_pearson) -> list:
    scores = [(similarity(prefs, person, other), other) for other in prefs if person != other]
    scores.sort()
    scores.reverse()
    return scores[:n]


topList_pear = topmatches(critics, 'Susie', 5)

print(topList_pear)
