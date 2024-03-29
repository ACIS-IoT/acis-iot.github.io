#include <string.h>
#include <string>
#include <omnetpp.h>
#include <sstream>
#include <random>
#include <fstream>
#include <random>
    using namespace omnetpp;

    /**
     * Derive the Txc1 class from cSimpleModule. In the Tictoc1 network,
     * both the `tic' and `toc' modules are Txc1 objects, created by OMNeT++
     * at the beginning of the simulation.
     */
    class WaterFlow : public cSimpleModule
    {
    public:
        WaterFlow();
    private:
        cMessage*  TRIGGER;
        int H;
        const  std::string csvfilename ="log.csv";
        int PLD;
        int nextBroadcast;
        int cycleLenght;
        int refractoryPeriod;
        int sameCount;
        const int  sameThreshold=2;
        double lambda;  // Rate parameter for the exponential distribution
        std::default_random_engine generator;
        std::exponential_distribution<double> distribution;
        std::vector<std::string> extractSubstrings(const std::string& inputString);
        void transmit(int H, int pld);
        void lift(int H,int pld);
        void restart();
        void writeDataToCSV(const std::string& action, int pld);
   protected:
        // The following redefined virtual function holds the algorithm.
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;

    };

    // The module class needs to be registered with OMNeT++
    Define_Module(WaterFlow);


    WaterFlow::WaterFlow() {
        lambda = 0.5;
    }

    void WaterFlow::initialize()
    {
        TRIGGER = new cMessage();
        double interval = distribution(generator, std::exponential_distribution<double>::param_type(lambda));
        scheduleAt(simTime() + interval, TRIGGER);
    }


    void WaterFlow::handleMessage(cMessage *msg)
    {

        EV << "Received  " << msg->getName()  << endl;
        std::string s = msg->getName();

        bool isFound = s.find("WF") != std::string::npos;
        if(isFound){
            std::vector<std::string> extractedSubstrings = extractSubstrings( msg->getName());
            std::string PLD = extractedSubstrings[1];
            int pld = std::stoi(PLD);
            writeDataToCSV("WF", pld);
        }


        TRIGGER = new cMessage();
        double interval = distribution(generator, std::exponential_distribution<double>::param_type(lambda));
        scheduleAt(simTime() + interval, TRIGGER);
    }


    // Function to write data to a CSV file
    void WaterFlow::writeDataToCSV(const std::string& action,   int pld) {

        std::string result = std::string(simTime().str()) + ","+ std::string(std::to_string(pld));
        std::ofstream file(csvfilename.c_str(), std::ios::app);
        if (file.is_open()) {
            file << result << endl;
            file.close();
        } else {
            // Handle file open error
            EV_ERROR << "Error opening file: " << csvfilename.c_str() << endl;
        }
    }

    std::vector<std::string> WaterFlow::extractSubstrings(const std::string& inputString) {
        std::vector<std::string> substrings;
        std::istringstream iss(inputString);
        std::string substring;

        while (std::getline(iss, substring, '/')) {
            substrings.push_back(substring);
        }

        return substrings;
    }
