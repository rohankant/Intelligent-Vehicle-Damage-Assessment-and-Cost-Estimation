# Flask Application for Vehicle Damage Assessment and Cost Estimation

This folder contains the files required to run our flask application forIntelligent vehicle damage assessment and cost estimation with images.

The folder contains the following Structure:
1. *app.py*: This file contains the flask implementation of the application.
2. *static folder*: This folder contains the following folders:
    * *css*: Contains all CSS files needed to style the application.
    * *js*: Contains the javascript files necessary to run this application (mainly for uploading of image by user).
3. *templates folder*: Contains all HTML files needed by the application.
4. *models*: Contains Models (In this demo the models exceed Github limit hence arent present in the code)



## Setup

1. Python version used - `3.8.16`
2. Tensorflow version - `2.12.0`
3. All training was done on Jupyter Notebooks.
4. Dataset used for:
    * *Damaged/Not damaged*: (https://www.kaggle.com/datasets/anujms/car-damage-detection)
    * *Damage localization*: Made In House
    * *Damage extremity*: Made In House
5. Google Drive link for our Dataset: (https://drive.google.com/drive/folders/1uwSP3DXzjnVyVOxCzGyr8BC00iUiVlCp?usp=sharing)



## Running the application

To run the application locally, follow these steps:
1. Clone the repository by running the command: 
2. Change your current working directory to the cloned repository. 
3. Install all the required libraries for the application.
4. Start the application by executing the command:<br> `python app.py`
5. Once the application is running, copy the localhost link provided in the terminal output and paste it into your web browser.

By following these steps, you will be able to run the application locally on your machine.
