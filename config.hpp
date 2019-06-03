#ifndef __CONFIG_HPP__
#define __CONFIG_HPP__

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

//

#ifndef LEDGER_CONVERGE
    #define LEDGER_CONVERGE          4
#endif
#ifndef LEDGER_FORCE_CONVERGE
    #define LEDGER_FORCE_CONVERGE    7
#endif
#ifndef AV_MIN_CONSENSUS
    #define AV_MIN_CONSENSUS        50
#endif
#ifndef AV_AVG_CONSENSUS
    #define AV_AVG_CONSENSUS        60
#endif
#ifndef AV_MAX_CONSENSUS
    #define AV_MAX_CONSENSUS        70
#endif

#ifndef NUM_NODES
    #define NUM_NODES             1000
#endif
#ifndef NUM_MALICIOUS_NODES
    #define NUM_MALICIOUS_NODES     15
#endif
#ifndef CONSENSUS_PERCENT
    #define CONSENSUS_PERCENT       80
#endif

// Latencies in milliseconds
// E2C - End to core, the latency from a node to a nearby node
// C2C - Core to core, the additional latency when nodes are far 
#ifndef MIN_E2C_LATENCY
    #define MIN_E2C_LATENCY          5
#endif
#ifndef MAX_E2C_LATENCY
    #define MAX_E2C_LATENCY         50
#endif
#ifndef MIN_C2C_LATENCY
    #define MIN_C2C_LATENCY          5
#endif
#ifndef MAX_C2C_LATENCY
    #define MAX_C2C_LATENCY        200
#endif
#ifndef NUM_OUTBOUND_LINKS
    #define NUM_OUTBOUND_LINKS      10
#endif
#ifndef UNL_MIN
    #define UNL_MIN                 20
#endif
#ifndef UNL_MAX
    #define UNL_MAX                 30
#endif
#ifndef UNL_THRESH
    #define UNL_THRESH              (UNL_MIN/2) // unl datapoints we have to have before we change position
#endif

#ifndef BASE_DELAY
    #define BASE_DELAY               1 // extra time we delay a message to coalesce/suppress
#endif

#ifndef SELF_WEIGHT
    #define SELF_WEIGHT              1 // how many UNL votes you give yourself
#endif
#ifndef PACKETS_ON_WIRE
    #define PACKETS_ON_WIRE          3 // how many packets can be "on the wire" per link per direction
                                   // simulates non-infinite bandwidth
#endif

//

class SimulatorConfiguration{
    private:
        std::string configfilename;
        boost::property_tree::ptree pt;

    public:
        int Num_Nodes           = NUM_NODES;
        int Num_Malicious       = NUM_MALICIOUS_NODES;
        int Num_Outbound_Links  = NUM_OUTBOUND_LINKS;
        float malicious_nodes_percentage =100.0* NUM_MALICIOUS_NODES / NUM_NODES;
        
        int Max_e2c_latency = MAX_E2C_LATENCY;
        int Min_e2c_latency = MIN_E2C_LATENCY;
        
        int Max_c2c_latency = MAX_C2C_LATENCY;
        int Min_c2c_latency = MIN_C2C_LATENCY;
        
        int Max_UNL         = UNL_MAX;
        int Min_UNL         = UNL_MIN;
        int UNL_threshold   = UNL_THRESH;

        int Base_Delay  = BASE_DELAY;
        int Self_Weight = SELF_WEIGHT;
        int Packets_on_Wire = PACKETS_ON_WIRE;

        int consensus_percent =  CONSENSUS_PERCENT;

        SimulatorConfiguration( std::string cfilename): configfilename(cfilename) {
            read_configFile( cfilename);
            //boost::property_tree::ini_parser::read_ini(cfilename, pt);

        }
        SimulatorConfiguration(){  ; };

        void read_configFile ( std::string cfilename ){
            configfilename=cfilename;
            boost::property_tree::ini_parser::read_ini(configfilename, pt);

            // boost::property_tree::ptree::const_assoc_iterator miter= pt.find("Latency.max_c2c_latency"); 
            // if (miter== pt.not_found())
            //     std::cerr << "not found" << std::endl;

            Max_c2c_latency=pt.get<int>("Latency.max_c2c_latency");
            Min_c2c_latency=pt.get<int>("Latency.min_c2c_latency");

            Max_e2c_latency=pt.get<int>("Latency.max_e2c_latency");
            Min_e2c_latency=pt.get<int>("Latency.min_e2c_latency");

            Num_Nodes=pt.get<int>("Nodes.num_nodes");
            Num_Malicious=pt.get<int>("Nodes.num_malicious");
            malicious_nodes_percentage = 100.0* Num_Malicious / Num_Nodes;

            consensus_percent=pt.get<int>("Blockchain.consensus_percent");
            Max_UNL=pt.get<int>("Blockchain.max_unl");
            Min_UNL=pt.get<int>("Blockchain.min_unl");
            UNL_threshold=pt.get<int>("Blockchain.unl_threshold");
            Num_Outbound_Links=pt.get<int>("Blockchain.num_outbound_links");

            Base_Delay=pt.get<int>("Simulation.base_delay");
            Self_Weight=pt.get<int>("Simulation.self_weight");
            Packets_on_Wire=pt.get<int>("Simulation.packet_on_wire");

        }
};

#endif