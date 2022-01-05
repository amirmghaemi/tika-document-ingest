# tika-document-ingest
Objective: Ingest libs for pulling/pushing docs from some dir or database, extracting basic text and metadata and forwarding that data into ELK.

## NIFI DOCUMENTATION

#### INSTALL NIFI 

1. Before beginning, make sure your device has JDK 8 installed and operational

2. Go to the official website https://nifi.apache.org/download.html and navigate from releases > 1.14.0 > binaries > nifi-1.14.0-bin.zip file and begin downloading. Our platform was created with the version 1.14.0 release.

3. Unzip the file and this is how the folder structure will be in your system file explorer tool. The folder should contain: bin, conf, docs, extensions, lib, license, notice, and readme.

#### INSTALL PREREQUISITE NAR FILE

1. After you have installed NiFi, you have one more task - and that is to install our prerequisite processor. To do this, download the “nifi-extracttext-nar-1.5.nar” file from this repo onto your system.

2. Once downloaded, navigate to the nifi-1.14.0 folder you extracted the content of earlier when it was a .zip file. Once inside this folder, go to the “lib” folder (short for library). This folder houses NiFi’s NAR files which are used to create processors within the app. 

3. Once inside the nifi-1.14.0 -> lib folder, move the nar file you downloaded here. You may have to restart your computer to allow NiFi to update and register the processor.

#### START NIFI 

1. To start the NiFi, you can directly double click on the “run-nifi.bat” file in the nifi-1.14.0 -> bin folder. 

2. If the command line produces a process ID, then your NiFi instance is running. You can also check the status of NiFi by executing the “status-nifi.bat” file.

3. Go to the following URL – https://localhost:8443/nifi/  to check if the NiFi has started. Your port might be different. Don’t worry if this URL is not loading instantly. NiFi takes time after starting, just check periodically every few minutes.

4. ***Once the folders are created***, you can check the URL. If you see a warning message stating that “your connection is not private”, click on “Advanced” and then click on “Proceed to (host number)”.

#### USERNAME AND PASSWORD 

1. You should now be approached by a login page asking for your username and password. This information can be found within the “nifi-app.log” file in the nifi-1.14.0 -> logs folder.

2. Open the “nifi-app.log” file and use Ctrl+F to search for the keywords “username” and “password”. Once you have these credentials, go to the URL where NiFi is running and enter the details.


#### INSTALL TEMPLATE

1. Once you are on the NIFI platform, your canvas should be empty. If not, this is okay. Holding down the shift key, use the mouse to select the canvas you see. Then, once the canvas is selected, right click your mouse while the cursor is on the template and press “delete”.

2. Now that your canvas is clean, right click an empty space on the canvas and press “Upload Template”. From here, press “Select Template” and choose the NIFI template you have downloaded from our GitHub repository.

#### SET UP DATA TO INGEST 

1. In order to run the template, you will first need to create a new folder on your computer containing the various files you would like NIFI to ingest. An example of this is the folder called “nifi input” I created on my system. This folder can contain any file types, just make sure it has all of the files that you would like NIFI to take in. Also, it is important to note that any files in this folder will be deleted when Nifi is run. The location of this folder on my system is “C:\Users\Kymani\Documents\nifi input”. 

2. After you have created a folder on your system and put in the files you would like NIFI to ingest, go back to the NIFI app on your browser. 

3. Once in the NIFI app, double click the processor group called “Get File & Convert to JSON” to open it. Once here, double click the “GetFile” processor. After this, navigate to the “properties” tab.

4. From here, you should see a property titled “Input Directory”. In the space next to it labeled “Value”, simply paste the EXACT file path of the folder containing your files you would like NIFI to ingest, with an example file path being “C:\Users\Kymani\Documents\nifi input” and press OK to close the processor.

#### RUN THE TEMPLATE 

1. Now you are all set! Now, to run NIFI and all of the processor groups.

2. If you would like to run NiFi and all of its processors we have created, look at the bottom left of your NIFI app inside of the static solid white/gray colored bar. Make sure you are on the NIFI FLOW page and not inside of any of the processor groups. An easy way to confirm this is look at your canvas, you should see all three processor groups, if you do then proceed. If you do not, simply press the NiFi FLOW text at the bottom of the screen and you will be navigated to the main page showing all of the processors. 

3. After confirming you are on the main page showing all three processor groups, simply right click your mouse on a black space of the canvas and press “Start” and NIFI will begin running the processes. In order for the pipeline to run correctly, make sure you have ELASTICSEARCH accessible and DOCKER running.

#### NIFI USER-GUIDE

1. Please refer to this link https://nifi.apache.org/docs/nifi-docs/html/user-guide.html to discover the various ways you can use nifi.

## ELK STACK DOCUMENTATION

#### Notes
1. "ELK" stands for ElasticSearch, LogStash, and Kibana / ElatisSearch = Data Store | LogStash = ? | Kibana = Data Visualization
2. Prerequisites for properly utilizing this stack is having Docker up and running on your system

#### Download ELK stack
1. Download the "security-tweaks" branch of this docker-ELK fork: https://github.com/UMD-ARLIS/docker-elk
2. Extract the "docker-elk-security-tweaks" folder

#### Run instance of ELK stack
2. Navigate to the "docker-compose.yml" file inside of the extracted folder
3. Right click in the folder and click "Open in Windows Terminal"
4. Use the "docker compose up" command to start an instance of ELK stack

#### Setup instance of ELK stack
5. Once ELK stack is running successfully, run the workflow in Nifi and send data to the ELK stack
6. Access ELK stack through a browser (Microsoft Edge works well) and click on the three horizontal lines at the top left. At this moment you will be entering ElasticSearch.
7. Once inside ElasticSearch, scroll down to the "Management" section and click on "Stack Management"
8. Near the left edge of the page, click on "Index Patterns" under "Kibana"
9. Click on the blue "Create index pattern" button
10. Type "tikac*" into the box for "Index pattern name" and click "Next step"
11. Click "file.creationTime" for the "Time field" box and click "Create index pattern"
12. Repeat steps 8 to 11, using "tikam*" for the "Index pattern name" box in step 10

#### View data in Kibana
13. Click on the three horizontal lines at the top left and click on "Discover" under the "Analytics" section 
14. Change between the index patterns "tikac*" and "tikam*" by clicking on the index pattern dropdown above the field names near the left edge
15. View the data within a specific range of time by filtering the time at the top right or by clicking on the green bars of data 
