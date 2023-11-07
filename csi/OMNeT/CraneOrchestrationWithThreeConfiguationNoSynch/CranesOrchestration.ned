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
    @display("bgb=1110.4401,1890.1621");
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
        Crane2: Crane {
            @display("p=786.96405,1011.466;i=crane");
        }
        Crane3: Crane {
            @display("p=786.96405,659.02203;i=crane");
        }
        Drone2: Drone {
            @display("p=120.700005,1011.466;is=-");
        }
        Drone3: Drone {
            @display("p=137.598,659.02203;is=-");
        }

        Gateway1: InBox {
            @display("p=446.59003,794.206;i=device/antennatower");
        }

        Crane4: Crane {
            @display("p=762.82404,1634.2781;i=crane");
        }
        Crane5: Crane {
            @display("p=762.82404,1281.834;i=crane");
        }
        Drone4: Drone {
            @display("p=96.560005,1634.2781;is=-");
        }
        Drone5: Drone {
            @display("p=113.458,1281.834;is=-");
        }

        Gateway2: InBox {
            @display("p=422.45,1417.0181;i=device/antennatower");
        }

    connections:
        Drone0.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway.DRONE0_TRANSMIT;
        Drone1.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway.DRONE1_TRANSMIT;

        Gateway.DRONE0_LISTEN --> {  delay = 100ms; } --> Drone0.DRONE_LISTEN;
        Gateway.DRONE1_LISTEN --> {  delay = 100ms; } --> Drone1.DRONE_LISTEN;

        Drone0.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane0.CRANE_LIFT;
        Drone1.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane1.CRANE_LIFT;

        Gateway1.DRONE0_LISTEN --> {  delay = 100ms; } --> Drone2.DRONE_LISTEN;
        Gateway1.DRONE1_LISTEN --> {  delay = 100ms; } --> Drone3.DRONE_LISTEN;

        Drone3.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway1.DRONE1_TRANSMIT;

        Drone3.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane3.CRANE_LIFT;

        Drone2.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway1.DRONE0_TRANSMIT;
        Drone2.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane2.CRANE_LIFT;
        Drone5.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway2.DRONE1_TRANSMIT;

        Drone5.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane5.CRANE_LIFT;

        Drone4.DRONE_TRANSMIT --> {  delay = 100ms; } --> Gateway2.DRONE0_TRANSMIT;
        Drone4.CRANE_LIFT --> {  delay = 100ms;@display("ls=#1A5FB4"); } --> Crane4.CRANE_LIFT;
        Gateway2.DRONE0_LISTEN --> {  delay = 100ms; } --> Drone4.DRONE_LISTEN;
        Gateway2.DRONE1_LISTEN --> {  delay = 100ms; } --> Drone5.DRONE_LISTEN;

}
