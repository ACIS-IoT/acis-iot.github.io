simple WV
{
    parameters:
        @display("i=watervolume;is=l");
        @icon(images/drone.png);
        double driftRate;

    gates:
        input WV_LISTEN;
        output WV_TRANSMIT;
}

simple WL
{
    parameters:
        @display("i=sealevel;is=l");
        @icon(images/drone.png);
        double driftRate;

    gates:
        input WL_LISTEN;
        output WL_TRANSMIT;
}

simple Rain
{
    parameters:
        @display("i=rain;is=s");
        @icon(images/drone.png);
        double driftRate;

    gates:
        input Rain_LISTEN;
        output Rain_TRANSMIT;
}

simple InBox
{
    parameters:
        @display("i=device/antennatower");
        @icon(images/drone.png);

    gates:
        input Rain_TRANSMIT;
        input WL_TRANSMIT;
        input WV_TRANSMIT;

        output Rain_LISTEN;
        output WL_LISTEN;
        output WV_LISTEN;
}

//
// Two instances (tic and toc) of Txc1 connected both ways.
// Tic and toc will pass messages to one another.
//
network CranesOrchestration
{
    @display("bgb=1112.776,849.966");
    submodules:
        Gateway: InBox {
            @display("p=933.296,444.854;i=device/antennatower");
        }

        wl: WL {
            @display("p=151.276,116.662;is=s");
        }
        wv: WV {
            @display("p=160.25,591.002;is=s");
        }
        rain: Rain {
            @display("p=151.276,371.78");
        }
    connections:
        rain.Rain_TRANSMIT --> {  delay = 100ms; } --> Gateway.Rain_TRANSMIT;
        wl.WL_TRANSMIT --> {  delay = 100ms; } --> Gateway.WL_TRANSMIT;
        wv.WV_TRANSMIT --> {  delay = 100ms; } --> Gateway.WV_TRANSMIT;

        Gateway.Rain_LISTEN --> {  delay = 100ms; } --> rain.Rain_LISTEN;
        Gateway.WL_LISTEN --> {  delay = 100ms; } --> wl.WL_LISTEN;
        Gateway.WV_LISTEN --> {  delay = 100ms; } --> wv.WV_LISTEN;

}
