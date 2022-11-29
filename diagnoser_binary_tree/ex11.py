###########################################################################
# FILE: ex11.py
# WRITER: Mariia Makarenko, makarenko, 342849676
# EXERCISE: intro2cs1 ex1 2021
# DESCRIPTION: A simple program that builds decision trees and calculates
# diagnoses according to them.
###########################################################################
import itertools


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root: Node):
        self.root = root

    def diagnose(self, symptoms):
        """
        This function moves in a decision tree according to symptoms: if a
        symptom in a tree is in symptoms, the function goes in a positive
        direction in a tree. Else, in negative.
        :param symptoms: a list of symptoms
        :return: an illness
        """
        return self._diagnose_helper(self.root, symptoms)

    def _diagnose_helper(self, root, symptoms):
        """This is a recursive helper function for the diagnose function."""
        if root:
            if root.positive_child is None and root.negative_child is None:
                return root.data
            if root.data in symptoms and root.positive_child is not None:
                return self._diagnose_helper(
                    root.positive_child, symptoms)
            elif root.data not in symptoms and root.negative_child is not None:
                return self._diagnose_helper(
                    root.negative_child, symptoms)

    def calculate_success_rate(self, records):
        """
        This function calculates a success rate for a tree in the root
        attribute of self. It uses the diagnose function to diagnose illness.
        If the illness matches the symptoms in records, then the diagnosis
        is precise. The function then calculates the rate by dividing the
        number of correct diagnoses by the total number of diagnoses (by the
        length of the records).
        :param records: a list of objects of class Record
        :return: percentage of correct diagnoses
        """
        if len(records) == 0:
            raise ValueError("Records are empty!")
        else:
            success_sum = 0
            for record in records:
                if self.diagnose(record.symptoms) == record.illness:
                    success_sum += 1
            return success_sum / len(records)

    def all_illnesses(self):
        """
        This function goes to the leaves of the tree, collects their values
        and returns them.
        :return: a list of all the illnesses in the tree, sorted from the most
        common one to the less
        """
        diseases_dict = self._all_illnesses_helper(self.root, {})
        return sorted(diseases_dict, key=diseases_dict.get, reverse=True)

    def _all_illnesses_helper(self, root, diseases_dict):
        """This is a recursive helper function for the all_illnesses
        function."""
        if root.positive_child is None and root.negative_child is None and \
                root.data is not None:
            disease = root.data
            if disease and disease in diseases_dict:
                diseases_dict[disease] += 1
            else:
                diseases_dict[disease] = 1
        else:
            if root.positive_child is not None:
                self._all_illnesses_helper(root.positive_child, diseases_dict)
            if root.negative_child is not None:
                self._all_illnesses_helper(root.negative_child, diseases_dict)
        return diseases_dict

    def paths_to_illness(self, illness):
        """
        This function returns all the ways of reaching a given illness in the
        tree in the form of list of lists where each list is a path. In each
        path True means "positive direction", False means "negative direction".
        :param illness: a string or None representing an illness
        :return: a list of lists wir=th all possible paths to the illness
        """
        return self._paths_to_illness_helper(illness, self.root, [], [])

    def _paths_to_illness_helper(self, illness, root, temp, result):
        """This is a recursive helper function for the paths_to_illnesses
        function."""
        if root.positive_child is None and root.negative_child is None:
            if root.data == illness:
                result.append(temp)
            return result
        if root.positive_child is not None:
            self._paths_to_illness_helper(
                illness, root.positive_child, temp + [True], result)
        if root.negative_child is not None:
            self._paths_to_illness_helper(
                illness, root.negative_child, temp + [False], result)
        return result

    def minimize(self, remove_empty=False):
        """
        This function changes the tree by getting rid of those nodes that do
        not affect the final decision. If remove_empty is True, all the
        children that lead to the None decisions are also removed.
        :param remove_empty: True/False
        :return: None
        """
        self.root = self._minimize_helper(remove_empty, self.root)

    def _minimize_helper(self, remove_empty, root):
        """This is a recursive helper function for the minimize function."""
        if root is None:
            return
        if root.positive_child is None and root.negative_child is None:
            return root
        root.positive_child = self._minimize_helper(remove_empty,
                                                    root.positive_child)
        root.negative_child = self._minimize_helper(remove_empty,
                                                    root.negative_child)
        if root.positive_child is None:
            if remove_empty and root.negative_child.data is None:
                return None
            elif root.negative_child.data is not None:
                return root.negative_child
        elif root.negative_child is None:
            if remove_empty and root.positive_child.data is None:
                return None
            elif root.positive_child.data is not None:
                return root.positive_child
        elif root.negative_child is not None and root.positive_child is not \
                None:
            if remove_empty:
                if root.negative_child.data is None:
                    return root.positive_child
                elif root.positive_child.data is None:
                    return root.negative_child
            if root.positive_child.data == root.negative_child.data:
                if self._is_leaf(root.positive_child) and \
                        self._is_leaf(root.negative_child) or \
                        self._is_symmetric(root):
                    return root.positive_child
        return root

    def _is_symmetric(self, root):
        """
        This function checks if a tree is the same tree by the y axis.
        :param root: a tree
        :return: True if the same, False if it is not
        """
        return self._is_symmetric_helper(root.positive_child,
                                         root.negative_child)

    def _is_symmetric_helper(self, root1, root2):
        """This is a recursive helper function for the is_symmetric
        function."""
        if root1 is None and root2 is None:
            return True
        else:
            if root1.data == root2.data and \
                    self._is_symmetric_helper(root1.positive_child,
                                              root2.positive_child) \
                    and self._is_symmetric_helper(root1.negative_child,
                                                  root2.negative_child):
                return True
        return False

    def _is_leaf(self, root):
        """This function checks if a root is a leaf."""
        if root.positive_child is None and root.negative_child is None:
            return True
        return False


def build_tree(records, symptoms):
    """
    This function returns an optimal tree that checks all the symptoms from
    the symptoms list and to each combination of symptoms in the tree appends
     a leaf of illness that better suits it.
    :param records: a list of records (if not all of class Record, TypeError)
    :param symptoms: a list of symptoms
    :return: Diagnoser object for the tree that was built
    """
    if len([record for record in records if type(record) != Record]) != 0:
        raise TypeError("Records contain objects not of class Record")
    if len([symptom for symptom in symptoms if type(symptom) != str]) != 0:
        raise TypeError("Symptoms contain not only strings")
    return Diagnoser(_build_tree_helper(records, symptoms, 0))


def _build_tree_helper(records, symptoms, index):
    """This is a recursive helper function for the build tree function."""
    if index == len(symptoms):
        if records:
            new_records = [record.illness for record in records]
            new_records = sorted(set(new_records),
                                 key=lambda x: new_records.count(x),
                                 reverse=True)
            disease = new_records[0]
            return Node(disease)
        else:
            return Node(None)
    positive_sub_tree = _build_tree_helper(
        [record for record in records if symptoms[index] in record.symptoms],
        symptoms, index + 1)
    negative_sub_tree = _build_tree_helper(
        [record for record in records if symptoms[index] not in
         record.symptoms], symptoms, index + 1)
    return Node(symptoms[index], positive_sub_tree, negative_sub_tree)


def optimal_tree(records, symptoms, depth):
    """
    This function returns a tree that is made of a group of symptoms that has
    a length depth that has the best success rate.
    :param records: a list of records (if not all of class Record, TypeError)
    :param symptoms: a list of symptoms (if not all of them strings, TypeError,
     if there is a double symptom, ValueError)
    :param depth: a number of symptoms that must be in a tree. If less than 0
    or more than the symptoms length, ValueError
    :return: a tree with the best success rate
    """
    if depth < 0 or depth > len(symptoms):
        raise ValueError("Invalid depth value")
    if len(set(symptoms)) < len(symptoms):
        raise ValueError("Double symptoms")
    if len([record for record in records if type(record) != Record]) != 0:
        raise TypeError("Records contain objects not of class Record")
    if len([symptom for symptom in symptoms if type(symptom) != str]) != 0:
        raise TypeError("Symptoms contain not only strings")
    trees = {}
    for group_of_symptoms in itertools.combinations(symptoms, depth):
        tree = build_tree(records, group_of_symptoms)
        if len(records) == 0:
            return tree
        trees[tree] = tree.calculate_success_rate(records)
    trees = sorted(trees, key=trees.get, reverse=True)
    if trees:
        return trees[0]
    return None
