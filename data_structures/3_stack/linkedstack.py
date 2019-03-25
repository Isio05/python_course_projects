from linkedlist import LinkedList


class LinkedStack:
    """
    This class is a stack wrapper around a LinkedList.
    """

    def __init__(self):
        self.__linked_list = LinkedList()

    def push(self, node):
        """
        Add a node to the start of the linked list property.
        :param node: The Node to add
        :return: None
        """
        self.__linked_list.add_start_to_list(node)

    def pop(self):
        """
        Remove a node from the start of the linked list, and return
        the removed node.
        :return: Node, the last node of the linked list after being removed.
        """
        return self.__linked_list.remove_start_from_list()

    def print_details(self):
        self.__linked_list.print_list()

    def __len__(self):
        """
        Return the amount of Nodes in the linked list.
        :return:
        """
        return self.__linked_list.size()
