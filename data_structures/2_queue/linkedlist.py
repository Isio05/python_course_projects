class LinkedList:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_start_to_list(self, node):
        """
        :param node: the node to add at the start
        :return: None
        """
        if self.__root:
            node.set_next(self.__root)
        self.__root = node

    def remove_end_from_list(self):
        """
        - Iterate over each node
        - Find both the second-to-last node and the last node
        - Set the second-to-last node's next to be None
        - Return the last node
        :return: the removed Node.
        """
        marker = self.__root

        if not marker.get_next():
            self.__root = None
            return marker

        while marker is not None:
            following_node = marker.get_next()
            if following_node:
                if following_node.__next is None:
                    marker.set_next(None)
                    return following_node
            marker = marker.get_next()

    def print_list(self):
        marker = self.__root
        while marker:
            marker.print_details()
            marker = marker.get_next()

    def find(self, name):
        """
        :param name: the name of the Node to find.
        :return: the found Node, or raises a LookupError if not found.
        """
        marker = self.__root
        while marker:
            if marker.name == name:
                return marker
            marker = marker.get_next()
        raise LookupError("Value {} has not been found".format(name))

    def size(self):
        """
        :return: the amount of nodes in this list.
        """
        marker = self.__root
        counter = 0
        while marker.__next:
            marker = marker.get_next()
            counter += 1
        return counter
