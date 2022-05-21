from .singleton import SingletonMeta
import yaml


class LoadFiles(metaclass=SingletonMeta):
    def getYaml(self, filepath):
        with open(filepath, 'r') as file_descriptor:
            data = yaml.load(file_descriptor)
        return data

    def getExcel(self, filepath):
        pass

    def getTxt(self, filepath):
        with open(filepath, 'r') as file_descriptor:
            data = file_descriptor.read()
            print(data)
