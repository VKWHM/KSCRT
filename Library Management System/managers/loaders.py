import json
import os
from abc import ABCMeta, abstractmethod

from utils import Book


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


# TODO: Implement the YamlLoader class

# TODO: Implement the TomlLoader class

# TODO: Implement the XmlLoader class

# TODO: Implement the CsvLoader class


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
