
import datetime
import os.path
import unittest

from .. import reader


class ReaderTest(unittest.TestCase):
    DATA =  os.path.join(os.path.dirname(__file__), 'data')

    def test_single_string(self):
        xml = """
        <wddxPacket version='1.0'>
        <header comment='PHP packet'/>
        <data>
            <string>PHP to WDDX packet example</string>
        </data>
        </wddxPacket>
        """
        data = reader.loads(xml)
        self.assertEqual(data, ['PHP to WDDX packet example',])

    def test_basic_types(self):
        xml = """
        <wddxPacket version='1.0'>
        <data>
            <number>3.1415926</number>
            <null />
            <string>Hello, world</string>
            <number>42</number>
            <dateTime>1998-06-12T04:32:12</dateTime>
            <boolean value='true'/>
            <boolean value='false'/>
        </data>
        </wddxPacket>
        """
        data = reader.loads(xml)
        expected = [
            3.1415926,
            None,
            'Hello, world',
            42,
            datetime.datetime(1998, 6, 12, 4, 32, 12),
            True,
            False,
        ]
        self.assertEqual(data, expected)

    def test_compound_types(self):
        xml = """
        <wddxPacket version='1.0'>
            <data>
            <struct>
                <var name='pi'><number>3.1415926</number></var>
                <var name='answer'><number>42</number></var>
                <var name='not_at_all'><null /></var>
                <var name='cities'>
                    <array length='3'>
                    <string>Auckland</string>
                    <string>Wellington</string>
                    <string>Christchurch</string>
                    </array>
                </var>
            </struct>
            </data>
        </wddxPacket>
        """
        data = reader.loads(xml)
        expected = [{
            'answer': 42,
            'cities': ['Auckland', 'Wellington', 'Christchurch'],
            'not_at_all': None,
            'pi': 3.1415926,
        }]
        self.assertEqual(data, expected)

    def test_from_file(self):
        path = os.path.join(self.DATA, 'wddx.xml')
        data = reader.load(path)
        expected = [{
            'carton_size': '12',
            'category': 'items',
            'full_name': 'Magirita coupe',
            'id': '311',
            'is_valid': 't',
            'long_desc': None,
            'name': '8429',
            'photo': '/uploaded/item/1039133948.jpg',
            'php_class_name': 'blue_item',
            'price': '5.91',
            'short_desc': '266ml margarita glass',
            'sub_cat': None,
            'sub_sub_cat': None,
            'thumbnail': '/uploaded/item/tn_1039133948.jpg',
        }]
        self.assertEqual(data, expected)

    def test_from_file2(self):
        path = os.path.join(self.DATA, 'wddx2.xml')
        data = reader.load(path)
        expected =  [{
            'a': [10, 'second element'],
            'b': True,
            'd': datetime.datetime(1998, 6, 12, 4, 32, 12),
            'n': -12.456,
            'obj': {'n': -12.456, 's': 'a string',},
            's': 'a string',
        }]
