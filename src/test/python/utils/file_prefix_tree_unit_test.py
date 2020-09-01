import unittest

from utils.file_prefix_tree import FilePrefixTree


class TestPrefixTree(unittest.TestCase):
    def test_init(self):
        paths = []
        tree = FilePrefixTree("C:\\", paths)
        root = tree.root
        self.assertEqual("ROOT", root.name)
        self.assertEqual(1, len(root.children))
        basedir = tree.root.children[0]
        self.assertEqual("C:", basedir.name)
        self.assertEqual(0, len(basedir.children))

    def test_only_root_files(self):
        paths = ["C:\\test\\A.jpg",
                 "C:\\test\\B.jpg",
                 "C:\\test\\C.jpg"]
        tree = FilePrefixTree("C:\\test\\", paths)
        basedir = tree.basedir
        self.assertEqual("test", basedir.name)
        self.assertEqual(3, basedir.files)
        self.assertEqual(0, len(basedir.children))

    def test_two_folders(self):
        paths = ["C:\\test\\A\\A.jpg",
                 "C:\\test\\A\\B.jpg",
                 "C:\\test\\B\\C.jpg"]
        tree = FilePrefixTree("C:\\test\\", paths)

        basedir = tree.basedir
        self.assertEqual("test", basedir.name)
        self.assertEqual(0, basedir.files)
        self.assertEqual(2, len(basedir.children))
        a = basedir.children[0]
        self.assertEqual("A", a.name)
        self.assertEqual(0, len(a.children))
        self.assertEqual(2, a.files)

        b = basedir.children[1]
        self.assertEqual(b.name, "B")
        self.assertEqual(len(b.children), 0)
        self.assertEqual(b.files, 1)

    def test_root_and_folders(self):
        paths = ["C:\\test\\foo.jpg",
                 "C:\\test\\A\\B.jpg"]
        tree = FilePrefixTree("C:\\test\\", paths)
        basedir = tree.basedir
        self.assertEqual("test", basedir.name)
        self.assertEqual(1, basedir.files)
        self.assertEqual(1, len(basedir.children))
        a = basedir.children[0]
        self.assertEqual("A", a.name)
        self.assertEqual(0, len(a.children))
        self.assertEqual(1, a.files)

    def test_nested_folders(self):
        paths = ["C:\\test\\D\\A.jpg",
                 "C:\\test\\A\\B\\C\\B.jpg"]
        tree = FilePrefixTree("C:\\test\\", paths)
        basedir = tree.basedir
        self.assertEqual(basedir.name, "test")
        self.assertEqual(basedir.files, 0)
        self.assertEqual(len(basedir.children), 2)
        a = basedir.children[0]
        self.assertEqual(a.name, "A")
        self.assertEqual(len(a.children), 1)
        self.assertEqual(a.files, 0)
        b = a.children[0]
        self.assertEqual(b.name, "B")
        self.assertEqual(len(b.children), 1)
        self.assertEqual(b.files, 0)
        c = b.children[0]
        self.assertEqual(c.name, "C")
        self.assertEqual(len(c.children), 0)
        self.assertEqual(c.files, 1)

    def test_prefix_elimination(self):
        paths = ["C:\\test\\A\\B\\foo.jpg",
                 "C:\\test\\A\\C\\foo.jpg",
                 "C:\\test\\D\\E\\foo.jpg",
                 "C:\\test\\D\\F\\foo.jpg"]
        tree = FilePrefixTree("C:\\test\\", paths)
        basedir = tree.basedir
        self.assertEqual(2, len(basedir.children))
        self.assertEqual(2, len(basedir.children[0].children))
        self.assertEqual(2, len(basedir.children[1].children))

    # TODO test folders that have the same name as disk drives
    # TODO test folders that have the same name as fotos.