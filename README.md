# ECI-Elderly-TeleCaring-Monitoring-System

This repository discusses the implementation code for " Enabling Pandemic-Resilient Healthcare: Edge-Computing-Assisted Real-Time Elderly Caring Monitoring System" article.
### How to Setup Experiment Environment 
Installation steps:
1. Install git
``` Sudo apt-get install git ```
2. Clone repo from GitHub
``` Git clone https://github.com/zubair1811/IntelligentTactileEdge2022.git ```
3. Check that python3.8 and pip3 are installed in the Ubuntu Linux or not if not then follow as
```
sudo apt-get update
sudo apt-get install python3.8 (If you got an error then first install the repo for that b version)
sudo apt install software-properties-common
 sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install python3-pip (for python 3)
sudo apt install Python-pip (for python 2) [Not used in our system, you may test]
```
4. Install mininet: Go to mininet official website https://mininet.org/download/ 
```
git clone https://github.com/mininet/mininet
cd mininet
git tag  # list available versions
git checkout -b mininet-3.6.9 (I choose this version for simulation)
PYTHON=python3 util/install.sh –a (This indicates that we are going to use python3)
If It shows Enjoy Mininet! it means successfully installed 
WE can check by using the ‘mn -c’ command
```
5. Install all other packages 
```
sudo python3 -m pip install numpy
sudo python3 -m pip install pandas
sudo python3 -m pip install PySimpleGUI==4.59.0
sudo python -m pip install scikit-learn
sudo python -m pip install substring
sudo python -m pip install pynput
sudo python -m pip install keras
sudo python -m pip install tensorflow: Note the actual simulation was done with tensorflow=1.13.1 however it is not further available we can use any version.  
```	
6. To run the simulation follow the below command 
``` sudo python3 Network_Topo.py ```
