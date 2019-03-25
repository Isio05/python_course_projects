from linkedlist import LinkedList


class LinkedQueue:
    """
    This class is a queue wrapper around a LinkedList.
    """

    def __init__(self):
        self.__linked_list = LinkedList()

    def push(self, node):
        """
        Add a node to the linked list property.
        :param node: The Node to add
        :return: None
        """
        self.__linked_list.add_start_to_list(node)

    def pop(self):
        """
        Remove a node from the end of the linked list, and return
        the removed node.
        :return: Node, the last node of the linked list after being removed.
        """
        return self.__linked_list.remove_end_from_list()

    def find(self, name):
        return self.__linked_list.find(name)

    def print_details(self):
        self.__linked_list.print_list()

    def __len__(self):
        """
        Return the amount of Nodes in the linked list.
        :return:
        """
        return self.__linked_list.size()
