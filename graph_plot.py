import pydot
import pandas as pd
import numpy as np
import json

# the filename of json topology
net_filename='./results/case_wGraph/net_graph_out_tiny.topo'

net_file=open(net_filename)

net_json=json.load(net_file)

# Network in the file is described as an array of Nodes
# each Node, has an id, UNL, messages_sent, messages_received,links, isMalicious,
#each link has
print(net_json['Network'][0].keys())

print(net_json['Network'][0]['links'][0].keys())

links_colnames=['from_node', 'from_ismalicious', 'to_node', 'to_ismalicious', 'num_messages', 'link_latency']
nodes_colnames=['id', 'ismalicious', 'messages_sent', 'messages_received','UNL','is_inUNL','msgs_to_malicious', 'msgs_to_honest','msgs_from_malicious', 'msgs_from_honest','malicious_in_UNL']


print("Creating dataframes")

links_df=pd.DataFrame(columns=links_colnames)
nodes_df=pd.DataFrame(columns=nodes_colnames)

for n in net_json['Network']:
    nodes_df=nodes_df.append({'id':n['id'], 'ismalicious':n['isMalicious'] , 'messages_sent': n['messages_sent'] ,
                              'messages_received':n['messages_received'],'UNL':n['UNL'], 'is_inUNL':[],
                              'msgs_to_malicious':0, 'msgs_to_honest':0, 'msgs_from_malicious':0, 'msgs_from_honest':0,'malicious_in_UNL':0}, ignore_index=True)
    for l in n['links']:
        links_df=links_df.append({'from_node':n['id'],'from_ismalicious':n['isMalicious'], 'to_node':l['to_node'],'to_ismalicious':False,
                         'num_messages':l['messages_sent'],'link_latency':l['total_latency']},ignore_index=True)



# fill in 'to_ismalicious' field

for l in links_df.iterrows():
    tmp=nodes_df[nodes_df['id']==l[1]['to_node']]
    l[1]['to_ismalicious']=tmp['ismalicious'].values[0]



# fill in 'is_inUNL' field

for n in nodes_df.iterrows():
    n1list=[]
    for n2 in nodes_df.iterrows():
        if n[1]['id'] in n2[1]['UNL']:
            n1list.append(n2[1]['id'])
    n[1]['is_inUNL']=n1list


# count malicious nodes in UNLs
for node in nodes_df.iterrows():
    tmp1=nodes_df.loc[(nodes_df['id'].isin(node[1]['UNL']))]
    node[1]['malicious_in_UNL']=tmp1['ismalicious'].sum()

print( links_df.shape)

print(nodes_df.shape)

# print("Creating graph of topology")
# #initialize graph
# net_graph=pydot.Dot(graph_name="Nodes Network Topology",graph_type="digraph")
#
# for node in nodes_df.iterrows():
#     gnode=None
#     if node[1]['ismalicious']:
#         gnode=pydot.Node(node[1]['id'],style="filled",fillcolor="red")
#     else:
#         gnode = pydot.Node(node[1]['id'], style="filled", fillcolor="green")
#     net_graph.add_node(gnode)
#
# for link in links_df.iterrows():
#     ledge=pydot.Edge(link[1]['from_node'], link[1]['to_node'],style="normal",color="black")
#     net_graph.add_edge(ledge)
#
# for node in nodes_df.iterrows():
#     for unl in node[1]['UNL']:
#         unledge=pydot.Edge(unl,node[1]['id'],style="normal",color="blue")
#         net_graph.add_edge(unledge)
#
# net_graph.write_png(net_filename[:-4]+".png")

print ("Extracting statistics....")

# statistics to get extracted....
# 1) number of msgs from malicious  vs number of messages from honest  to malicious nodes
# 2) number of msgs from malicious  vs number of messages from honest  to honest nodes
# 3) number of msgs to malicious vs number of messages to honest on malicious nodes
# 4) number of msgs to malicious vs number of messages to honest on honest nodes


for node in nodes_df.iterrows():
    tmp1=links_df.loc[((links_df['from_node']==node[1]['id']) & (links_df['to_ismalicious']==True))]
    for link in tmp1.iterrows():
        node[1]['msgs_to_malicious']+=link[1]['num_messages']

    tmp2 = links_df.loc[((links_df['from_node'] == node[1]['id']) & (links_df['to_ismalicious'] == False))]
    for link in tmp2.iterrows():
        node[1]['msgs_to_honest'] += link[1]['num_messages']

    tmp3 = links_df.loc[((links_df['to_node'] == node[1]['id']) & (links_df['from_ismalicious'] == True))]
    for link in tmp3.iterrows():
        node[1]['msgs_from_malicious'] += link[1]['num_messages']

    tmp4 = links_df.loc[((links_df['to_node'] == node[1]['id']) & (links_df['from_ismalicious'] == False))]
    for link in tmp4.iterrows():
        node[1]['msgs_from_honest'] += link[1]['num_messages']



nodes_df.to_csv(net_filename[:-5]+'_nodes.csv',sep='\t')
links_df.to_csv(net_filename[:-5]+'_links.csv',sep='\t')


