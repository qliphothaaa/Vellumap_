import sys
DEBUG = False
class DataSerialize(object):
    def __init__(self):
        self.id = id(self)

    def serialize(self):
        raise NotImplemented()


    def deserialize(self, data, hashmap={}):
        raise NotImplemented()


if __name__ == '__main__':
    pass



           
