import pandas as pd

data_folder = '/Users/benjaminsmith/Documents/computational-modeling/data/'
exp_design = pd.read_csv(data_folder  + 'daquila2012/exp-design.csv')

data_exp_1_raw = pd.read_csv(data_folder + 'daquila2012/exp-1.csv')

data_exp_2_raw = pd.read_csv(data_folder + 'daquila2012/exp-2.csv')


def reshape_experimental_data(exp_df,DoseAmountDict,DoseSubstance):

    exp_df_long=pd.melt(exp_df, id_vars=['Subject','Measure'],var_name='ExposureEvent')
    exp_df_wide=exp_df_long.groupby(['Subject']).apply(lambda d: d.pivot(index='ExposureEvent',columns='Measure',values='value'))
    exp_df_tabular = exp_df_wide.reset_index()

    exp_df_tabular.ExposureEvent = [int(r.replace("Event ", "")) for r in exp_df_tabular.ExposureEvent]
    exp_df_tabular_ordered = exp_df_tabular.sort_values(['Subject','ExposureEvent']).reset_index(drop=True)
    exp_df_tabular_ordered_alldata = pd.merge(exp_df_tabular_ordered, exp_design, how='left', on='ExposureEvent')
    concentration_dict = {1: (0.9 / 100), 2: (2.70 / 100)}
    exp_df_tabular_ordered_alldata['ConcentrationAmount']= [concentration_dict[c] for c in exp_df_tabular_ordered_alldata.Concentration]
    exp_df_tabular_ordered_alldata['DoseAmount']= [DoseAmountDict[c] for c in
                                                          exp_df_tabular_ordered_alldata.DoseType]

    depletion_dict = {1:'Na replete',2:'Na depleted'}
    exp_df_tabular_ordered_alldata['DepletionDescription']= [depletion_dict[c] for c in exp_df_tabular_ordered_alldata.loc[:,"Depletion status"]]
    exp_df_tabular_ordered_alldata['DoseSubstance']=DoseSubstance
    return exp_df_tabular_ordered_alldata

data_exp_1 = reshape_experimental_data(data_exp_1_raw,{1:0,2:10,3:20,4:40},DoseSubstance='SCH 23390')
data_exp_2 = reshape_experimental_data(data_exp_2_raw,{1:0,2:25,3:125,4:250},DoseSubstance='Raclopride')


#data_exp_2.to_csv(data_folder + "myout.csv")

