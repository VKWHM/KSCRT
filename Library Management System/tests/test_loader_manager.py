from unittest import TestCase

from managers.loaders import JsonLoader, XmlLoader, YamlLoader, TomlLoader, CsvLoader, supportedExtensions

test_samples = [
    {
        "uuid": "03d462ed-dbac-43b4-8a66-c3cfaf47245a",
        "name": "The Hitchhiker's Guide To The Galaxy",
        "author": "Douglas Adams",
        "available": False,
        "issue_date": "2024/06/26 16:55:12",
        "expire_date": "2024/07/09 16:55:12",
        "number_of_readings": 17
    },
    {
        "uuid": "f07abcb2-1f4b-457b-a856-cdff22f7acfc",
        "name": "Watership Down",
        "author": "Richard Adams",
        "available": True,
        "issue_date": "",
        "expire_date": "",
        "number_of_readings": 51
    },
    {
        "uuid": "a74e8e90-2b3b-4c53-a166-8dfb3b2783b1",
        "name": "The Five People You Meet in Heaven",
        "author": "Mitch Albom",
        "available": True,
        "issue_date": "",
        "expire_date": "",
        "number_of_readings": 75
    },
    {
        "uuid": "d5feecd6-b41a-4d6e-bd7a-ad8eeed5b5bf",
        "name": "Speak",
        "author": "Laurie Halse Anderson",
        "available": True,
        "issue_date": "",
        "expire_date": "",
        "number_of_readings": 5
    },
    {
        "uuid": "d09d6221-dd8f-4667-a4e9-2f063ee37f5d",
        "name": "I Know Why the Caged Bird Sings",
        "author": "Maya Angelou",
        "available": True,
        "issue_date": "",
        "expire_date": "",
        "number_of_readings": 74
    }
]


class LoaderTestSetup():

    def test_supported_extensions(self):
        self.assertIn(self.loader.extension, supportedExtensions.keys(), "The loader extension is not registered.")

    def test_serialize(self):
        serialized = self.loader.serialize(test_samples)
        self.assertIsNotNone(serialized)

    def test_deserialize(self):
        serialized = self.loader.serialize(test_samples)
        deserialized = self.loader.deserialize(serialized)
        sort_funtion = lambda dict_: dict_['number_of_readings']
        self.assertEqual(sorted(test_samples, key=sort_funtion), sorted(deserialized, key=sort_funtion),
                         "The deserialized content is not the same as the original.")


class TestJsonLoader(TestCase, LoaderTestSetup):
    def setUp(self):
        self.loader = JsonLoader()


class TestYamlLoader(TestCase, LoaderTestSetup):
    def setUp(self):
        self.loader = YamlLoader()


class TestTomlLoader(TestCase, LoaderTestSetup):
    def setUp(self):
        self.loader = TomlLoader()


class TestXmlLoader(TestCase, LoaderTestSetup):
    def setUp(self):
        self.loader = XmlLoader()


class TestCsvLoader(TestCase, LoaderTestSetup):
    def setUp(self):
        self.loader = CsvLoader()
