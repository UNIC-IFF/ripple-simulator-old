import pandas as pd
import sys
import matplotlib
import matplotlib.pyplot as plt

# fname="./cases_output_test1.csv"
fname="./cases_output.csv"
if len(sys.argv)>1:
    fname=sys.argv[1]

cols= ['Num_nodes' , 'Num_malicious', 'consencus_percent', 'num_outbound_links', 'max_unl', 'min_unl', 'unl_threshold', 'min_c2c_latency', 'max_c2c_latency', 'min_e2c_latency' , 'max_e2c_latency', 'convergence_time',  'unprocessed_messages', 'total_messages_sent', "noConvergence"]

#load csv
res=pd.read_csv(fname, sep="\t", names=cols)

#  std::cout << myConfig.Num_Nodes <<"\t"<< myConfig.Num_Malicious << "\t" << myConfig.consensus_percent << "\t" <<  myConfig.Num_Outbound_Links << "\t" << myConfig.Max_UNL << "\t" <<myConfig.Min_UNL << "\t" <<myConfig.UNL_threshold 
            # << "\t" << myConfig.Min_c2c_latency << "\t" << myConfig.Max_c2c_latency << "\t" << myConfig.Min_e2c_latency<< "\t" <<myConfig.Max_e2c_latency
            # << "\t" << network.master_time<< "\t" << mc<< "\t" <<total_messages_sent << "\t"<< isFatal<< std::endl ;

# print(res)


fig, ax = plt.subplots()

ax.plot(res['Num_malicious'][:2]/res['Num_nodes'][:2] , res['convergence_time'][:2], 'b--', label='100 Nodes')
ax.plot(res['Num_malicious'][3:5]/res['Num_nodes'][3:5] , res['convergence_time'][3:5], 'b:',label='1000 Nodes')
ax.plot(res['Num_malicious'][6:8]/res['Num_nodes'][6:8] , res['convergence_time'][6:8], 'b', label='2000 Nodes')
ax.set(xlabel='Malicious Nodes portion', ylabel='Convergence time (ms)', title="Convergence time vs Malicious nodes")
ax.grid()
legend=ax.legend(loc='center center', shadow=False, fontsize='medium')
legend.get_frame().set_facecolor('C3')

fig.savefig(fname[:-4]+'.png')

#plt.show()



