import csv
import math

with open('../Table.txt', 'rb') as f:
    reader = csv.reader(f)
    toy_data_list = list(reader)

with open('../schillingData.txt', 'rb') as f:
    reader = csv.reader(f)
    data_list = list(reader)


class node:
    def __init__(self, column_num=-1, result_value=None):
        self.column_number = column_num
        self.result_value = result_value
        self.children = {}


def all_possible_results_count(examples):
    result_counts = {}
    for row in examples:
        output = row[-1]
        if output not in result_counts:
            result_counts[output] = 1
        else:
            result_counts[output] += 1
    return result_counts


def entropy(examples):
    results = all_possible_results_count(examples)
    total_results = len(examples)
    total_entropy = 0.0
    for key in results.keys():
        probability = float(results[key])/total_results
        total_entropy -= probability * (math.log(probability)/math.log(2))
    return total_entropy


def plurality_value(examples):
    results = all_possible_results_count(examples)
    max =-1
    max_value = None
    for key in results.keys():
        if results[key] > max:
            max = results[key]
            max_value = key
    return node(result_value=max_value)


def divide_examples(examples, value, column_number):
    examples_with_value = []
    for example in examples:
        if example[column_number] == value:
            examples_with_value.append(example)
    return examples_with_value


def create_tree (examples, attributes):
    results = all_possible_results_count(examples)
    if len(results) == 1:
        return plurality_value(examples)
    elif not attributes:
        return plurality_value(examples)
    else:
        column_num = importance(attributes, examples)
        # print data_list[0][column_num]

        current_node = node(column_num=column_num)

        possible_values = []
        for example in examples:
            if example[column_num] not in possible_values:
                possible_values.append(example[column_num])

        remaining_attr = []
        for attr in attributes:
            if(attr != column_num):
                remaining_attr.append(attr)

        for value in possible_values:
            examples_with_value = divide_examples(examples, value, column_num)
            current_node.children[value] = create_tree(examples_with_value, remaining_attr)

    return current_node


def importance(attributes, examples):
    max_gain = -1.0
    best_attribute = None
    total_entropy = entropy(examples)
    total_rows = len(examples)
    for column_num in attributes:
        possible_values = []
        for example in examples:
            if example[column_num] not in possible_values:
                possible_values.append(example[column_num])
        remainder = 0
        for value in possible_values:
            examples_with_value = divide_examples(examples, value, column_num)
            remainder += (float(len(examples_with_value)) / total_rows) * entropy(examples_with_value)

        information_gain = total_entropy - remainder
        if information_gain > max_gain:
            max_gain = information_gain
            best_attribute = column_num
    return best_attribute


def classify(test_example,tree):
    if tree.result_value != None:
        return tree.result_value
    col_value = test_example[tree.column_number]
    if tree.children.has_key(col_value):
        return classify(test_example,tree.children[col_value])


def find_accuracy(test_examples, tree):
    match = 0
    for example in test_examples:
        result = classify(example,tree)
        if result == example[-1]:
            match += 1
    return float(match)/len(test_examples)*100


def n_fold_validation(data_set,n=10):
    total_accuracy = 0
    attributes = []
    for col in range(0, len(data_set[0]) - 1):
        attributes.append(col)

    step = int(math.ceil(float(len(data_set))/n))
    for start in range(1,len(data_set), step):
        test_set = []
        training_set = []

        for index in range(1,len(data_set)):
            if start <= index < (start + step):
                test_set.append(data_set[index])
            else:
                training_set.append(data_set[index])
        tree = create_tree(training_set, attributes)
        accuracy = find_accuracy(test_set, tree)
        total_accuracy += accuracy
        print "Accuracy = " + str(accuracy)
    print "Average accuracy: " + str(float(total_accuracy)/n)



print "N-fold cross validation for toy data set (here, n=3)-> "
n_fold_validation(toy_data_list,3)

print "\nN-fold cross validation for real data set (here, n=10)-> "
n_fold_validation(data_list,10)