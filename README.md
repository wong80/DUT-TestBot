# DUT-TestBot
### Introduction
DUT-TestBot is a simple python-based program that is developed to automate common DUT (Device under Test) tests to validate the performance of the said Instrument such as Power Supply Unit (PSU) or electrical applicanes, modules. The application fundamentally uses **`PyVisa`** Library, a python wrapper for **`VISA` (Virtual Instrument Software Architecture)** to communicate and send commands to these instruments. The commands sent to the instruments are `SCPI` (Standard Commands for Programmable Instruments) through the hardware layer. The program is also equipped with a simple GUI that was programmed using `PyQt5` as well as basic data analysis and visualization using python libraries `pandas` & `matplotlib`.
 
## Installation Guide
### Requirements
`python >=3.11.2` Latest version of Python can be downloaded from [here](https://www.python.org/downloads/).
### Dependencies
The dependencies for this program has been listed in `requirements.txt`. If you are running a virtual environment, you can install the dependencies using:
```
pip install requirements.txt
```
### 1. Downloding ZIP File
Go find the repository of this GitHub or click [here](https://github.com/wong80/DUT-TestBot) and click `Download ZIP`. After download is complete, extract to the directory of your choice. To run the program, click on the `GUI.exe` found in Executables Folder

### 2. Using GitHub Desktop
Use the URL link [here](https://github.com/wong80/DUT-TestBot) and paste the URL in `Clone A Repository` section in GitHub Desktop, or head to the repository and just click on `Open with GitHub Desktop`

### 3. Using Git
Copy the line of code below into git bash to download the repository.
```
gh repo clone wong80/DUT-TestBot
```
## Supported Models 
This lists contains the list of Instrument Models/Series that are compatible with this program.
##

## User Guide
When the executable is opened, user should be greeted by a window that should look as below.

## To-Do List
