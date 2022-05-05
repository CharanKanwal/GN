import ast
import json
import pandas as pd
import copy

def json_flatten(value):
    #li_checker.append(value)
    global nest_keys
    if type(value) == dict:
        for i in value:
            if type(value[i]) == list:
                if type(value[i][0]) == dict and len(value[i]) >1:
                    nest_keys += 1
            if(type(value[i])) == str:
                if value[i] != "":
                    if value[i][0] == "[" and value[i][1] != "]":
                        if type(ast.literal_eval(value[i])) == list:
                            value[i] = ast.literal_eval(value[i])
                            if type(value[i][0]) == dict and len(value[i]) >1:
                                nest_keys += 1
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            if type(value[i]) == bool:
                continue

            if type(value[i]) == dict:
                for k in value[i]:
                    if type(value[i][k]) != list and type(value[i][k]) != dict:
                        continue
                    if type(value[i][k]) == list:
                        if type(value[i][k][0]) == dict and len(value[i][k]) >1:
                            nest_keys+=1
                    if type(value[i][k]) == dict:
                        for ki in value[i][k]:
                            if type(value[i][k][ki]) != list and type(value[i][k][ki]) != dict:
                                continue
                            if type(value[i][k][ki]) == list:
                                if type(value[i][k][ki][0]) == dict and len(value[i][k][ki]) >1:
                                    nest_keys+=1



    if type(value) == list:
        for r in range(0,len(value)):
            json_flatten(value[r])

    print(nest_keys)
    if nest_keys > 0:
        if type(value) == dict:
            if nest_keys != len(value.keys()):
                key_len_counter(value)
            else:
                main(value)
        if type(value) == list:
            if nest_keys != len(value[0].keys()):
                key_len_counter(value)
    else:
        main(value)



def main(value, currentObject={}, currentList=[]):

    if (type(value) == dict):
        handleDict(value, currentObject, currentList)
    elif (type(value) == list):
        handleArray(value, currentObject, currentList)
    else:
        handleValues(value, currentObject, currentList)


def handleDict(value, currentObject, currentList):
    countOfNonDictsAndLists = 0

    for i in value:
        if (type(value[i]) == list):
            if (len(value[i]) == 0):
                value[i] = None
            elif (len(value[i]) == 1):
                value[i] = value[i][0]

    for i in value:
        if (type(value[i]) != dict and type(value[i]) != list):
            countOfNonDictsAndLists += 1
            newList = currentList.copy()
            newList.append(i)
            currentObject[".".join(newList)] = value[i]

    if (countOfNonDictsAndLists == len(value.keys())):
        addRowToArray(currentObject)

    for i in value:
        if (type(value[i]) == dict):
            newList = currentList.copy()
            newList.append(i)
            main(value[i], currentObject, newList)

    for i in value:
        if (type(value[i]) == list):
            newList = currentList.copy()
            newList.append(i)
            main(value[i], currentObject, newList)

# THIS IS DONE
def handleArray(value, currentObject, currentList):
    for i in range(0, len(value)):
        newObject = currentObject.copy()
        main(value[i], newObject, currentList)

# THIS IS DONE
def handleValues(value, currentObject, currentList):
    currentObject[".".join(currentList)] = value
    addRowToArray(currentObject)

# THIS IS DONE
def addRowToArray(value):
    matchCounter = 0
    for i in range(0, len(finalList)):
        if (objectSimilarity(value, finalList[i])):
            matchCounter+=1
    if (matchCounter == 0):
        finalList.append(value)
        #print(finalList)

# THIS IS DONE
def objectSimilarity(obj1, obj2):
    for i in obj1:
        if (obj1.get(i) != obj2.get(i)):
            return False
    return True



def main_nest(value, list_of_nest_keys, ordered_nesting, currentObject={}, currentList=[],):

    if (type(value) == dict):
        handleDict_nest(value,list_of_nest_keys,ordered_nesting, currentObject,currentList)
    elif (type(value) == list):
        handleArray_nest(value,list_of_nest_keys, ordered_nesting, currentObject, currentList)
    else:
        handleValues_nest(value, currentObject, currentList,ordered_nesting)


def handleDict_nest(value, list_of_nest_keys,ordered_nesting, currentObject, currentList):
    countOfNonDictsAndLists = 0

    for i in value:
        if (type(value[i]) == list):
            if (len(value[i]) == 0):
                value[i] = None
            elif (len(value[i]) == 1):
                value[i] = value[i][0]

    for i in value:
        if (type(value[i]) != dict and type(value[i]) != list or i in list_of_nest_keys):
            countOfNonDictsAndLists += 1
            newList = currentList.copy()
            newList.append(i)
            k = ".".join(newList)
            if k not in list_of_nest_keys:
                currentObject[".".join(newList)] = value[i]

    if (countOfNonDictsAndLists == len(value.keys())):
        addRowToArray_nest(currentObject,ordered_nesting)

    for i in value:
        if (type(value[i]) == dict):
            newList = currentList.copy()
            newList.append(i)
            main_nest(value[i],list_of_nest_keys,ordered_nesting, currentObject, newList)

    for i in value:
        if (type(value[i]) == list):
            if i not in list_of_nest_keys:
                newList = currentList.copy()
                newList.append(i)
                j = ".".join(newList)
                if j not in list_of_nest_keys:
                    main_nest(value[i],list_of_nest_keys,ordered_nesting, currentObject, newList)

# THIS IS DONE
def handleArray_nest(value,list_of_nest_keys,ordered_nesting, currentObject, currentList):
    for i in range(0, len(value)):
        newObject = currentObject.copy()
        main_nest(value[i],list_of_nest_keys,ordered_nesting, newObject, currentList)

# THIS IS DONE
def handleValues_nest(value, currentObject, currentList,ordered_nesting):
    currentObject[".".join(currentList)] = value
    addRowToArray_nest(currentObject,ordered_nesting)

# THIS IS DONE
def addRowToArray_nest(value,ordered_nesting):
    #print(value)
    matchCounter = 0
    #print(len(value.keys()),p, sep="|")

    if len(value.keys()) == non_nest_count:
        for m in range(0,len(ordered_nesting)):
            #print(value)
            value1 = value.copy()
            #print(value1)
            value1.update(ordered_nesting[m])
            #print(value1)
            #print(value1)
            for i in range(0, len(finalList)):
                if (objectSimilarity_nest(value1, finalList[i])):
                    matchCounter+=1
            if (matchCounter == 0):
                finalList.append(value1)
        #print(finalList)

def objectSimilarity_nest(obj1, obj2):
    for i in obj1:
        if (obj1.get(i) != obj2.get(i)):
            return False
    return True

def key_len_counter(val):
    #print(val)
    global non_nest_count
    li.append(val)
    if type(val) == dict:
        for i in val:
            if type(val[i]) == list:
                if len(val[i]) == 0:
                    non_nest_count+=1
                if type(val[i][0]) == dict and len(val[i]) == 1:
                    non_nest_count+= len(val[i][0].keys())
                if type(val[i][0]) == dict and len(val[i]) > 1:
                    continue

            if type(val[i]) == dict:
                for k in val[i]:
                    if type(val[i][k]) != list and type(val[i][k]) != dict:
                        non_nest_count+=1
                    if type(val[i][k]) == list:
                        if type(val[i][k][0]) == dict and len(val[i][k]) >1:
                            continue
                        if type(val[i][k][0]) == dict and len(val[i][k]) ==1:
                            non_nest_count+=len(val[i][k][0].keys())
                            continue
                    if type(val[i][k]) == dict:
                        for ki in val[i][k]:
                            if type(val[i][k][ki]) != list and type(val[i][k][ki]) != dict:
                                non_nest_count+=1
                            if type(val[i][k][ki]) == list:
                                if type(val[i][k][ki][0]) == dict and len(val[i][k][ki]) >1:
                                    continue
                                if type(val[i][k][ki][0]) == dict and len(val[i][k][ki]) ==1:
                                    non_nest_count+=len(val[i][k][0].keys())
                                    continue

            if type(val[i]) != list and type(val[i]) != dict:
                if(type(val[i])) == str:
                    if val[i] != "":
                        if val[i][0] == "[" and val[i][1] != "]":
                            if type(ast.literal_eval(val[i])) == list:
                                val[i] = ast.literal_eval(val[i])
                                if type(val[i][0]) == dict and len(val[i]) >1:
                                    continue
                                if type(val[i][0]) == dict and len(val[i]) ==1:
                                    non_nest_count+=len(val[i][0].keys())
                                    continue

                    non_nest_count+=1
                else:
                    non_nest_count+=1


    if type(val) == list:
        for j in range(0,len(val)):
            if type(val[j]) == dict:
                key_len_counter(val[j])


    nest_key_tracker(li[0])


def nest_key_tracker(value,current_nest=[],list_of_nest=[]):
    global nest_keys
    list1.append(value)

    if type(value) == dict:
        for i in value:
            if type(value[i]) == list:
                current_key_nest = current_nest.copy()
                current_key_nest.append(i)
                nest_key_tracker1(value[i],current_key_nest,list_of_nest)

            if type(value[i]) == dict:
                new_list = current_nest.copy()
                new_list.append(i)
                nest_key_tracker(value[i],new_list,list_of_nest)

            if(type(value[i])) != list and (type(value[i])) != dict:
                current_key_nest = current_nest.copy()
                current_key_nest.append(i)
                nest_key_tracker2(value[i],current_key_nest,list_of_nest)

    if type(value) == list:
        for r in range(0,len(value)):
            nest_key_tracker(value[r])

    if nest_keys == len(nest_dict.keys()):
        nest_dict_breaker(list1[0],list_of_nest)



def nest_key_tracker1(value,current_nest,list_of_nest):
    for r in range(0,len(value)):
        if type(value[0]) == dict and len(value) > 1:
            current_key_nest = current_nest.copy()
            m = ".".join(current_key_nest)
            list_of_nest.append(m)
            nest_dict[m] = value



def nest_key_tracker2(value,current_nest,list_of_nest):
    if(type(value)) == str:
        if value != "":
            if value[0] == "[" and value[1] != "]":
                if type(ast.literal_eval(value)) == list:
                    value = ast.literal_eval(value)
                    if type(value[0]) == dict and len(value) >1:
                        current_key_nest = current_nest.copy()
                        m = ".".join(current_key_nest)
                        list_of_nest.append(m)
                        nest_dict[m] = value


def nest_dict_breaker(val,list_of_nest,new_nest_dict={}):
    new_nest_dict = copy.deepcopy(nest_dict)

    for k in nest_dict:
        for i in range(0,len(nest_dict[k])):
            j =0
            for key in nest_dict[k][i]:
                if type(nest_dict[k][i][key]) != dict and type(nest_dict[k][i][key]) !=list:
                    continue
                if type(nest_dict[k][i][key]) == dict:
                    j+=1

            if j == 0:
                continue
            if j>0:
                new_nest_dict[k][i] = {}
                for key in nest_dict[k][i]:

                    if type(nest_dict[k][i][key]) != dict and type(nest_dict[k][i][key]) != list:
                        new_nest_dict[k][i][key] = nest_dict[k][i][key]
                    if type(nest_dict[k][i][key]) == dict:
                        for kie in nest_dict[k][i][key]:
                            m = ".".join([key,kie])

                            new_nest_dict[k][i][m] = nest_dict[k][i][key][kie]


    incorporate_nest(val,new_nest_dict,list_of_nest)


def incorporate_nest(val,new_nest_dict,list_of_nest_keys,list_of_row_nest =[]):

    li = []
    for k in new_nest_dict:
        li.append(len(new_nest_dict[k]))
    len_max = max(li)
    list_of_row_nest = []
    for j in range(0,len_max):
        dict = {}
        for k in new_nest_dict:
            if len(new_nest_dict[k]) >= j+1:
                dict[k] = new_nest_dict[k][j]
        list_of_row_nest.append(dict)
    dict_breaker(list_of_row_nest,val,list_of_nest_keys)




def dict_breaker(l,val,list_of_nest_keys,dict_new={},list_of_nest_dict=[]):
    matchCounter = 0
    for i in range(0,len(l)):
        dict_new = {}
        for k in l[i]:
            list = []
            list.append(k)
            for key in l[i][k]:
                l_new = list.copy()
                l_new.append(key)
                ki = ".".join(l_new)
                #print(ki)
                dict_new[ki] = l[i][k][key]
        for i in range(0, len(list_of_nest_dict)):
            if objectSimilarity_nest(dict_new, list_of_nest_dict[i]):
                matchCounter+=1
        if matchCounter == 0:
            list_of_nest_dict.append(dict_new)

    #print(list_of_nest_dict)
    main_nest(val,list_of_nest_keys,list_of_nest_dict)



with open('D:\\companies.json') as f:
    data = json.load(f)

nest_dict = {}
list1 = []
li = []
nest_keys = 0
non_nest_count = 0
finalList = []

json_flatten(data)
df = pd.DataFrame(finalList)
