#include <string.h>
#include <fstream>
#include <string>
#include <omnetpp.h>
#include <sstream>
#include <random>
#include <array>
    using namespace omnetpp;

    /**
     * InBox class definition
     */
    class InBox : public cSimpleModule
    {
    public:
        InBox();
    private:
        static const int ARRAY_SIZE = 2;
        cMessage*  LISTEN;
        cMessage*  INIT;
        int full;
        const  std::string csvfilename ="gateway.csv";
        std::array<int, ARRAY_SIZE> timeArray;
        std::array<int, ARRAY_SIZE> pldArray;
        std::pair<std::string, std::string> extractSubstrings(const std::string& inputString);
        double lambda;  // Rate parameter for the exponential distribution
        std::default_random_engine generator;
        std::exponential_distribution<double> distribution;
        void broadcast(int H, int pld);
        void restart();
        void writeDataToCSV(int D1H, int D2H, int SYNCH);
   protected:
        // The following redefined virtual function holds the algorithm.
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;

    };

    // The module class needs to be registered with OMNeT++
    Define_Module(InBox);


    InBox::InBox() {
        lambda = 0.9;
    }

    void InBox::initialize()
    {
        EV_INFO << "Module instance name: " << getFullName() << endl;
        restart();
    }

    void InBox::handleMessage(cMessage *msg)
    {

        EV << "Received " << msg->getName()  << endl;
        std::string s = msg->getName();

        bool isFound = s.find("TRANSMIT") != std::string::npos;

        if(isFound){
            int gateIndex = msg->getArrivalGateId();
            EV << "Received message on gate: " << gateIndex << endl;

            std::pair<std::string, std::string> extractedSubstrings = extractSubstrings(msg->getName());
            std::cout << "H substring: " << extractedSubstrings.first << std::endl;
            std::cout << "pld substring: " << extractedSubstrings.second << std::endl;

            if(gateIndex==0){
                int collectedclk = std::stoi(extractedSubstrings.first );
                int collectedpld= std::stoi(extractedSubstrings.second );
                timeArray[0]= collectedclk;
                pldArray[0]= collectedpld;
                full++;
            }else{
                int collectedclk = std::stoi(extractedSubstrings.first );
                int collectedpld= std::stoi(extractedSubstrings.second );
                timeArray[1]= collectedclk;
                pldArray[1]= collectedpld;
                full++;
            }

        }else{
            if(full==ARRAY_SIZE){
                int rclk= (timeArray[0]+timeArray[1])/2;
                broadcast(rclk, pldArray[1]);
                full=0;
                writeDataToCSV(timeArray[0],timeArray[1],rclk);
            }
        }


        restart();

    }

    /**
     * Broadcast the clock value to drones
     */
    void InBox::broadcast(int H, int pld){
        std::string result = std::string("LISTEN/") + std::string("1/") + std::string(std::to_string(H))+ "/" + std::string(std::to_string(pld));
        LISTEN = new cMessage(result.c_str());
        send(LISTEN, "DRONE1_LISTEN");
        sendDelayed(LISTEN->dup(), 1e-9,"DRONE0_LISTEN");
    }
    /**
     * Reschedule the send
     */
    void InBox::restart()
    {
        INIT = new cMessage();
        double interval = distribution(generator, std::exponential_distribution<double>::param_type(lambda));
        scheduleAt(simTime() + interval, INIT);
    }

    std::pair<std::string, std::string> InBox::extractSubstrings(const std::string& inputString) {
        std::pair<std::string, std::string> substrings;

        // Find the position of the first and second slashes
        size_t firstSlashPos = inputString.find('/');
        size_t secondSlashPos = inputString.find('/', firstSlashPos + 1);

        // Extract the "H" substring
        substrings.first = inputString.substr(firstSlashPos + 1, secondSlashPos - firstSlashPos - 1);

        // Extract the "pld" substring
        substrings.second = inputString.substr(secondSlashPos + 1);

        return substrings;
    }

    // Function to write data to a CSV file
    void InBox::writeDataToCSV(int D1H, int D2H, int SYNCH) {

        std::string result = std::string(simTime().str()) + ","+ std::string(std::to_string(D1H))+"," +std::string(std::to_string(D2H))+"," + std::string(std::to_string(SYNCH));
        std::ofstream file(csvfilename.c_str(), std::ios::app);
        if (file.is_open()) {
            file << result << endl;
            file.close();
        } else {
            // Handle file open error
            EV_ERROR << "Error opening file: " << csvfilename.c_str() << endl;
        }
    }
