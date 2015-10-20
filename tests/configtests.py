import unittest
from config import TabularConfig, FunctionNode, Dependency
from settings import FunctionSetting
from tests import testdata

__author__ = 'tangz'

class ConfigTests(unittest.TestCase):

    def test_config_without_dependencies(self):
        conf = TabularConfig()
        nodeAA = FunctionNode(FunctionSetting(testdata.mult), kwargs={'a':1, 'b':2})
        nodeBB = FunctionNode(FunctionSetting(testdata.counter), kwargs={'start':2, 'inc':1})
        nodeCC = FunctionNode(FunctionSetting(testdata.mult), args=[3, 4])
        conf.set("AA", nodeAA)
        conf.set("BB", nodeBB)
        conf.set("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.get("AA").getvalue(), 2)
            self.assertEqual(conf.get("BB").getvalue(), i+2)
            self.assertEqual(conf.get("CC").getvalue(), 12)

    def test_config_with_arg_dependencies_all(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB')
        dependencyCC = Dependency('CC')
        nodeAA = FunctionNode(FunctionSetting(testdata.mult), dependencies=[dependencyBB, dependencyCC])
        nodeBB = FunctionNode(FunctionSetting(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionSetting(testdata.mult), args=[3, 4])
        conf.set("AA", nodeAA)
        conf.set("BB", nodeBB)
        conf.set("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.get("AA").getvalue(), 24)
            self.assertEqual(conf.get("BB").getvalue(), 2)
            self.assertEqual(conf.get("CC").getvalue(), 12)

    def test_config_with_kwarg_dependencies_all(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB', 'inc')
        dependencyCC = Dependency('CC', 'start')
        nodeAA = FunctionNode(FunctionSetting(testdata.counter), dependencies=[dependencyBB, dependencyCC])
        nodeBB = FunctionNode(FunctionSetting(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionSetting(testdata.mult), args=[3, 4])
        conf.set("AA", nodeAA)
        conf.set("BB", nodeBB)
        conf.set("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.get("AA").getvalue(), 2*i + 12)
            self.assertEqual(conf.get("BB").getvalue(), 2)
            self.assertEqual(conf.get("CC").getvalue(), 12)

    # Note: a corner case. Almost all cases, users are recommended to not mix args & kwargs.
    def test_config_with_mixed_dependencies_all(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB')
        dependencyCC = Dependency('CC', 'inc')
        nodeAA = FunctionNode(FunctionSetting(testdata.counter), dependencies=[dependencyBB, dependencyCC])
        nodeBB = FunctionNode(FunctionSetting(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionSetting(testdata.mult), args=[3, 4])
        conf.set("AA", nodeAA)
        conf.set("BB", nodeBB)
        conf.set("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.get("AA").getvalue(), 12*i + 2)
            self.assertEqual(conf.get("BB").getvalue(), 2)
            self.assertEqual(conf.get("CC").getvalue(), 12)

    # We recommend users to always use kwargs when dealing with mixed pure and dependent arguments.
    def test_config_with_arg_dependencies_some(self):
        conf = TabularConfig()

        dependencyBB = Dependency('BB', 'a')
        nodeAA = FunctionNode(FunctionSetting(testdata.mult), kwargs={'b':2}, dependencies=[dependencyBB])
        nodeBB = FunctionNode(FunctionSetting(testdata.mult), args=[1, 2])
        nodeCC = FunctionNode(FunctionSetting(testdata.mult), args=[3, 4])
        conf.set("AA", nodeAA)
        conf.set("BB", nodeBB)
        conf.set("CC", nodeCC)

        for i in range(5):
            self.assertEqual(conf.get("AA").getvalue(), 4)
            self.assertEqual(conf.get("BB").getvalue(), 2)
            self.assertEqual(conf.get("CC").getvalue(), 12)

    # TODO: (1) test reset; (2) test A -> B; A -> C; B -> C
    # TODO implement: check circular dependency
