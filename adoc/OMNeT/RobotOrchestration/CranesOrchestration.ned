simple Robot
{
    parameters:
        @display("i=robot;is=l");
        @icon(images/drone.png);
        double driftRate;

    gates:
        input Robot_LISTEN;
        output Robot_TRANSMIT;
}

simple InBox
{
    parameters:
        @display("i=device/antennatower");
        @icon(images/drone.png);

    gates:
        input Robot0_TRANSMIT;
        input Robot1_TRANSMIT;
        output Robot0_LISTEN;
        output Robot1_LISTEN;
}

//
// Two instances (tic and toc) of Txc1 connected both ways.
// Tic and toc will pass messages to one another.
//
network CranesOrchestration
{
    @display("bgb=965.60004,637.296");
    submodules:
        Robot0: Robot {
            @display("p=396.138,469.212;is=vs");
        }
        Robot1: Robot {
            @display("p=158.968,208.966;is=vs");
        }

        Gateway: InBox {
            @display("p=828.172,269.22;i=device/antennatower");
        }

    connections:
        Robot0.Robot_TRANSMIT --> {  delay = 100ms; } --> Gateway.Robot0_TRANSMIT;
        Robot1.Robot_TRANSMIT --> {  delay = 100ms; } --> Gateway.Robot1_TRANSMIT;

        Gateway.Robot0_LISTEN --> {  delay = 100ms; } --> Robot0.Robot_LISTEN;
        Gateway.Robot1_LISTEN --> {  delay = 100ms; } --> Robot1.Robot_LISTEN;

}
