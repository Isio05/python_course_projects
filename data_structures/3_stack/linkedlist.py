class LinkedList:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_start_to_list(self, node):
        marker = self.__root
        if marker:
            node.set_next(marker)
        self.__root = node

    def remove_start_from_list(self):
        """
        - If self.__root is None, raise a RuntimeError as the list is already empty
        - Create a variable which stores the root
        - Set self.__root to be equal to the root's next node
        - Return the variable created previously
        :return:
        """
        marker = self.__root

        if not marker:
            raise RuntimeError("List already empty.")

        if marker.get_next() is None:
            self.__root = None
            return marker

        self.__root = marker.get_next()
        return marker

    def print_list(self):
        marker = self.__root
        while marker:
            marker.print_details()
            marker = marker.get_next()

    def find(self, text):
        marker = self.__root
        while marker:
            if marker.text == text:
                return marker
            marker = marker.get_next()
        raise LookupError("The value {} has not been found".format(text))

    def size(self):
        marker = self.__root
        counter = 0
        while marker:
            counter += 1
            marker = marker.get_next()
        return counter
