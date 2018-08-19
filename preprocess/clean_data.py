import pandas as pd


# 该py文件的功能是将源数据
# first_step_clean_data方法：
# 1、去除多余列；2、仅仅保留最近n个月的数据；3、只保留至少被m个用户购买过的item。
#
# second_step_clean_data方法：
# 1、去除只含一个item的session；2、对每个用户按时间生成多个session(以一天为一个单位)

class Dataset(object):

    def __init__(self):
        return

    def item_appear(self, appear_time, ds):
        dm = ds[['use_ID', 'ite_ID']].drop_duplicates()
        da = dm.groupby(by=['ite_ID'], as_index=False)['ite_ID'].agg({'cnt': 'count'})
        ite_list = list(da[da['cnt'] >= appear_time]['ite_ID'])
        ds = ds[ds['ite_ID'].isin(ite_list)]
        return ds

    def session_not_single(self, ds):
        ds = ds[ds.duplicated(['use_ID', 'time'], keep=False) == True]
        return ds

    def user_have_more_session(self, ds,user_sessin):
        dm = ds.drop_duplicates(['use_ID', 'time'])
        da = dm.groupby(by=['use_ID'], as_index=False)['use_ID'].agg({'cnt': 'count'})
        use_list = list(da[da['cnt'] >= user_sessin]['use_ID'])
        ds = ds[ds['use_ID'].isin(use_list)]
        return ds

    def first_step_clean_data(self, source_file, months=7, appear_time=20,user_sessin=5):
        data = pd.read_csv(source_file)
        ds = data.drop(['sel_ID', 'cat_ID'], axis=1)
        ds = ds[(ds['act_ID'] == 1) & (ds['time'] > 20150430)]
        ds = ds.drop(['act_ID'], axis=1)
        # 去除重复的数据，如果重复在后面的session中会相同的item
        ds = ds.drop_duplicates()
        ds = ds.sort_values(by=['use_ID', 'time'])

        # 统计每个ite_ID被多少个不同的user购买，只保留被至少appear_time个用户购买过的item
        ds = self.item_appear(appear_time, ds)
        # dm = ds[['use_ID', 'ite_ID']].drop_duplicates()
        # da = dm.groupby(by=['ite_ID'], as_index=False)['ite_ID'].agg({'cnt': 'count'})
        # ite_list = list(da[da['cnt'] >= appear_time]['ite_ID'])
        # ds = ds[ds['ite_ID'].isin(ite_list)]

        # 对每个用户的消费行为，如果一个时间点只有一个item的数据，则去除，即只保留重复数据
        ds = self.session_not_single(ds)
        # ds = ds[ds.duplicated(['use_ID', 'time'], keep=False) == True]

        # 对于每个用户，如果只存在一个session，则去除
        ds = self.user_have_more_session(ds,user_sessin)
        # dm = ds.drop_duplicates(['use_ID', 'time'])
        # da = dm.groupby(by=['use_ID'], as_index=False)['use_ID'].agg({'cnt': 'count'})
        # use_list = list(da[da['cnt'] >= 6]['use_ID'])
        # ds = ds[ds['use_ID'].isin(use_list)]

        # ds = self.item_appear(appear_time, ds)
        ds.to_csv('~/SHAN/data.csv', index=False)


source_file = '~/SHAN/ijcai2016_taobao.csv'
data_file = '~/SHAN/data.csv'
months = 7
appear_time = 20
user_sessin = 5
data = Dataset()
data.first_step_clean_data(source_file, months, appear_time,user_sessin)