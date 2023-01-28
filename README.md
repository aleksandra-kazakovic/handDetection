# Recognition-POC
The Recognition POC application is a software tool that is designed to improve the efficiency and accuracy of the work process by reducing errors that can occur when workers take products from the wrong compartment of a bin. To achieve this, the application uses a camera placed above the bin, which is divided into compartments and processes the recording to detect the hand of the worker as they reach into the bin to take a product. After that, it can be easily determined whether he took the product from the expected compartment or not.

## What needs to be adjusted
### portConfigurations.ini 
It is necessary to set the port number and the video we want to process. It is possible to have multiple ports and videos. If we want a live stream instead of a video, then we need to set cameraInput to 0.

Example when we want a live stream
````
[Port1Config]
portId = 0
cameraInput = 0
````
Example when we want to monitor several different ports

````
[Port1Config]
portId = 0
cameraInput = demo1.mp4

[Port2Config]
portId = 1
cameraInput = demo2.mp4
````

### binConfigurations.ini
It is necessary to set the parameters that show where the bin starts and what are the dimensions of the bin. **typeOfBin** determines how many compartments the bin has and it also needs to be set.
Example 
````
[BinConfig]
binStartX = 0
binStartY = 0
binWidth = 600
binHeight = 330
typeOfBin = 13
````

### .env for Database 
Create a PostgreSQL database named recognition_poc and set other parameters. 
Example 
````
PG_HOST=localhost
PG_DATABASE=recognition_poc
PG_USER=postgres
PG_PASSWORD=SecurePas$1
PG_PORT='5432'
````


Run the program with ````python .\main.py````

## Help with determining the dimensions of the bin

In order to make it easier to determine the dimensions of the bin, there is an auxiliary application within the project.

In the file **findBox.py**, it is necessary to set the **videoPath** so that it contains a video on which the position of the bin needs to be determined.
The program can be run using the ````python .\Detection\findBox.py```` command. 
These dimensions can later be used for setting binConfigurations.ini
