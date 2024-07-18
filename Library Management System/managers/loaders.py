import csv
import io
import json
import os
import xml.etree.ElementTree as Et
from abc import ABCMeta, abstractmethod

import toml
import yaml

from utils import list2dict, dict2list, Book


class BaseLoader[T](metaclass=ABCMeta):
    """
    Abstract base class for loaders.

    Attributes:
        extension (str): The file extension that this file loader supports.
        filePath (str): The path of the file to load or save.
        fileName (str): The name of the file to load or save.
        fileExt (str): The extension of the file to load or save.
    """
    extension: str = NotImplemented

    def __init__(self, filePath=''):
        """
        Initializes a new instance of the BaseLoader class.

        Args:
            filePath (str): The path of the file to load or save.
        """
        self.filePath = filePath
        self.fileName, self.fileExt = os.path.splitext(filePath)

    def load(self) -> T:
        """
        Loads the content of the file.

        Returns:
            list[Book]: The content of the file.
        """
        with open(self.filePath, 'r') as file:
            content = file.read()
        return self.deserialize(content)

    def save(self, content: T):
        """
        Saves the content to the file.

        Args:
            content (list[Book]): The content to save to the file.
        """
        serialized_content = self.serialize(content)
        with open(self.filePath, 'w') as file:
            file.write(serialized_content)

    @abstractmethod
    def deserialize(self, serialized_content: str) -> T:
        """
        Deserializes the content of the file.

        Args:
            serialized_content (str): The serialized content of the file.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def serialize(self, content: T) -> str:
        """
        Serializes the content to save to the file.

        Args:
            content (object): The content to save to the file.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError


# A dictionary to store the supported file extensions and their corresponding loader classes.
supportedExtensions: dict[str, BaseLoader] = {}


def register_extension(class_):
    """
    Registers a file loader class for a specific file extension.

    Args:
        class_ (Type[BaseLoader]): The loader class to register.

    Returns:
        Type[BaseLoader]: The registered loader class.

    Raises:
        RuntimeError: If a loader class for the same file extension is already registered.
    """
    if class_.extension not in supportedExtensions.keys():
        supportedExtensions[class_.extension] = class_
        return class_
    raise RuntimeError(f"[!!] The {class_.__name__} was already register.")


@register_extension
class JsonLoader[T](BaseLoader[T]):
    extension = ".json"

    def deserialize(self, serialized_content):
        return json.loads(serialized_content)

    def serialize(self, content):
        return json.dumps(content, indent=3)


@register_extension
class XmlLoader[T: list[Book]](BaseLoader[T]):
    extension = ".xml"

    def deserialize(self, serialized_content):
        root = Et.fromstring(serialized_content)
        return self._elements2list(root)

    def serialize(self, content):
        return Et.tostring(self._list2elements(content), encoding='unicode')

    @staticmethod
    def _list2elements(list_: T):
        parent = Et.Element('Library')
        dict_ = list2dict(list_)
        for uuid, item in dict_.items():
            element = Et.SubElement(parent, 'book', {"uuid": uuid})
            for key, value in item.items():
                sub_element = Et.SubElement(element, key)
                sub_element.text = str(value)
        return parent

    @staticmethod
    def _elements2list(elements) -> T:
        result_list = []
        for element in elements:
            item = {}
            for sub_element in element:
                value = sub_element.text
                try:
                    value = int(value)
                except ValueError:
                    if value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                except TypeError:
                    value = ''
                finally:
                    item[sub_element.tag] = value
            item['uuid'] = element.attrib['uuid']
            result_list.append(item)
        return result_list


@register_extension
class YamlLoader[T](BaseLoader[T]):
    extension = ".yaml"

    def deserialize(self, serialized_content):
        return dict2list(yaml.safe_load(serialized_content))

    def serialize(self, content):
        return yaml.dump(list2dict(content), default_flow_style=False)


@register_extension
class TomlLoader[T](BaseLoader[T]):
    extension = ".toml"

    def deserialize(self, serialized_content: str) -> list:
        return dict2list(toml.loads(serialized_content))

    def serialize(self, content: list) -> str:
        return toml.dumps(list2dict(content))


@register_extension
class CsvLoader[T: list[dict]](BaseLoader[T]):
    extension = ".csv"

    def deserialize(self, serialized_content):
        input_ = io.StringIO(serialized_content)
        rows = list(csv.DictReader(input_))

        for row in rows:
            for key, value in row.items():
                try:
                    value = int(value)
                except ValueError:
                    if value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                finally:
                    row[key] = value
        return list(rows)

    def serialize(self, content):
        output = io.StringIO()
        if len(content) != 0:
            writer = csv.DictWriter(output, fieldnames=content[0].keys())
            writer.writeheader()
            writer.writerows(content)
        return output.getvalue()


def dump_data[T](data: T, filePath: str):
    """
    Dumps a list of books to a file.

    Args:
        data (Generic[T]): The list of books to dump.
        filePath (str): The path of the file to dump the books to.

    Raises:
        TypeError: If the file format is unsupported.
    """
    if (loaderClass := supportedExtensions.get(os.path.splitext(filePath)[1].lower())) is not None:
        loader = loaderClass[T](filePath)
        loader.save(data)
    else:
        raise TypeError(f"File format of {filePath} is unsupported!!")


def get_loader(filePath) -> BaseLoader:
    """
    Gets a file loader for a specific file.

    Args:
        filePath (str): The path of the file to get a loader for.

    Returns:
        BaseLoader: The file loader for the file.

    Raises:
        TypeError: If the file format is unsupported.
        FileExistsError: If the file does not exist.
    """
    if os.path.exists(filePath):
        fileName, fileExtension = os.path.splitext(os.path.basename(filePath))
        if (loaderClass := supportedExtensions.get(fileExtension.lower())) is not None:
            return loaderClass
        raise TypeError(f"File format of {fileName + fileExtension} is unsupported!!")
    raise FileExistsError(f"{filePath} not exsits !!")
