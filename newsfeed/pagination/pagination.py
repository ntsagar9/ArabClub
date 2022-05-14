from .node import Node


class Pagination:
    __page_size = 1

    def __init__(self, data, posts_count, pages_count) -> None:
        self.row_data = data
        self.posts_count = posts_count
        self.pages_count = pages_count
        if self.pages_count > posts_count:
            self.pages_count = self.posts_count

    @property
    def get_counts(self):
        count = round(self.posts_count / self.pages_count)
        remind = (count * self.pages_count) - (count * self.pages_count)
        return {"count": int(count), "remainder": remind}

    @property
    def data(self):
        return self.row_data

    def is_valid_count(self, data: list, count: int):
        if count > len(data):
            self.posts_count = len(data)
            return True
        return True

    def create_pagination(self) -> list:
        data_list = []
        counts_data = self.get_counts
        if self.is_valid_count(self.row_data, self.posts_count):
            if counts_data.get("count") > 0:
                for i in range(self.pages_count):
                    temp = []
                    cur_page_number = i + 1
                    for p in range(counts_data["count"]):

                        temp.append(self.row_data[0][0])
                        self.row_data.pop(0)
                    data_list.append(temp)
            return data_list
        else:
            pass

    @classmethod
    def set_size(cls, new_size):
        cls.__page_size = new_size
        return cls.__page_size


class post_queue(Pagination):
    def __init__(self, **kwargs) -> None:
        super(post_queue, self).__init__(**kwargs)
        self.node = Node()

    def push(self, data):
        new_node = Node()
        cur_node = self.node

        while True:
            if cur_node.next is None:
                cur_node.data = data
                break
            cur_node = cur_node.next
        new_node.data = data
        cur_node.next = new_node
        return cur_node

    def pop(self):
        cur_node = self.node
        self.node = self.node.next
        Node.floor_count()
        return cur_node.data

    def get(self, index: int):
        index = index
        cur_index = 1
        cur_node = self.node
        while True:
            if index == 0:
                raise ValueError("Queue range of index start from 1 not zero.")
            if cur_node.next is None:
                raise IndexError("Index out of range.!")

            if cur_index == index:
                return cur_node.data

            cur_index += 1
            cur_node = cur_node.next

    def push_list(self):
        pagination = self.create_pagination()
        for data in pagination:
            return self.push(data)

    @property
    def __len__(self):
        return self.node.__len__

    @property
    def len(self):
        return self.node.__len__
