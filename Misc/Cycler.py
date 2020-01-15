class Cycler:
    def __init__(self, array:list, completion_callback:callable=None):
        """
        This class cylcles through each item in a specified list with each call to the "next" property, or the "next_item" method.
        Note that this class is iterable
        :param array: the array to cycle through
        :param completion_callback: The method which will be called (with no arguements) each time the cycler has completed a cycle. Leave as None to skip
        """
        self.array = array
        self.index = 0
        self.num = 0
        self.completion_callback = completion_callback

    def set_completion_callback(self, completion_callback:callable):
        """
        Set the completion callback (The method which will be called (with no arguements) each time the cycler has completed a cycle)
        :param completion_callback: The callback to run. Use None to disable 
        :return: 
        """
        self.completion_callback = completion_callback

    def append(self, item):
        """
        Appends the specified item to the end of the cycler.
        :param item: the item to append
        """
        self.array.append(item)

    def next_item(self):
        """
        This method returns the next item in the cycle
        :return: the next item
        """
        item = self.array[self.index]
        self.index += 1
        if self.index >= len(self.array):
            if self.completion_callback is not None:
                self.completion_callback()
            self.index = 0

        return item

    @property
    def next(self):
        """
        This method returns the next item in the cycle
        :return: the next item
        """
        return self.next_item()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            val = self.array[self.num]
            self.num += 1

            return val
        except IndexError:
            raise StopIteration
