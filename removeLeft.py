import re

name_source = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
op = ['(', ')', '{', '}', '[', ']', '/', '\\', '*', '+', '!', '-', '%', '>', '<', '=']


class Infinite:
    def __init__(self, name):
        self.name = name
        self.equalList = []
        self.FIRST = {}
        self.FOLLOW = set()

    def equalList_change(self, express):
        expresses = express.split('|')
        for express in expresses:
            self.equalList.append(express)

        # 将输入文法转换为LL（1）文法


def expressGet(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        express = f.read()
        regex = "[A-Z]->[a-zA-Z|*+-/(){}ε]+"
        res = re.findall(regex, express)
        if len(res) == len(express.split('\n')):
            return res  # 说明输入的文法合法，否则说明输入的文法中有不匹配项
        else:
            return None


def init(expresses):
    infinite = {}
    name_get = list(name_source)
    for express in expresses:
        name = express[0]
        equal = express[3:]
        if name not in infinite.keys():
            inf = Infinite(name)
            infinite[name] = inf
            name_get.remove(name)
        else:
            inf = infinite[name]
        inf.equalList_change(equal)
    print("输入的文法：")
    for name in infinite.keys():
        print(name, end="->")
        s = '|'.join(infinite[name].equalList)
        print(s)
    return infinite, name_get


def leftGet(infinite, name_get):
    name_list = list(infinite.keys())
    for name in name_list:
        first_set = set()
        for equal in infinite[name].equalList:
            first_set.add(equal[0])
        for first in first_set:
            same_equal = [equal for equal in infinite[name].equalList if equal[0] == first]
            if len(same_equal) > 1:
                """说明存在公共左因子，则采取提取公共左因子操作"""
                new_name = name_get[0]
                new_infinite = Infinite(new_name)
                name_get.remove(new_name)
                same = same_equal[0][0]
                for equ in same_equal:
                    new_infinite.equalList.append(equ[1:])
                    infinite[name].equalList.remove(equ)
                infinite[name].equalList.append(same + new_name)
                infinite[new_name] = new_infinite
    print("提取公共左因子后的文法：")
    for name in infinite.keys():
        print(name, end="->")
        s = '|'.join(infinite[name].equalList)
        print(s)


def removeLeft(expresses):
    """
    消除左递归
    :param expresses:  输入产生式
    :return:新的消除左递归后的文法
    """
    infinite, name_get = init(expresses)
    print("111")
    name_list = list(infinite.keys())
    print("111")
    for i in range(0, len(name_list)):
        infinite_i = infinite[name_list[i]]
        for j in range(0, i):
            infinite_j = infinite[name_list[j]]
            for equal in infinite_i.equalList:
                if equal[0] == infinite_j.name:
                    if len(equal) > 1:
                        for j_equal in infinite_j.equalList:
                            new_equal = j_equal + equal[1:]
                            infinite_i.equalList.append(new_equal)
                        infinite_i.equalList.remove(equal)
        new_name = name_get[0]  # 添加新非终结符
        target = []
        flag = False
        for k in range(len(infinite_i.equalList) - 1):
            if infinite_i.equalList[k][0] == infinite_i.name:  # 消除直接左递归
                flag = True
                for j in range(0, len(infinite_i.equalList)):
                    if infinite_i.equalList[j][0] != infinite_i.name:
                        """对于不是左递归的后加符号"""
                        infinite_i.equalList[j] += new_name
                target.append(infinite_i.equalList[k])
                infinite_i.equalList.remove(infinite_i.equalList[k])  # 删除左递归
        if flag:
            infinite_new = Infinite(new_name)
            for equ in target:
                equ_temp = equ[1:] + new_name
                infinite_new.equalList.append(equ_temp)
            infinite_new.equalList.append('ε')
            infinite[new_name] = infinite_new
            name_get.remove(new_name)
    print("消除左递归后的文法：")
    for name in infinite.keys():
        print(name, end="->")
        s = '|'.join(infinite[name].equalList)
        print(s)
    leftGet(infinite, name_get)
    """FIRST_get(infinite)
    FOLLOW_get(infinite)
    if LL_judge(infinite):
        print("是LL（1）文法")
    else:
        print("不是LL(1)文法")"""
    return infinite, name_get


def FIRST_next(infinite, name, get_record):
    """
    求解FIRST集使用的递归函数
    :param infinite: 终结符字典
    :param name: 要求解的终结符
    :param get_record: 记录是否已经求解过
    :return: None
    """
    if get_record[name]:
        return
    for equal in infinite[name].equalList:
        if equal[0].islower() or equal[0] in op:
            infinite[name].FIRST.setdefault(equal[0], [])
            infinite[name].FIRST[equal[0]].append(equal)
        elif equal == 'ε':
            infinite[name].FIRST.setdefault(equal, [])
            infinite[name].FIRST['ε'].append(equal)
        else:
            if not get_record[equal[0]]:  # 没有求解则需要递归求解
                FIRST_next(infinite, equal[0], get_record)
                # 判断是否含有空串
            if 'ε' in infinite[equal[0]].FIRST:  # 含有时则需要去除空串
                new_set = set(infinite[equal[0]].FIRST)
                new_set.discard('ε')
                # infinite[name].FIRST=infinite[name].FIRST.union(new_set)
                for key in infinite[equal[0]].FIRST.keys():
                    infinite[name].FIRST.setdefault(key, [])
                    infinite[name].FIRST[key].append(equal)
                for new_name in equal[1:]:
                    if new_name.islower() or equal[0] in op:
                        infinite[name].FIRST.setdefault(new_name, [])
                        infinite[name].FIRST[new_name].append(equal)
                        break
                    else:
                        FIRST_next(infinite, new_name, get_record)
                        if 'ε' not in infinite[equal[0]].FIRST:
                            for key in infinite[equal[0]].FIRST.keys():
                                infinite[name].FIRST.setdefault(key, [])
                                infinite[name].FIRST[key].append(equal)
                            break
                        else:
                            new1_set = set(infinite[equal[0]].FIRST)
                            new1_set.discard('ε')
                            for key in new1_set:
                                infinite[name].FIRST.setdefault(key, [])
                                infinite[name].FIRST[key].append(equal)
                            continue
            else:
                for key in infinite[equal[0]].FIRST.keys():
                    infinite[name].FIRST.setdefault(key, [])
                    infinite[name].FIRST[key].append(equal)

    get_record[name] = True


def FIRST_get(infinite):
    """
     求解FIRST集
    :param infinite:
    :return:返回更新后的字典
    """
    get_record = {}  # 用来记录那些非终结符的FIRST集已经被求解
    name_list = list(infinite.keys())
    for name in name_list:
        get_record[name] = False
    for name in name_list:
        FIRST_next(infinite, name, get_record)
    print("各个非终结符的FIRST集：")
    for name in name_list:
        print(name, end=":")
        print(infinite[name].FIRST)


def FOLLOW_next(infinite, name, get_record, name_list):
    if get_record[name]:  # 已被求结果则直接返回
        return
    for find_name in name_list:
        for equal in infinite[find_name].equalList:
            if name in equal:  # 要求解的非终结符在产生式中
                index = equal.index(name)
                if index == len(equal) - 1 and find_name != name:  # 在末尾位置
                    FOLLOW_next(infinite, find_name, get_record, name_list)  # 递归调用求解FOLLOW集
                    infinite[name].FOLLOW = infinite[name].FOLLOW.union(infinite[find_name].FOLLOW)
                elif index < len(equal) - 1 and (equal[index + 1].islower() or equal[index + 1] in op):  # 紧接着的为终结符
                    infinite[name].FOLLOW.add(equal[index + 1])
                else:  # 紧接着的是非终结符
                    if index < len(equal) - 1:
                        if 'ε' not in set(infinite[equal[index + 1]].FIRST.keys()):
                            keys = set(infinite[equal[index + 1]].FIRST.keys())
                            for key in keys:
                                infinite[name].FOLLOW.add(key)
                        else:  # 空串在内的情况
                            pos = index + 1
                            first = list(infinite[equal[pos]].FIRST.keys())  # 存储first集合
                            while 'ε' in first:
                                first.remove('ε')
                                for key in first:
                                    infinite[name].FOLLOW.add(key)
                                if equal[pos].islower() or equal[pos] in op:
                                    infinite[name].FOLLOW.add(equal[pos])
                                    break
                                if pos + 1 >= len(equal):
                                    break
                                else:
                                    pos += 1
                                    first = list(infinite[equal[pos]].FIRST.keys())

                            if pos + 1 == len(equal):
                                first = list(infinite[equal[pos]].FIRST.keys())
                                if 'ε' in first:
                                    FOLLOW_next(infinite, find_name, get_record, name_list)  # 递归调用求解FOLLOW集
                                    infinite[name].FOLLOW = infinite[name].FOLLOW.union(infinite[find_name].FOLLOW)

    get_record[name] = True


def FOLLOW_get(infinite, start=0):
    get_record = {}
    name_list = list(infinite.keys())
    for name in name_list:
        get_record[name] = False
    if start == 0:  # 说明没有自定义开始符号，默认以第一个符号为开始符号
        infinite[name_list[0]].FOLLOW.add('#')
    for name in name_list:
        FOLLOW_next(infinite, name, get_record, name_list)
    print("各个非终结符的FOLLOW集：")
    for name in name_list:
        print(name, end=":")
        print(infinite[name].FOLLOW)


def LL_judge(infinite):
    name_list = infinite.keys()
    flag = True
    for name in name_list:  # 验证第二个条件
        for first in infinite[name].FIRST.keys():
            if len(infinite[name].FIRST[first]) > 1:  # 对应多个产生式因此不是
                flag = False
                break
    if flag:  # 第二个条件满足判断第三个条件
        for name in name_list:
            first_set = set(infinite[name].FIRST.keys())
            follow_set = infinite[name].FOLLOW
            if 'ε' in first_set:
                if len(first_set.intersection(follow_set)) > 0:
                    flag = False
                    break
    return flag


def LL_analyse(table, express, start=0):
    """
    实现对输入表达式进行分析
    :param table: 之前建立的预测分析表
    :param express: 要分析的表达式
    :param start: 用户指定的开始符号
    :return:分析过程的各个状态
    """
    stack = []  # 建栈
    name_list = list(table.keys())
    actions = []  # 记录分析过程中的动作
    temp_stack = []  # 记录每一个分析步骤栈的状态
    temp_express = []  # 记录每一个分析步骤输入串的状态
    create_uses = []  # 记录每一个步骤使用的产生式
    stack.append('#')  # ‘#’号压入栈
    stack.append(name_list[start])
    actions.append('初始化')
    temp_stack.append(list(stack))  # 注意python
    temp_express.append(express)
    create_uses.append(' ')
    i = 0
    while True:
        if i >= len(express):
            break
        else:
            a = express[i]  # 读取输入字符存入a
            if len(stack) > 0:
                X = stack.pop()  # 弹出栈顶元素
            else:
                actions.append("异常表达式,分析结束")
                temp_express.append(express[i:])
                temp_stack.append(list(stack))
                create_uses.append("ERROR 异常")
                break
            if X.islower() or X in op or X == '#':  # 处理栈顶为终结符的情况
                if X == '#':
                    actions.append("LL(1)分析结束")
                    temp_express.append(express[i:])
                    temp_stack.append(list(stack))
                    create_uses.append("#")
                    break
                else:  # 两个终结符匹配
                    actions.append('GET NEXT')
                    temp_stack.append(list(stack))
                    create_uses.append(' ')
                    i += 1
                    temp_express.append(express[i:])

            elif X.isupper():  # 处理栈顶为非终结符的情况
                if a not in op and not a.isalnum() and a != '#':
                    actions.append("ERROR" + "跳过" + "{}".format(a))  # 进入下一个
                    stack.append(X)  # 将X中的元素重新放回
                    temp_express.append(express[i:])
                    temp_stack.append(list(stack))
                    create_uses.append(" ")
                    i += 1  # 跳过当前元素
                else:
                    if a.isalnum():  # 转换
                        a = 'i'
                    if table[X][a] == 'ERROR':  # 此时为ERROR则需要进行错误处理
                        actions.append("ERROR" + "跳过" + "{}".format(a))  # 进入下一个
                        stack.append(X)  # 将X中的元素重新放回
                        temp_express.append(express[i:])
                        temp_stack.append(list(stack))
                        create_uses.append(" ")
                        i += 1  # 跳过当前元素
                    elif table[X][a] == 'synch':
                        actions.append("synch" + "弹出" + "{}".format(X))
                        temp_stack.append(list(stack))
                        create_uses.append(" ")
                        temp_express.append(express[i:])
                    else:
                        create = ''.join(table[X][a])
                        if table[X][a] != 'ε':
                            actions.append("POP,PUSH({})".format(''.join(reversed(create))))
                            create_uses.append(X + "->" + ''.join(table[X][a]))
                            for s in reversed(create):
                                stack.append(s)
                            temp_stack.append(list(stack))
                            temp_express.append(express[i:])
                        else:
                            actions.append("POP")
                            create_uses.append(X + "->" + ''.join(table[X][a]))
                            temp_stack.append(list(stack))
                            temp_express.append(express[i:])
    print(temp_stack)
    print(temp_express)

    return temp_stack, temp_express, create_uses, actions


def LL_create_table(infinite):
    """
    建立LL(1)预测分析表,初步分析表
    :param infinite: 经处理后的文法信息
    :return: 建立的LL（1）预测分析表
    """
    inputSet = set()
    name_list = infinite.keys()
    table = {}
    for name in name_list:
        for s in infinite[name].FIRST.keys():
            inputSet.add(s)
        for s in infinite[name].FOLLOW:
            inputSet.add(s)
    inputSet.discard('ε')
    for s in inputSet:
        for name in name_list:
            table.setdefault(name, dict())
            table[name].setdefault(s, '')
            if s in infinite[name].FIRST.keys():  # 如果在内则直接将对应值放入表
                table[name][s] = infinite[name].FIRST[s]
            elif 'ε' in infinite[name].FIRST.keys() and s in infinite[name].FOLLOW:
                table[name][s] = 'ε'
            else:
                table[name][s] = 'ERROR'
    print(" ", end=" ")
    for s in inputSet:
        print('{:<15}'.format(s), end="|")
    print()
    for name in table.keys():
        print(name, end=":")
        for s in inputSet:
            print('{:<15}'.format(str(table[name][s])), end="|")
        print()
    return table


def LL_create_new_table(infinite):
    """
        建立LL(1)预测分析表,进一步的分析表，考虑到后期在进行实际语法分析时的异常处理因此不能只简单地考虑没发生异常的情况，因此分析表需要重新构造
        :param infinite: 经处理后的文法信息
        :return: 建立的LL（1）预测分析表
        """
    inputSet = set()
    name_list = infinite.keys()
    table = {}
    for name in name_list:
        for s in infinite[name].FIRST.keys():
            inputSet.add(s)
        for s in infinite[name].FOLLOW:
            inputSet.add(s)
    inputSet.discard('ε')
    for s in inputSet:
        for name in name_list:
            table.setdefault(name, dict())
            table[name].setdefault(s, '')
            if s in infinite[name].FIRST.keys():  # 如果在内则直接将对应值放入表
                table[name][s] = infinite[name].FIRST[s]
            elif 'ε' in infinite[name].FIRST.keys() and s in infinite[name].FOLLOW:
                table[name][s] = 'ε'
            elif 'ε' not in infinite[name].FIRST.keys() and s in infinite[name].FOLLOW:
                table[name][s] = 'synch'  # 同步符号
            else:
                table[name][s] = 'ERROR'
    print(" ", end=" ")
    for s in inputSet:
        print('{:<15}'.format(s), end="|")
    print()
    for name in table.keys():
        print(name, end=":")
        for s in inputSet:
            print('{:<15}'.format(str(table[name][s])), end="|")
        print()
    return table


if __name__ == "__main__":
    filename = 'rule.txt'
    expression = expressGet(filename)
    removeLeft(expression)

"""
E->TG
G->+T|-TG
G->ε
T->FS
S->*FS|/FS
S->ε
F->(E)
F->i
"""
