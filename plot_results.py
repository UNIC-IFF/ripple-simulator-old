import pandas as pd
import sys
import matplotlib
import matplotlib.pyplot as plt

# fname="./cases_output_test1.csv"
fname="./results/case_N_nodesvsMalnodes_2/cases_output_comb.csv"
if len(sys.argv)>1:
    fname=sys.argv[1]

cols= ['Num_nodes' , 'Num_malicious', 'consensus_percent', 'num_outbound_links', 'max_unl', 'min_unl', 'unl_threshold', 'min_c2c_latency', 'max_c2c_latency', 
        'min_e2c_latency' , 'max_e2c_latency', 'convergence_time','unprocessed_messages', 'total_messages_sent', 'unprocessed_messages ratio' , "noConvergence"]

#load csv
res=pd.read_csv(fname, sep="\t", names=cols, header=None)

# ex 
#   Num_nodes   Num_malicious   consensus_percent   num_outbound_links  max_unl min_unl unl_threshold   min_c2c_latency max_c2c_latency min_e2c_latency max_e2c_latency convergence_time    unprocessed_messages    
#   2000        1200            80                  10                  30      20      10              5               200             5               50              2031                152048                  1712564 0.081544        0       60

#  std::cout << myConfig.Num_Nodes <<"\t"<< myConfig.Num_Malicious << "\t" << myConfig.consensus_percent << "\t" <<  myConfig.Num_Outbound_Links << "\t" << myConfig.Max_UNL << "\t" <<myConfig.Min_UNL << "\t" <<myConfig.UNL_threshold 
            # << "\t" << myConfig.Min_c2c_latency << "\t" << myConfig.Max_c2c_latency << "\t" << myConfig.Min_e2c_latency<< "\t" <<myConfig.Max_e2c_latency
            # << "\t" << network.master_time<< "\t" << mc<< "\t" <<total_messages_sent << "\t"<< isFatal<< std::endl ;

# print(res)
res['unprocessed_messages ratio']=res['unprocessed_messages']/(res['total_messages_sent']+res['unprocessed_messages'])
res['malicious nodes portion']=res['Num_malicious']/res['Num_nodes']

unique_NumNodes=pd.unique(res['Num_nodes'])
N_unique_NumNodes=pd.unique(res['Num_nodes']).shape[0]
#N_cases_per_Nnodes=int(res.shape[0]/N_unique_NumNodes)

unique_malpC=pd.unique(res['malicious nodes portion'])

fig, ax = plt.subplots()
mpC_plot=pd.DataFrame()
mpC_plot['Num_nodes']=unique_NumNodes.sort_values()
for i in range(0,res.shape[0]-1,N_cases_per_Nnodes):
    mpC_plot['convergence_time']=res['Num_nodes']==mpC_plot['Num_nodes']
    ax.plot(res['Num_malicious'][i:i+N_cases_per_Nnodes-1]/res['Num_nodes'][i:i+N_cases_per_Nnodes-1] , res['convergence_time'][i:i+N_cases_per_Nnodes-1], marker=i/N_cases_per_Nnodes,label=str(res['Num_nodes'][i])+' Nodes')
    plt.yscale('symlog', linthrehy=0.001)
    # plt.setp(marker=matplotlib.markers[i])

# ax.plot(res['Num_malicious'][:2]/res['Num_nodes'][:2] , res['convergence_time'][:2], 'b--', label='100 Nodes')
# ax.plot(res['Num_malicious'][3:5]/res['Num_nodes'][3:5] , res['convergence_time'][3:5], 'b:',label='1000 Nodes')
# ax.plot(res['Num_malicious'][6:8]/res['Num_nodes'][6:8] , res['convergence_time'][6:8], 'b', label='2000 Nodes')
ax.set(xlabel='Malicious Nodes portion', ylabel='Convergence time (ms)', title="Convergence time vs Malicious nodes")
ax.grid()
legend=ax.legend(loc='best best', shadow=False, fontsize='medium')
legend.get_frame().set_facecolor('C3')

fig.savefig(fname[:-4]+'malpercentage_1.png')

#plt.show()



#### 
fig, ax = plt.subplots()

for i in range(0,res.shape[0]-1,N_cases_per_Nnodes):
    ax.plot(res['Num_malicious'][i:i+N_cases_per_Nnodes-1]/res['Num_nodes'][i:i+N_cases_per_Nnodes-1],res['unprocessed_messages ratio'][i:i+N_cases_per_Nnodes-1],
        marker=i/N_cases_per_Nnodes, label=str(res['Num_nodes'][i])+' Nodes')

ax.set(xlabel='Malicious Nodes portion', ylabel='Unprocessed messages portion', title='Needless network utilization')
ax.grid()
legend=ax.legend(loc='best',shadow=False, fontsize='small')
legend.get_frame().set_facecolor('C1')

fig.savefig(fname[:-4]+'_unprmsgs-malpC.png')

#plt.show()
