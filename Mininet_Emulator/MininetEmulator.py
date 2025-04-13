#!/usr/bin/python
import Sim_GUI as sgui
import Sim_GUI_2 as sgui2
import os
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
from mininet.term import makeTerm
import random

exec(open("./mininet_settings").read())


def myTopology():

    info( '#**********# Start Mininet #**********#\n' )
    net_emu = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')

    info( '#**********# Adding SDN Controller #**********#\n' )
    c1=net_emu.addController(name='c1', controller=OVSController, protocol='tcp', port=6534)

    info( '#**********# Adding OVS-vswitches #**********#\n')
    s0 = net_emu.addSwitch('s0', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s1 = net_emu.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s2 = net_emu.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s3 = net_emu.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s4 = net_emu.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s5 = net_emu.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone', stp=1)

    info( '#**********# Adding Hosts #**********#\n')
    MS = net_emu.addHost('Master', ip='10.0.0.41/8')
    Server = net_emu.addHost('Server', ip='10.0.0.42/8')
    SS = net_emu.addHost('Slave', ip='10.0.0.43/8')

    #### Add external host
    n=15
    for h in range(1, n + 1):
        host_a = net_emu.addHost('a%s' % h)
        bw = random.randint(1,10)
        net_emu.addLink(host_a, s0, bw=bw, delay='0.2ms') # S2 --- (a1, a2, ..., a5) --> d=0.2ms, bw= 1-10

        host_b = net_emu.addHost('b%s' % h)
        bw = random.randint(1,10)
        net_emu.addLink(host_b, s5, bw=bw, delay='0.2ms') # S1 --- (b1, b2, ..., b5) --> d=0.2ms, bw= 1-10`

    info( '#**********# Linking host with OVS_vswitches #**********#\n')
    # Ht_swt_linkConfig = {'delay':'0', 'bw' : 100}

    Link1 = net_emu.addLink(MS, s1,cls=TCLink , **Ht_swt_linkConfiguration)
    Link11 = net_emu.addLink(Server, s3,cls=TCLink , **Ht_swt_linkConfiguration)
    Link2 = net_emu.addLink(SS, s5, cls=TCLink, **Ht_swt_linkConfiguration)

    info( '#**********# Linking OVS_vswitches with OVS_vswitches #**********#\n')

    Link2 = net_emu.addLink(s0, s1, cls=TCLink, **s0s1_linkConfiguration)
    Link3 = net_emu.addLink(s0, s3, cls=TCLink, **s0s3_linkConfiguration)
    Link4 = net_emu.addLink(s1, s2, cls=TCLink, **s1s2_linkConfiguration)
    Link5 = net_emu.addLink(s1, s3, cls=TCLink, **s1s3_linkConfiguration)
    Link6 = net_emu.addLink(s2, s4, cls=TCLink, **s2s4_linkConfiguration)
    Link7 = net_emu.addLink(s3, s4, cls=TCLink, **s3s4_linkConfiguration)
    Link9 = net_emu.addLink(s3, s5, cls=TCLink, **s3s5_linkConfiguration)
    Link10 = net_emu.addLink(s4,s5, cls=TCLink, **s4s5_linkConfiguration)

    info( '#**********# Start Network Emulatotion #**********#\n')
    net_emu.build()

    info( '#**********# Start SDN-Controller #**********#\n')
    c1.start()

    info( '#**********# Start OVS-vswitches  #**********#\n')
    net_emu.get('s0').start([c1])
    net_emu.get('s2').start([c1])
    net_emu.get('s1').start([c1])
    net_emu.get('s3').start([c1])
    net_emu.get('s4').start([c1])
    net_emu.get('s5').start([c1])

    net_emu.start()
    net_emu.staticArp()


    info( '#**********# loading routing rules and converging STP #**********#\n')
    time.sleep(35)

    net_emu.pingAll()

    return(net_emu)

def Exp01_Haptic_Data(net,n):

    print ("*** Loading IoTactileSim for Experiment Number 01 (START) >>>")
    n=n
    a = []
    b = []
    for i in range(1, n + 1):
        a.append(net['a%s' % i])
        b.append(net['b%s' % i])
    
    print('*** Testing connectivity between pairs')
    for i in range(n):
        net.ping(hosts=[a[i], b[i]])


    slave = net.get("Slave")
    server = net.get("Server")
    master = net.get("Master")


    for i in range(1, n + 2):
        if i==n+1:
            print(f' Programe Script Runing  {i}')
            makeTerm(slave,cmd='python3 ../1_Exp_Haptic_Data/haptic_slaveside.py; read')
            time.sleep(1)
            makeTerm(server, cmd='python3 ../1_Exp_Haptic_Data/haptic_serverside.py; read')
            time.sleep(1)
            makeTerm(master, cmd='python3 ../1_Exp_Haptic_Data/ms_comm.py; read')
        else:
            print('External Host runing')
            a[i - 1].cmd('netcat -l 1234 >/dev/null &')  # A host on S1 acts as Server
            time.sleep(random.random() * 2)  # Each transmission starts after a random delay between 0.2 and 2.0 secs
            MB = random.randint(3, 630)  # Random amount of MB to transmit
            b[i - 1].cmd('dd if=./file.test bs={}M count=1 | nc 10.0.0.{} 1234 &'.format(MB, i))


    event4 = next(sgui.send())
    if event4 == 'Display Result':
        sgui2.window.un_hide()
        sgui2.graph_plotting_Exp1()
        sgui2.window.hide()

    print("\n <<<<< Select Next Options >>>>>>"
          "\n (1)-Exp#1: SEensor Data Transfer"
          "\n (2)-Exit")

    event5 = next(sgui.send())
    if event5 == 'Exit Mininet' or sgui.sg.WIN_CLOSED:
        print('ExitMininet')
        exit()
    if event5 == 'EXP#1(Sensor Data)':
        sgui2.window.un_hide()
        sgui2.select_packet_HD()
        sgui2.window.hide()
        Exp01_Haptic_Data(net,n)



####### Starting Simulatator ########
if __name__ == '__main__':
    net=0
    event1=next(sgui.send())
    if event1=='Start Simulation':
        print("***  Simulation Start ***")
        os.system("sudo mn -c")
        setLogLevel('info')
        net = myTopology()

    print("***  Please Select Exeriment "
          "\n Exp#1: Sensor Data Transfer ***")

    event2 = next(sgui.send())
    if event2 == 'EXP#1(Sensor Data)':
        print("You Selected Sensor Data Transfer Exmeriment(#01)")
        print("Please Select Number of Packets for Sensor Data")
        sgui2.select_packet_HD()
        sgui2.window.hide()
        host=15
        Exp01_Haptic_Data(net,n=host)
            
    if event2 == 'Exit Mininet' or sgui.sg.WIN_CLOSED:
        print("You Selected Exit, See You! Again....")
        exit()


