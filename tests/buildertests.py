import unittest
import builder as bldr
from config import FunctionNode, Dependency
from functions import formatters
from wrapper import FunctionWrapper, SingleRepeater, ClusterRepeater, FormatWrapper

__author__ = 'tangz'


class ConfigBuilderTest(unittest.TestCase):

    def test_build_basic_function_with_no_args(self):
        column = 'Test Column'
        builder = bldr.ConfigBuilder()
        fn = lambda: 3
        builder.newcolumn(column).usefunc(fn).build()

        config = builder.output_config()
        built_node = config.nodefor(column)

        expected_node = FunctionNode(FunctionWrapper(fn))
        expected_node.col_funcnode_map = config
        self.assertEqual(built_node, expected_node)

    def test_build_basic_function_with_args(self):
        column = 'Test Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x: x
        builder.newcolumn(column).usefunc(fn).useargs(1).build()

        config = builder.output_config()
        built_node = config.nodefor(column)

        expected_node = FunctionNode(FunctionWrapper(fn), args=[1])
        expected_node.col_funcnode_map = config
        self.assertEqual(built_node, expected_node)

    def test_build_basic_function_with_kwargs(self):
        column = 'Test Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x: x
        builder.newcolumn(column).usefunc(fn).usekwargs(x=1).build()

        config = builder.output_config()
        built_node = config.nodefor(column)

        expected_node = FunctionNode(FunctionWrapper(fn), kwargs={'x': 1})
        expected_node.col_funcnode_map = config
        self.assertEqual(built_node, expected_node)

    def test_build_function_withargs_notequal_withkwargs(self):
        column = 'Test Column'
        fn = lambda x: x

        builder = bldr.ConfigBuilder()
        builder.newcolumn(column).usefunc(fn).useargs(1).build()
        config = builder.output_config()
        built_node1 = config.nodefor(column)

        builder2 = bldr.ConfigBuilder()
        builder2.newcolumn(column).usefunc(fn).usekwargs(x=1).build()
        built_node2 = builder2.output_config().nodefor(column)

        built_node1.col_funcnode_map = config
        built_node2.col_funcnode_map = config

        self.assertNotEqual(built_node1, built_node2)

    def test_build_function_with_one_dependency(self):
        column1 = 'Test Column'
        column2 = 'Dependency Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x: x
        builder.newcolumn(column1).usefunc(fn).add_dependency(column2).build()
        builder.newcolumn(column2).usefunc(fn).useargs(1).build()

        config = builder.output_config()
        built_node = config.nodefor(column1)

        expected_node1 = FunctionNode(FunctionWrapper(fn), dependencies=[Dependency(column2)])
        expected_node1.col_funcnode_map = config
        self.assertEqual(built_node, expected_node1)

    def test_build_function_with_dependency_arg_kwarg_mix(self):
        column1 = 'Test Column'
        column2 = 'Dependency Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x, y, z: x + y + z
        const = lambda x: x
        builder.newcolumn(column1).usefunc(fn).add_dependency(column2).useargs(3).usekwargs(y=2).build()
        builder.newcolumn(column2).usefunc(const).useargs(1).build()

        config = builder.output_config()
        built_node = config.nodefor(column1)

        expected_node1 = FunctionNode(FunctionWrapper(fn), dependencies=[Dependency(column2)], args=[3], kwargs={'y': 2})
        expected_node1.col_funcnode_map = config
        self.assertEqual(built_node, expected_node1)

    def test_build_function_with_multiple_dependencies(self):
        column1 = 'Test Column'
        column2 = 'Dependency Column 1'
        column3 = 'Dependency Column 2'
        builder = bldr.ConfigBuilder()
        fn = lambda x, y: x + y
        const = lambda x: x
        builder.newcolumn(column1).usefunc(fn).add_named_dependency(column2, 'x')\
            .add_named_dependency(column3, 'y').build()
        builder.newcolumn(column2).usefunc(const).useargs(1).build()
        builder.newcolumn(column3).usefunc(const).useargs(2).build()

        config = builder.output_config()
        built_node = config.nodefor(column1)

        expected_node1 = FunctionNode(FunctionWrapper(fn), dependencies=[Dependency(column2, 'x'),
                                                                         Dependency(column3, 'y')])
        expected_node1.col_funcnode_map = config
        self.assertEqual(built_node, expected_node1)

    def test_build_function_with_single_repeater(self):
        column = 'Test Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x: x
        builder.newcolumn(column).usefunc(fn).useargs(1).userepeater(bldr.REPEATER_SINGLE, 5).build()

        config = builder.output_config()
        built_node = config.nodefor(column)

        expected_node = FunctionNode(SingleRepeater(FunctionWrapper(fn), 5), args=[1])
        expected_node.col_funcnode_map = config
        self.assertEqual(built_node, expected_node)

    def test_build_function_with_cluster_repeater(self):
        column = 'Test Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x: x
        builder.newcolumn(column).usefunc(fn).useargs(1).userepeater(bldr.REPEATER_CLUSTER, 5).build()

        config = builder.output_config()
        built_node = config.nodefor(column)

        expected_node = FunctionNode(ClusterRepeater(FunctionWrapper(fn), 5), args=[1])
        expected_node.col_funcnode_map = config
        self.assertEqual(built_node, expected_node)

    def test_build_function_with_formatter(self):
        column = 'Test Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x: x
        formatter = formatters.prepend("Ref_")
        builder.newcolumn(column).usefunc(fn).useargs(1).useformatter(formatter).build()

        config = builder.output_config()
        built_node = config.nodefor(column)

        expected_node = FunctionNode(FormatWrapper(FunctionWrapper(fn), formatter), args=[1])
        expected_node.col_funcnode_map = config
        self.assertEqual(built_node, expected_node)

    def test_build_function_with_formatter_and_repeater(self):
        column = 'Test Column'
        builder = bldr.ConfigBuilder()
        fn = lambda x: x
        formatter = formatters.prepend("Ref_")
        builder.newcolumn(column).usefunc(fn).useargs(1).useformatter(formatter).userepeater(bldr.REPEATER_SINGLE,
                                                                                             5).build()

        config = builder.output_config()
        built_node = config.nodefor(column)

        expected_node = FunctionNode(SingleRepeater(FormatWrapper(FunctionWrapper(fn), formatter), 5), args=[1])
        expected_node.col_funcnode_map = config
        self.assertEqual(built_node, expected_node)

