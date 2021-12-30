import unittest
import fp_growth
import psutil
import os

class Tester(object):
    def __init__(self, case, node):
        self.case = case
        self.node = node

    def child(self, p, count=None):
        c = self.node.search(p)
        self.case.failIf(c is None, 'No child with item %s' % p)

        test = Tester(self.case, c)
        if count is not None:
            test.count(count)
        return test

    def leaf(self):
        self.case.assertTrue(self.node.leaf, 'Node must be a leaf')
        return self


    def count(self, count):
        self.case.assertEqual(self.node.count, count,
            'expected count to be %d; instead it was %d' %
            (count, self.node.count))
        return self




class TestCaseTree(unittest.TestCase):
    def setUp(self):
        self.tree = fp_growth.Frequency_Pattern_Tree()
        self.root = Tester(self, self.tree.root)

    def assertPathsEqual(self, expected, actual):
        actual = list(actual)
        self.assertEqual(len(expected), len(actual))

        for items, path in zip(expected, actual):
            self.assertEqual(len(items), len(path))
            for item, node in zip(items, path):
                self.assertEqual(item, node.item)


    def nodes(self, item):
        return list(self.tree.nodes(item))



class TestsInsertion(TestCaseTree):

    def testCommonPrefix(self):
        self.tree.add('abcd')
        self.tree.add('abde')

        b = self.root.child('a', 2).child('b', 2)
        b.child('c', 1).child('d', 1)
        b.child('d', 1).child('e', 1)


    def testOneBranch(self):
        self.tree.add('abc')
        self.root.child('a', 1).child('b', 1).child('c', 1)



    def testNumeric(self):
        self.tree.add([1,2,3])
        self.tree.add([1,2,4])
        self.root.child(1,2).child(2,2).child(3,1)
        self.root.child(1,2).child(2,2).child(4,1)


    def testIndependentBranches(self):
        self.tree.add('abc')
        self.tree.add('def')

        self.root.child('a', 1).child('b', 1).child('c', 1)
        self.root.child('d', 1).child('e', 1).child('f', 1)




class TestsRoute(TestCaseTree):

    def testNeighbors(self):
        self.tree.add('abc')
        self.tree.add('bcd')
        self.tree.add('cde')

        left_c = self.root.child('a').child('b').child('c').node
        middle_c = self.root.child('b').child('c').node
        right_c = self.root.child('c').node

        self.assertTrue(left_c.neighbor is middle_c)
        self.assertTrue(middle_c.neighbor is right_c)


    def testRoutes(self):
        self.tree.add('abc')
        self.tree.add('bcd')
        self.tree.add('cde')

        self.assertEqual(1, len(self.nodes('a')))
        self.assertEqual(2, len(self.nodes('b')))
        self.assertEqual(3, len(self.nodes('c')))
        self.assertEqual(2, len(self.nodes('d')))
        self.assertEqual(1, len(self.nodes('e')))


class TestsPrefixPath(TestCaseTree):
    def testPaths(self):
        self.tree.add('abc')
        self.tree.add('bcd')
        self.tree.add('cde')

        self.assertPathsEqual(['abc', 'bc', 'c'], self.tree.prefix_paths('c'))


class ConditionalTreeTests(TestCaseTree):

    def testPruning(self):
        self.tree.add('abc')
        self.tree.add('abd')
        self.tree.add('ac')
        self.tree.add('abe')
        self.tree.add('dc')

        paths = list(self.tree.prefix_paths('c'))
        ct = fp_growth.conditional_tree_from_paths(paths)
        root = Tester(self, ct.root)
        root.child('a', 2).child('b',1).child('c',1).leaf()
        self.assertEqual(2, len(root.node.children))

    def testSupport(self):
        """
        Issue #2: incorrect support calculation for shared paths
        """
        self.tree.add('abcd')
        self.tree.add('abd')
        paths = list(self.tree.prefix_paths('d'))
        ct = fp_growth.conditional_tree_from_paths(paths)
        root = Tester(self, ct.root)
        a = root.child('a', 2)
        b = a.child('b', 2)
        c = b.child('c', 1)

    def testGeneration(self):
        self.tree.add('abc')
        self.tree.add('abd')
        self.tree.add('ade')

        b = self.root.child('a', 3).child('b', 2)
        b.child('c', 1)
        b.child('d', 1)
        self.root.child('a').child('d', 1).child('e', 1)

        paths = list(self.tree.prefix_paths('d'))
        ct = fp_growth.conditional_tree_from_paths(paths)
        root = Tester(self, ct.root)

        a = root.child('a', 2)
        a.child('b', 1).child('d',1).leaf()
        self.assertEqual(2, len(a.node.children))





class SetTestFrequent(unittest.TestCase):
    def testDuplicate(self):
        raw = '25,52,274;71;71,274;52;25,52;274,71'
        transactions = [line.split(',') for line in raw.split(';')]
        import time
        start_time = time.time()
        itemsets = list(fp_growth.find_frequent_itemsets(transactions, 2))
        print("-----%s seconds--------" % (time.time() - start_time))

        self.assertEqual([['25'], ['52'], ['25', '52'], ['274'], ['71']], itemsets)


if __name__ == '__main__':
    p1 = psutil.Process(os.getpid())
    print('Total Bytes Used:', end='')
    print(p1.memory_info().rss)

    unittest.main()
