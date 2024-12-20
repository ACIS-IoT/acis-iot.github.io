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
    class Drone : public cSimpleModule
    {
    public:
        Drone();
    private:
        cMessage*  INIT;
        cMessage*  LIFT;
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
        void lift(int H,int pld);
        void restart();
        void writeDataToCSV(const std::string& action, const std::string& source, int h, int pld);
   protected:
        // The following redefined virtual function holds the algorithm.
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;

    };

    // The module class needs to be registered with OMNeT++
    Define_Module(Drone);


    Drone::Drone() {
        lambda = 0.5;  // Set the lambda value for the exponential distribution
        H=0;
        PLD=1;
        cycleLenght   =  150;
        refractoryPeriod  = 100;
        nextBroadcast = intuniform(0, refractoryPeriod);
    }

    void Drone::initialize()
    {

        EV_INFO << "Module instance name: " << getFullName() << endl;
        driftRate = par("driftRate");
        restart();
    }


    void Drone::handleMessage(cMessage *msg)
    {
        EV << "Received " << msg->getName()  << endl;
        std::string s = msg->getName();

        bool isFound = s.find("LISTEN") != std::string::npos;

        if (!isFound) {
            bool eval_to_transmit= ((H==nextBroadcast) || ( (H==(nextBroadcast+refractoryPeriod) % cycleLenght) && sameCount<sameThreshold));
            if(eval_to_transmit){
                transmit(H,PLD);
                sameCount=0;
            }
        }else{
            listen_input = simTime().dbl();

            listen_input= listen_input-sendTimeDouble;

            std::ofstream file("send_times.txt", std::ios::app);
            if (file.is_open()) {
                std::string str = std::to_string(listen_input);
                std::string result = "COMMUNICATION LAG FOR DRONE GATEWAY : " + str;
                file << result << endl;
                file.close();
            } else {
                // Handle file open error
                EV_ERROR << "Error opening file: " << csvfilename.c_str() << endl;
            }

            //LISTEN
           // writeDataToCSV("LISTEN",std::string(getFullName()),H,PLD);
            // Call the function to extract substrings
               std::vector<std::string> extractedSubstrings = extractSubstrings( msg->getName());
               std::string full = extractedSubstrings[1];
               int isFull = std::stoi(full);


            if(isFull==1){

                if(H>refractoryPeriod){
                    std::string rclk = extractedSubstrings[2];
                    int collectedclk = std::stoi(rclk);
                    H=collectedclk;
                }
                std::string rpld = extractedSubstrings[3];
                int collectedpld = std::stoi(rpld);
                if(PLD==collectedpld){
                    sameCount++;
                    lift(H,PLD);
                }else{
                    if(PLD>collectedpld){
                        PLD=collectedpld;
                    }else{
                        transmit(H,PLD);
                    }
                }

            }
        }

        /**
         * Increment the local tick
         */
        if(H==cycleLenght){
           H=0;
           sameCount=0;
        }else{
            double interval = distribution(generator, std::exponential_distribution<double>::param_type(driftRate));
            if (interval <= driftRate) {
                H=H+2;
            } else {
                H=H+1;
            }
        }





        //Schedule a while
        restart();
    }


    /**
     * Transmit a message
     */
    void Drone::transmit(int H, int pld)
    {

        std::string result = std::string("TRANSMIT/") + std::string(std::to_string(H))+"/" + std::string(std::to_string(pld));
        TRANSMIT = new cMessage(result.c_str());

        sendTimeDouble = simTime().dbl();



        send(TRANSMIT, "DRONE_TRANSMIT"); // send out the message
        //writeDataToCSV("TRANSMIT",std::string(getFullName()),H,pld);
    }

    /**
     * Send a lift to the drone
     */
    void Drone::lift(int H,int pld)
    {
        std::string result = std::string("LIFT/")+ std::string(std::to_string(H)) + "/" +std::string(std::to_string(pld));
        LIFT = new cMessage(result.c_str());
        send(LIFT, "CRANE_LIFT"); // send out the message
        //writeDataToCSV("LIFT",std::string(getFullName()),H,pld);
    }
    /**
     * reschedule the send
     */
    void Drone::restart()
    {
        INIT = new cMessage();
        double interval = distribution(generator, std::exponential_distribution<double>::param_type(lambda));
        scheduleAt(simTime() + interval, INIT);
    }

    /**
     * extract substring from a message
     */
    std::vector<std::string> Drone::extractSubstrings(const std::string& inputString) {
        std::vector<std::string> substrings;
        std::istringstream iss(inputString);
        std::string substring;

        while (std::getline(iss, substring, '/')) {
            substrings.push_back(substring);
        }

        return substrings;
    }


    // Function to write data to a CSV file
    void Drone::writeDataToCSV(const std::string& action, const std::string& source, int h, int pld) {

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
