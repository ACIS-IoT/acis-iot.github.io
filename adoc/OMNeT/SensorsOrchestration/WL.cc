#include <string.h>
#include <string>
#include <omnetpp.h>
#include <sstream>
#include <random>
#include <fstream>

    using namespace omnetpp;

    /**
     * Drone class definition
     */
    class WL : public cSimpleModule
    {
    public:
        WL();
    private:
        cMessage*  INIT;
        cMessage*  TRANSMIT;
        std::ofstream outfile;
        const  std::string csvfilename ="log.csv";
        double driftRate; // drift rate in seconds
        int H;
        int PLD;
        int nextBroadcast;
        int cycleLenght;
        int refractoryPeriod;
        int sameCount;
        const int  sameThreshold=2;
        double lambda;  // Rate parameter for the exponential distribution
        double listen_input;
        double sendTimeDouble;
        std::default_random_engine generator;
        std::exponential_distribution<double> distribution;
        std::vector<std::string> extractSubstrings(const std::string& inputString);
        void transmit(int H, int pld);
        void restart();
        void writeDataToCSV(const std::string& action, const std::string& source, int h, int pld);
   protected:
        // The following redefined virtual function holds the algorithm.
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;

    };

    // The module class needs to be registered with OMNeT++
    Define_Module(WL);


    WL::WL() {
        lambda = 0.5;  // Set the lambda value for the exponential distribution
        H=0;
        PLD=1;
    }

    void WL::initialize()
    {

        EV_INFO << "Module instance name: " << getFullName() << endl;
        driftRate = par("driftRate");
        restart();
    }


    void WL::handleMessage(cMessage *msg)
    {
        EV << "Received " << msg->getName()  << endl;
        std::string s = msg->getName();

        bool isFound = s.find("LISTEN") != std::string::npos;

        if (!isFound) {

                transmit(H,PLD);
        }else{
            std::vector<std::string> extractedSubstrings = extractSubstrings( msg->getName());
                     std::string full = extractedSubstrings[1];
                     int isFull = std::stoi(full);


                  if(isFull==1){
                      std::string rclk = extractedSubstrings[2];
                      int collectedclk = std::stoi(rclk);
                      H=collectedclk;

                  }
        }

        /**
         * Increment the local tick
         */

              double interval = distribution(generator, std::exponential_distribution<double>::param_type(driftRate));
                if (interval <= driftRate) {
                    H=H+2;
                } else {
                    H=H+1;
                }
        //Schedule a while
        restart();
    }


    /**
     * Transmit a message
     */
    void WL::transmit(int H, int pld)
    {
        std::string result = std::string("TRANSMIT/") + std::string(std::to_string(H))+"/" + std::string(std::to_string(pld));
        TRANSMIT = new cMessage(result.c_str());
        send(TRANSMIT, "WL_TRANSMIT"); // send out the message
    }


    /**
     * reschedule the send
     */
    void WL::restart()
    {
        INIT = new cMessage();
        double interval = distribution(generator, std::exponential_distribution<double>::param_type(lambda));
        scheduleAt(simTime() + interval, INIT);
    }

    /**
     * extract substring from a message
     */
    std::vector<std::string> WL::extractSubstrings(const std::string& inputString) {
        std::vector<std::string> substrings;
        std::istringstream iss(inputString);
        std::string substring;

        while (std::getline(iss, substring, '/')) {
            substrings.push_back(substring);
        }

        return substrings;
    }


    // Function to write data to a CSV file
    void WL::writeDataToCSV(const std::string& action, const std::string& source, int h, int pld) {

        std::string result = std::string(simTime().str()) + ","+ action +","+ source +"," +std::string(std::to_string(h))+"," + std::string(std::to_string(pld));
        std::ofstream file(csvfilename.c_str(), std::ios::app);
        if (file.is_open()) {
            file << result << endl;
            file.close();
        } else {
            // Handle file open error
            EV_ERROR << "Error opening file: " << csvfilename.c_str() << endl;
        }
    }
