# Initial tests of emotion recognition method on Pepper robot
 
This repository involves the implementation of a [previous work](https://github.com/juan1t0/multimodalDLforER.git) but in the robotic context, specifically working with a Pepper robot.
 
The presented implementation consists of an out-robot emotion system. The whole deep-learning procedures run in a server while the robot executes determined actions according to the emotions recognised.
 
 
## Installation
 
Clone the repositories of two projects, And move the `multimodalDLforER` folder inside the `rutas-tests` folder
 
```bash
git clone https://github.com/juan1t0/rutas-tests.git
git clone https://github.com/juan1t0/multimodalDLforER.git
```
 
## Usage
 
This project use python scripts of two versions, 2.7 and 3.9, because the communication with robot needs the **NAOqi framework**, which works only with python 2.7.
 
To run this project
 
```bash
python main.py
```
 
The trained deep learning model are available in [google drive shared folder](https://drive.google.com/drive/folders/1NWrEQQWPqf3lH4YC9UMUx6mD_K3qShau?usp=sharing). For more information of this previous work visit [its github page](https://github.com/juan1t0/multimodalDLforER).
 
