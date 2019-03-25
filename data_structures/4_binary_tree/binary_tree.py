class BinaryTree:
    """
    This class is a binary tree implementation.
    """

    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add(self, node):
        """
        Add a node to the binary tree.
        If a node with that value already exists, raise a ValueError
        :param node: The Node to add
        :return: None
        """
        # The root is None, so set the root to be the new Node.
        if not self.__root:
            self.__root = node
        else:
            # Start iterating over the tree.
            marker = self.__root
            while marker:
                if node.value == marker.value:
                    raise ValueError("The node {} currently exists.".format(marker.value))
                elif node.value > marker.value:
                    if not marker.get_right():
                        marker.set_right(node)
                        return
                    else:
                        marker = marker.get_right()
                elif node.value < marker.value:
                    if not marker.get_left():
                        marker.set_left(node)
                        return
                    else:
                        marker = marker.get_left()

    def find(self, value):
        """
        Locate a node with a given value, and return it.
        If the Node is not found, it should raise a LookupError

        :param value: The value of the Node to locate.
        :return: Node, the found Node
        """
        marker = self.__root
        while marker:
            if marker.value == value:
                return marker
            elif value > marker.value:
                marker = marker.get_right()
            elif value < marker.value:
                marker = marker.get_left()
        raise LookupError("The {} value has not been found!".format(value))

    def print_inorder(self):
        self.__print_inorder_r(self.__root)

    def __print_inorder_r(self, current_node):
        if not current_node:
            return
        self.__print_inorder_r(current_node.get_left())
        print(current_node.print_details())
        self.__print_inorder_r(current_node.get_right())
