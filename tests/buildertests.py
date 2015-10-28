import random
import unittest
import itertools
from functions import dates, formatters
import writer
import builder as bldr

__author__ = 'tangz'

class ConfigBuilderTest(unittest.TestCase):

    def test_e2e_with_builder(self):
        clustersize = 10
        const = lambda value: value

        builder = bldr.ConfigBuilder()

        builder.newglobalsetting().userepeater(bldr.REPEATER_SINGLE, clustersize).build()

        builder.newcolumn('STRESS_TESTING_SCENARIO_ID').usefunc(const).useargs(0).build()
        builder.newcolumn('TRANCHE_COLLATERAL_TYPE').usefunc(random.choice).useargs(['COLLATERALIZED', 'NON-COLLATERALIZED']).build()
        builder.newcolumn('BS_TYPE').usefunc(const).usekwargs(value='DLO').build()
        builder.newcolumn('K_MATURITY').usefunc(random.uniform).norepeater().usekwargs(a=1, b=5).build()
        builder.newcolumn('LGD').usefunc(random.random).norepeater().build()
        builder.newcolumn('LGD2').usefunc(lambda x: x/2.0).add_named_dependency('LGD', 'x').build()
        # builder.newcolumn('Date').usefunc(dates.quarterlyiter).usekwargs(startdate='01/01/2015').userepeater(bldr.REPEATER_CLUSTER, clustersize).build()

        config = builder.output_config()
        writer.write_csv("../resources/Hope4.csv", config, 100)


    def _total_exposure_func(self, revolving, ending_bal):
        if revolving == 'N':
            return ending_bal
        else:
            return random.randint(70000, 90000)

    def test_copy(self):
        builder = bldr.ConfigBuilder()
        builder.newcolumn('TRANCHE_COLLATERAL_TYPE').usefunc(random.choice).useargs(['A', 'B', 'C', 'D', 'E']).build()
        builder.newcolumn('COPY_COLUMN').copyconfig('TRANCHE_COLLATERAL_TYPE')
        builder.newcolumn('COUNT').usefunc(itertools.count).useargs(1).useformatter(formatters.prepend('Ref_')).userepeater(bldr.REPEATER_SINGLE, 5).build()
        builder.newcolumn('COPY_COUNT').copyconfig('COUNT')
        config = builder.output_config()
        writer.write_csv("../resources/HopeCopy.csv", config, 100)


    def test_e2e_ECL(self):
        clustersize = 30
        num_contractrefs = 100

        builder = bldr.ConfigBuilder()

        builder.newglobalsetting().userepeater(bldr.REPEATER_SINGLE, clustersize).build()

        builder.newcolumn('Date').usefunc(dates.quarters_iter).usekwargs(startyear=2015, startmonth=3)\
            .userepeater(bldr.REPEATER_CLUSTER, clustersize)\
            .useformatter(formatters.dateformatter("%m/%d/%Y")).build()
        builder.newcolumn('Reference Id').usefunc(itertools.count).usekwargs(start=1)\
            .useformatter(formatters.prepend('Ref_')).build()
        builder.newcolumn('Ending Balance').usefunc(random.randint)\
            .useargs(50000, 60000)\
            .norepeater().build()
        builder.newcolumn('Total Exposure').usefunc(self._total_exposure_func)\
            .add_named_dependency('Ending Balance', 'ending_bal')\
            .add_named_dependency('Revolving (Y or N)', 'revolving')\
            .norepeater().build()
        builder.newcolumn('Performing (Y or N)').usefunc(random.choice).useargs(['Y', 'N']).build()
        builder.newcolumn('Revolving (Y or N)').usefunc(random.choice).useargs(['Y', 'N']).build()
        builder.newcolumn('Average Recovery Years').usefunc(random.randint).useargs(1, 9).build()
        builder.newcolumn('Effective Interest Rate').usefunc(random.uniform).useargs(5, 9)\
            .userepeater(bldr.REPEATER_CLUSTER, clustersize)\
            .useformatter(formatters.nround(3)).build()
        builder.newcolumn('LGD Effective rate').usefunc(random.uniform).useargs(1, 2)\
            .norepeater().useformatter(formatters.nround(3)).build()

        config = builder.output_config()
        writer.write_csv("../resources/ECL-100-30quarters2.csv", config, clustersize * num_contractrefs)

