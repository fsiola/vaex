import vaex

from benchmarks.fixtures import generate_numerical

class GroupBySetup:
    pretty_name = "Groupby benchmarks - H2O inspired"
    version = "1"

    params = ([10**7, 5*10**7, 10**8],)
    param_names = ['N']

    def setup_cache(self):
        # ensure the dataframe is generated
        generate_numerical()

    def setup(self, N):
        self.df = vaex.open(generate_numerical())[:N]
        self.df.categorize(self.df.i8_10, min_value=5, max_value=14, inplace=True)
        self.df.categorize(self.df.i4_10, min_value=5, max_value=14, inplace=True)
        self.df.categorize(self.df.i2_10, min_value=5, max_value=14, inplace=True)
        self.df.categorize(self.df.i1_10, min_value=5, max_value=14, inplace=True)

        self.df.categorize(self.df.i8_1K, min_value=5, inplace=True)
        self.df.categorize(self.df.i4_1K, min_value=5, inplace=True)
        self.df.categorize(self.df.i2_1K, min_value=5, inplace=True)

        self.df.categorize(self.df.i8_1M, min_value=5, inplace=True)
        self.df.categorize(self.df.i4_1M, min_value=5, inplace=True)


class Groupby(GroupBySetup):
    def time_question_1(self, N):
        self.df.groupby(['i1']).agg({'x': 'sum'})

    def time_question_2(self, N):
        self.df.groupby(['i1', 'i2']).agg({'x': 'sum'})

    def time_question_3(self, N):
        self.df.groupby(['i4_1M']).agg({'x': 'sum', 'y': 'mean'})

    def time_question_4(self, N):
        self.df.groupby(['i1']).agg({'x':'mean', 'y':'mean', 'x4':'mean'})

    def time_question_5(self, N):
        self.df.groupby(['i4_1M']).agg({'x': 'sum', 'y': 'sum', 'x4': 'sum'})

    # def time_question_6(self, N):
    #     self.df.groupby(['i4_10','i4_1K']).agg({'x': ['median','std']})

    def time_question_7(self, N):
        group_df = self.df.groupby(['i4_1M']).agg({'x': 'max', 'y': 'min'})
        result = group_df['range_x_y'] = group_df['x'] = group_df['y']

    def time_question_8(self, N):
        self.df[['i4_1M','x']].sort('i4_1M', ascending=False).groupby(['i4_1M'])

    # def time_question_9(self.N):
    #     Not implemented yet

    def time_question_10(self, N):
        self.df.groupby(['i1', 'i2', 'i1_10', 'i2_10', 'i2_1K', 'i4_10', 'i4_1K', 'i4_1M']).agg({'x':'sum', 'y':'count'})