simple Drone
{
    parameters:
        @display("i=drone;is=s");
        @icon(images/drone.png);
        double driftRate;

    gates:
        input DRONE_LISTEN;
        output DRONE_TRANSMIT;
        output CRANE_LIFT;
}

simple InBox
{
    parameters:
        @display("i=device/antennatower");
        @icon(images/drone.png);

    gates:
        input DRONE0_TRANSMIT;
        input DRONE1_TRANSMIT;
        output DRONE0_LISTEN;
        output DRONE1_LISTEN;
}

simple Crane
{
    @display("i=crane");
    gates:
        input CRANE_LIFT;
}

//
// Two instances (tic and toc) of Txc1 connected both ways.
// Tic and toc will pass messages to one another.
//
network CranesOrchestration
{
    @display("bgb=965.60004,637.296");
    submodules:
        Drone0: Drone {
            @display("p=120.700005,456.246;is=-");
        }
        Drone1: Drone {
            @display("p=137.598,103.802;is=-");
        }

        Gateway: InBox {
            @display("p=446.59003,238.98601;i=device/antennatower");
        }

        Crane0: Crane {
            @display("p=786.96405,456.246;i=crane");
        }
        Crane1: Crane {
            @display("p=786.96405,103.802;i=crane");
        }
    connections:
        Drone0.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway.DRONE0_TRANSMIT;
        Drone1.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway.DRONE1_TRANSMIT;

        Gateway.DRONE0_LISTEN --> {  delay = 100ms; } --> Drone0.DRONE_LISTEN;
        Gateway.DRONE1_LISTEN --> {  delay = 100ms; } --> Drone1.DRONE_LISTEN;

        Drone0.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane0.CRANE_LIFT;
        Drone1.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane1.CRANE_LIFT;

}
