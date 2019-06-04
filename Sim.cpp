//------------------------------------------------------------------------------
/*
    This file is part of consensus-sim
    Copyright (c) 2013, Ripple Labs Inc.

    Permission to use, copy, modify, and/or distribute this software for any
    purpose  with  or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE  SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH  REGARD  TO  THIS  SOFTWARE  INCLUDING  ALL  IMPLIED  WARRANTIES  OF
    MERCHANTABILITY  AND  FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY  SPECIAL ,  DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER  RESULTING  FROM  LOSS  OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION  OF  CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/
//==============================================================================

// #include <fstream>
#include <iostream>
#include <random>

#include "Core.h"

#include "config.hpp"

// #include <boost/program_options/cmdline.hpp>
#include <boost/program_options.hpp>
// #include <boost/program_options/variables_map.hpp>
// #include <boost/program_options/options_description.hpp>


namespace po= boost::program_options ;

static SimulatorConfiguration myConfig;

int nodes_positive=0, nodes_negative=0;

void Node::receiveMessage(const Message& m, Network& network)
{
    ++messages_received;

    // If we were going to send any of this data to that node, skip it
    for (Link& link : links)
    {
        if ((link.to_node == m.from_node) && (link.lm_send_time >= network.master_time))
        {
            // We can still update a waiting outbound message
            link.lm -> subPositions(m.data);
            break;
        }
    }

    // 1) Update our knowledge
    std::map<int, NodeState> changes;

    for (std::map<int, NodeState>::const_iterator change_it = m.data.begin();
        change_it != m.data.end(); ++change_it)
    {
        if ( (change_it->first != n) && (knowledge[change_it->first] != change_it->second.state) &&
                (change_it->second.ts > nts[change_it->first]) )
        {
            // This gives us new information about a node
            knowledge[change_it->first] = change_it->second.state;
            nts[change_it->first] = change_it->second.ts;
            changes.insert(std::make_pair(change_it->first, change_it->second));
        }
    }

    if (changes.empty()) return; // nothing changed

    // 2) Choose our position change, if any
    int unl_count = 0, unl_balance = 0;
    for (int node : unl)
    {
        if (knowledge[node] == 1)
        {
            ++unl_count;
            ++unl_balance;
        }
        if (knowledge[node] == -1)
        {
            ++unl_count;
            --unl_balance;
        }
    }

    if (this->isMalicious) // if we are a malicious node, be contrarian
        unl_balance = -unl_balance;

    // add a bias in favor of 'no' as time passes
    // (agree to disagree)
    unl_balance -= network.master_time / 250;

    bool pos_change=false;
    if (unl_count >= myConfig.UNL_threshold)
    { // We have enough data to make decisions
        if ( (knowledge[n] == 1) && (unl_balance < (-myConfig.Self_Weight)) )
        {
            // we switch to -
            knowledge[n] = -1;
            --nodes_positive;
            ++nodes_negative;
            changes.insert(std::make_pair(n, NodeState(n, ++nts[n], -1)));
            pos_change=true;
        }
        else if ( (knowledge[n] == -1) && (unl_balance > myConfig.Self_Weight) )
        {
            // we switch to +
            knowledge[n] = 1;
            ++nodes_positive;
            --nodes_negative;
            changes.insert(std::make_pair(n, NodeState(n, ++nts[n], +1)));
            pos_change=true;
        }
    }

    // 3) Broadcast the message
    for (Link& link : links)
    {
        if (pos_change || (link.to_node != m.from_node))
        {
            // can we update an unsent message?
            if (link.lm_send_time > network.master_time)
                link.lm->addPositions(changes);
            else
            {
                // No, we need a new mesage
                int send_time = network.master_time;
                if (!pos_change)
                {
                    // delay the messag a bit to permit coalescing and suppression
                    send_time += myConfig.Base_Delay;
                    if (link.lm_recv_time > send_time) // a packet is on the wire
                        send_time += link.total_latency / myConfig.Packets_on_Wire; // wait a bit extra to send
                }
                network.sendMessage(Message(n, link.to_node, changes), link, send_time);
                messages_sent++;
            }
        }
    }
}

int main(int argc, char * argv[])
{
    // std::string desc = "Ripple simulator";
    // Declare the supported options.
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "produce help message")
        ("num_nodes", po::value<int>(&myConfig.Num_Nodes), "set number of nodes")
        ("mal_nodes_pC", po::value<float>(&myConfig.malicious_nodes_percentage),"set percentange of num_nodes to be malicious ")
        ("num_malicious", po::value<int>(&myConfig.Num_Malicious), "set number of malicious nodes")
        ("max_e2c_latency", po::value<int>(&myConfig.Max_e2c_latency), "set max end to core latency")
        ("min_e2c_latency", po::value<int>(&myConfig.Min_e2c_latency), "set min end to core latency")
        ("max_c2c_latency", po::value<int>(&myConfig.Max_c2c_latency), "set max core to core latency")
        ("min_c2c_latency", po::value<int>(&myConfig.Min_c2c_latency), "set min core to core latency")
        ("consensus_percent", po::value<int>(&myConfig.consensus_percent), "set percentance for consensus")
        ("num_outbound_links", po::value<int>(&myConfig.Num_Outbound_Links), "set number of outbound links per node")
        ("max_unl", po::value<int>(&myConfig.Max_UNL), "set max Unique Node list size per node")
        ("min_unl", po::value<int>(&myConfig.Min_UNL), "set min Unique Node list size per node")
        ("unl_threshold", po::value<int>(&myConfig.UNL_threshold), "sets threshold for changing node's position")
        ("overlappingUNLs", po::value<float>(&myConfig.overlappingUNLs),"force to use the first overlappingUNLs*MAX_UNL nodes in all UNLs. \n It sets MIN_UNL=max(min_unl,overlappingUNLs*MAX_UNL nodes) ")
        ("base_delay", po::value<int>(&myConfig.Base_Delay), "Base_Delay")
        ("self_weight", po::value<int>(&myConfig.Self_Weight), "Self_Weight")
        ("packets_on_wire", po::value<int>(&myConfig.Packets_on_Wire), "packets on wire")
        ("config_file", po::value<std::string>(), "load from configuration file")

    ;

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);    

    if (vm.count("help")) {
        std::cout << desc << "\n";
        return 1;
    }

    if (vm.count("mal_nodes_pC")){
        myConfig.Num_Malicious=myConfig.Num_Nodes * vm["mal_nodes_pC"].as<float>() /100 ;
    }
    else{
        myConfig.malicious_nodes_percentage=100*myConfig.Num_Malicious/myConfig.Num_Nodes;
    }

    if ((vm.count("min_unl")) && (vm.count("unl_threshold")==0 ))
    {
        myConfig.UNL_threshold=vm["min_unl"].as<int>()/2;
    }

    if (vm.count("overlappingUNLs")){
        int nval= myConfig.overlappingUNLs*myConfig.Max_UNL;
        if (myConfig.Min_UNL< nval)
        {
            myConfig.Min_UNL=nval;
            if (vm.count("unl_threshold")==0)
                myConfig.UNL_threshold=myConfig.Min_UNL/2;
        }
    }

    if (vm.count("config_file")) {
        std::cerr << "Using config file : " << vm["config_file"].as<std::string>() << std::endl;
        myConfig.read_configFile(vm["config_file"].as<std::string>()); 
    
    } 

    // // getting the configuration parameters
    // if (argc != 2){
    //     // using defaults
    //     std::cerr << "Using default settings" << std::endl 
    //         << " To load configurations use: " << argv[0] << " <config_filename>" << std::endl;
    // }
    // else {
    //     std::cerr << "Using config file : " << argv[1] << std::endl;
    //     myConfig.read_configFile(argv[1]);
    // }




    std::cerr << "Running simulator for : \n\t "<< myConfig.Num_Nodes << " Nodes, " << myConfig.Num_Malicious << " of them are MALICIOUS, and CONSENSUS PERCENT " << myConfig.consensus_percent 
            << "\n \t NUM_OUTBOUND_LINKS per Node : " <<  myConfig.Num_Outbound_Links
            << "\n \tNum of UNL nodes per node follows Uniform(" << myConfig.Min_UNL << "," <<myConfig.Max_UNL << ") and the threshold to change position is " <<myConfig.UNL_threshold 
            << "\n \t with overlapping UNLs percentange "<< myConfig.overlappingUNLs*100 <<"% "
            << "\n \tNetwork latency between core nodes follows Uniform (" << myConfig.Min_c2c_latency << "," << myConfig.Max_c2c_latency << ") " 
            << "\n \tNetwork latency between end nodes and core nodes follows Uniform ("<<myConfig.Min_e2c_latency<< "," <<myConfig.Max_e2c_latency << ")"
            << std::endl ;

    // This will produce the same results each time
    std::mt19937 gen;
    std::uniform_int_distribution<> r_e2c(myConfig.Min_e2c_latency, myConfig.Max_e2c_latency);
    std::uniform_int_distribution<> r_c2c(myConfig.Min_c2c_latency, myConfig.Max_c2c_latency);
    std::uniform_int_distribution<> r_unl(myConfig.Min_UNL, myConfig.Max_UNL);
    std::uniform_int_distribution<> r_node(0, myConfig.Num_Nodes-1);

    // Node* nodes[myConfig.Num_Nodes];
    // Node nodes= new Node[myConfig.Num_Nodes];
    std::vector<Node*> nodes;
    // create nodes
    std::cerr << "Creating nodes" << std::endl;
    for (int i = 0; i < myConfig.Num_Nodes; ++i)
    {
        // nodes[i] = new Node(i, myConfig.Num_Nodes);
        nodes.push_back(new Node(i,myConfig.Num_Nodes));
        nodes[i]->e2c_latency = r_e2c(gen);

        // our own position starts as 50/50 split
        if (i%2)
        {
            nodes[i]->knowledge[i] = 1;
            nodes[i]->nts[i] = 1;
            ++nodes_positive;
        }
        else
        {
            nodes[i]->knowledge[i] = -1;
            nodes[i]->nts[i] = 1;
            ++nodes_negative;
        }

        // Build our UNL
        int unl_count = r_unl(gen);
        if (myConfig.overlappingUNLs>0)
        {
            int nval= myConfig.overlappingUNLs*myConfig.Max_UNL;
            for (int j=0; j<nval;j++)
            {
                nodes[i]->unl.push_back(j);
                --unl_count;
            }
        }

        while (unl_count > 0)
        {
            int cn = r_node(gen);
            if ((cn != i) && !nodes[i]->isOnUNL(cn))
            {
                nodes[i]->unl.push_back(cn);
                --unl_count;
            }
        }
    }

    // mark malicious nodes
    std::cerr << " Marking malicious nodes, randomly" << std::endl;
    for (int i=0; i<myConfig.Num_Malicious; i++){
        int mn=r_node(gen);
        if (nodes[mn]->isMalicious){
            i--;
        }
        else
        {
            nodes[mn]->isMalicious=true;
        }        
    }

    // create links
    std::cerr << "Creating links" << std::endl;
    for (int i = 0; i < myConfig.Num_Nodes; ++i)
    {
        int links = myConfig.Num_Outbound_Links;
        while (links > 0)
        {
            int lt = r_node(gen);
            if ((lt != i) && !nodes[i]->hasLinkTo(lt))
            {
                int ll = nodes[i]->e2c_latency + nodes[lt]->e2c_latency + r_c2c(gen);
                nodes[i]->links.push_back(Link(lt, ll));
                nodes[lt]->links.push_back(Link(i, ll));
                --links;
            }
        }
    }

    Network network;

    // trigger all nodes to make initial broadcasts of their own positions
    std::cerr << "Creating initial messages" << std::endl;
    for (int i = 0; i < myConfig.Num_Nodes; ++i)
    {
        for (Link& l : nodes[i]->links)
        {
            Message m(i, l.to_node);
            m.data.insert(std::make_pair(i, NodeState(i, 1, nodes[i]->knowledge[i])));
            network.sendMessage(m, l, 0);
        }
    }
    std::cerr << "Created " << network.messages.size()  << " events" << std::endl;
    
    bool isFatal=false;
    // run simulation
    do
    {
        if (nodes_positive > (myConfig.Num_Nodes * myConfig.consensus_percent / 100))
            break;
        if (nodes_negative > (myConfig.Num_Nodes * myConfig.consensus_percent / 100))
            break;
        
        std::map<int, Event>::iterator ev=network.messages.begin();
        if (ev == network.messages.end())
        {
            std::cerr << "Fatal: Radio Silence" << std::endl;
            isFatal=true;
            break;
            // return 0;
        }

        if ((ev->first / 100) > (network.master_time / 100))
            std::cerr << "Time: " << ev->first << " ms  " <<
                nodes_positive << "/" << nodes_negative <<  std::endl;
        network.master_time = ev->first;

        for (const Message& m : ev->second.messages)
        {
            if (m.data.empty()) // message was never sent
                --nodes[m.from_node]->messages_sent;
            else
                nodes[m.to_node]->receiveMessage(m, network);
        }
        
        network.messages.erase(ev);
    } while (1);

    int mc = 0;
    for (std::map<int, Event>::iterator it = network.messages.begin(); it != network.messages.end(); ++it)
            mc += it->second.messages.size();

    if(!isFatal)
        std::cerr << "Consensus reached in " << network.master_time << " ms with " << mc
        << " messages on the wire" << std::endl;
    else
        std::cerr << "FATAL: Radio Silence in " << network.master_time << " ms with " << mc << " messages on the wire" << std::endl;
    
    
    // output results
    long total_messages_sent= 0 ;
    for (int i = 0; i < myConfig.Num_Nodes; ++i)
        total_messages_sent += nodes[i]->messages_sent;
    std::cerr << "The average node sent " << total_messages_sent/myConfig.Num_Nodes << " messages" << std::endl;

    std::cout << myConfig.Num_Nodes <<"\t"<< myConfig.Num_Malicious << "\t" << myConfig.consensus_percent << "\t" <<  myConfig.Num_Outbound_Links << "\t" << myConfig.Max_UNL << "\t" <<myConfig.Min_UNL 
            << "\t" <<myConfig.UNL_threshold << "\t" <<myConfig.overlappingUNLs
            << "\t" << myConfig.Min_c2c_latency << "\t" << myConfig.Max_c2c_latency << "\t" << myConfig.Min_e2c_latency<< "\t" <<myConfig.Max_e2c_latency
            << "\t" << network.master_time<< "\t" << mc<< "\t" <<total_messages_sent << "\t"<< (float)mc/(mc+total_messages_sent)<< "\t"<<isFatal << "\t"<< myConfig.malicious_nodes_percentage<< "\t"<<std::endl ;
    
    for( Node* n : nodes){
        delete(n);
    }
}
