# Traffic-sign-detection
Project of photoelectric information processing experiment in ZJU, ISEE

<p align="center">
<img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/process/demo1.gif" />
</p>

<p align="center">
<img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/process/demo2.gif" />
</p>

## Overview

This is a small embedded project based on Raspberry Pi. The 'sparrow' may be small, fully-equipped. 

It involves the following:

- Colour extraction and ellipse detection based on traditional methods
- Video and order transfer between Raspberry Pi and PC based on socket programming using TCP/UDP protocol
- Simple remote controller based on PyQt5
- Image multi-classification problem based on classical neural network (lenet here)
- Application of SSD pedestrian detection model
- Raspberry Pi level output based on RPi.GPIO library
- Raspberry Pi built-in audio player driver calls

More details in [our project report (in Chinese)](https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/report.pdf) and [demo video](https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/demo.flv).

## References

- [Ellipse detection](https://github.com/ghostbbbmt/Traffic-Sign-Detection)
- [SSD model](https://github.com/zlingkang/mobilenet_ssd_pedestrian_detection)
- [Image classifer framework](https://github.com/AstarLight/Keras-image-classifer-framework)
- [Driver board datasheeet](http://www.wifi-robots.com/thread-8996-1-1.html)

## File structure

### Run demo

- on your PC

  - get your LAN IP address of PC 

    ```
     ipconfig
    ```

  - run on your cmd or Anaconda Prompt

    ```
    python3 PC.py --host=your_IP_address 
    ```

  - if you want to use TCP protocol to transfer video (not recommend)

    ```
    python3 PC.py --udp=False --host=your_IP_address 
    ```

- on your Pi

  - get your LAN IP address of Pi

    ```
     ifconfig
    ```

  - run on your terminal

    ```
    python3 Pi.py --host=your_IP_address 
    ```

  - if you want to use TCP protocol to transfer video (not recommend)

    **should be same as the protocol you chose on your PC**

    ```
    python3 Pi.py --udp=False --host=your_IP_address 
    ```

  - if you want complete all calculations on your Pi (not recommend)

    ```
    python3 run_direct.py
    ```

### Tools

- color_extract.py

  It is a small interactive UI for easy access to get color data in video

- remote_controller.py

  It is a simple UI which can control your car

- rename.py

  It is a script which can rename all your files in one dir

- utils.py

  It contains some useful functions

<p align="center">
    <img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/process/new.jpg" , width="360"/>
    <img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/process/binary.png" , width="360"/>
    <img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/process/labeled.png" , width="360"/>
    <img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/process/box.png" , width="360"/>
</p>

- grasp.py

  It can determine the flag type in an image or video and crop it out for use in data set construction and early debugging

### Learning-related

- lenet.py

  It is the network struct of lenet
  
  <p align="center">
  <img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/model/model.png" />
  </p>
  

- train.py

  Train the model of lenet, which implements a seven-classify (one background, six signs) task
  
  <p align="center">
  <img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/process/template.jpg" />
  </p>
  
  <p align="center">
  <img src="https://github.com/BrandonHanx/Traffic-sign-detection/blob/master/images/result_plot.png" />
  </p>
  
- predict.py

  Predict the label of single image

- pedestrian.py

  It is a script that calls the SSD model

  

