import unittest
from config import TabularConfig, FunctionNode, Dependency
from wrapper import FunctionWrapper
from tests import testdata

__author__ = 'tangz'

class ConfigTests(unittest.TestCase):

    def test_config_without_dependencies(self):
        conf = TabularConfig()
        nodeAA = FunctionNode(FunctionWrapper(testdata.mult), kwargs={'a':1, 'b':2})
        nodeBB = FunctionNode(FunctionWrapper(testdata.counter), kwargs={'start':2, 'inc':1})
        nodeCC = FunctionNode(FunctionWrapper(testdata.mult), args=[3, 4])
        conf.setnode("AA", nodeAA)
        conf.setnode("BB", nodeBB)
        conf.setnode("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.nodefor("AA").getvalue(), 2)
            self.assertEqual(conf.nodefor("BB").getvalue(), i+2)
            self.assertEqual(conf.nodefor("CC").getvalue(), 12)
            conf.resetall()

    def test_config_with_arg_dependencies_all(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB')
        dependencyCC = Dependency('CC')
        nodeAA = FunctionNode(FunctionWrapper(testdata.mult), dependencies=[dependencyBB, dependencyCC])
        nodeBB = FunctionNode(FunctionWrapper(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionWrapper(testdata.mult), args=[3, 4])
        conf.setnode("AA", nodeAA)
        conf.setnode("BB", nodeBB)
        conf.setnode("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.nodefor("AA").getvalue(), 24)
            self.assertEqual(conf.nodefor("BB").getvalue(), 2)
            self.assertEqual(conf.nodefor("CC").getvalue(), 12)
            conf.resetall()

    def test_config_with_kwarg_dependencies_all(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB', 'inc')
        dependencyCC = Dependency('CC', 'start')
        nodeAA = FunctionNode(FunctionWrapper(testdata.counter), dependencies=[dependencyBB, dependencyCC])
        nodeBB = FunctionNode(FunctionWrapper(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionWrapper(testdata.mult), args=[3, 4])
        conf.setnode("AA", nodeAA)
        conf.setnode("BB", nodeBB)
        conf.setnode("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.nodefor("AA").getvalue(), 2*i + 12)
            self.assertEqual(conf.nodefor("BB").getvalue(), 2)
            self.assertEqual(conf.nodefor("CC").getvalue(), 12)
            conf.resetall()

    # Note: a corner case. Almost all cases, users are recommended to not mix args & kwargs.
    def test_config_with_mixed_dependencies_all(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB')
        dependencyCC = Dependency('CC', 'inc')
        nodeAA = FunctionNode(FunctionWrapper(testdata.counter), dependencies=[dependencyBB, dependencyCC])
        nodeBB = FunctionNode(FunctionWrapper(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionWrapper(testdata.mult), args=[3, 4])
        conf.setnode("AA", nodeAA)
        conf.setnode("BB", nodeBB)
        conf.setnode("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.nodefor("AA").getvalue(), 12*i + 2)
            self.assertEqual(conf.nodefor("BB").getvalue(), 2)
            self.assertEqual(conf.nodefor("CC").getvalue(), 12)
            conf.resetall()

    # We recommend users to always use kwargs when dealing with mixed pure and dependent arguments.
    def test_config_with_arg_dependencies_some(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB', 'a')
        nodeAA = FunctionNode(FunctionWrapper(testdata.mult), kwargs={'b': 2}, dependencies=[dependencyBB])
        nodeBB = FunctionNode(FunctionWrapper(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionWrapper(testdata.mult), args=[3, 4])
        conf.setnode("AA", nodeAA)
        conf.setnode("BB", nodeBB)
        conf.setnode("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.nodefor("AA").getvalue(), 4)
            self.assertEqual(conf.nodefor("BB").getvalue(), 2)
            self.assertEqual(conf.nodefor("CC").getvalue(), 12)
            conf.resetall()


    # dependency of A -> B; A -> C; B -> C
    def test_config_with_graph_dependency(self):
        conf = TabularConfig()
        # Column AA
        # A -> B dependency
        dependencyBB_forAA = Dependency('BB', 'a')
        # A -> C dependency
        dependencyCC_forAA = Dependency('CC', 'b')
        nodeAA = FunctionNode(FunctionWrapper(testdata.mult), dependencies=[dependencyBB_forAA, dependencyCC_forAA])

        # Column BB
        dependencyCC_forBB = Dependency('CC', 'b')
        nodeBB = FunctionNode(FunctionWrapper(testdata.mult), kwargs={'a': 2}, dependencies=[dependencyCC_forAA])

        # Column CC
        nodeCC = FunctionNode(FunctionWrapper(testdata.mult), args=[5, 2])

        # add all nodes into tabular config
        conf.setnode("AA", nodeAA)
        conf.setnode("BB", nodeBB)
        conf.setnode("CC", nodeCC)

        self.assertEqual(conf.nodefor("AA").getvalue(), 200)
        self.assertEqual(conf.nodefor("BB").getvalue(), 20)
        self.assertEqual(conf.nodefor("CC").getvalue(), 10)
        conf.resetall()

    # TODO: add tests around Repeater nodes and Formatter nodes
    # TODO implement: check circular dependency
    # TODO: add real builder tests.
