#include <string.h>
#include <iostream>
    #include <omnetpp.h>

    using namespace omnetpp;

    using namespace std;

    class Crane : public cSimpleModule
    {
    private:
        std::vector<std::string> extractSubstrings(const std::string& inputString);
      protected:
        virtual void handleMessage(cMessage *msg) override;
    };


    Define_Module(Crane);


    void Crane::handleMessage(cMessage *msg)
    {

        std::string s = msg->getName();

        std::vector<std::string> extractedSubstrings = extractSubstrings( msg->getName());
        std::string H = extractedSubstrings[1];
        std::string lift = extractedSubstrings[2];
        EV << "H: " << H << endl;
        EV << "Lift: " << lift << endl;

    }


    std::vector<std::string> Crane::extractSubstrings(const std::string& inputString) {
        std::vector<std::string> substrings;
        std::istringstream iss(inputString);
        std::string substring;

        while (std::getline(iss, substring, '/')) {
            substrings.push_back(substring);
        }

        return substrings;
    }
