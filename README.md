# REAL TIME HUMAN DETECTION

- In this project the model with the input either as a live feed from any camera or a video file ,can detect the number of people at that instant as shown in the below video
- This is an end to end project , python's Streamlit framework is used.
- The works with YOLOV4 Model.





- > Down below , the sample output of a video file.

https://user-images.githubusercontent.com/82393353/173562045-5b2c7d60-2f85-455c-b982-b21e5e945864.mp4


## How YOLO works

- > As the name yolo(You only look once) tells, The total prediction of image is completed in one forward propogation(one run).

- > The yolov is built with convolutional neural networks.The yolov algoritham divides the image in to specific grids of equal areas and these grids are used for detection.

- > These grids predict the co-ordinates of the grid, object label and probability.But as there are many cells predicting the main object, there will be multiple bounding boxes for the same object , to solve this problem the algoritham uses the simple non maximal suppression technique.

- > Non maximal suppression technique bascically means , it takes a look at all the bounding boxes of an object in the image and selects the the box which has the highest probability , then it removes the all the boxes which overlap with the selected box thus getting the best bounding box.

- > Yolo architecture contains 24 convolutional neural networks and to fully connected neural networks.




![60edcdbb660bc4adc635f744_P9709u0H-JwS5jCaxiFCdr0_HQnbe3dExzj7Nq_fkcL3HIFTsBGt2uTWA89fLVcZik5dBjVw5BRlSy5KooKI-tXCXmPJ1aLHVxOcr-YLxGKbVwBrxjWKCCo8TUV90TgB37tmkpMz](https://user-images.githubusercontent.com/82393353/178156157-d3336995-b119-4aec-8c05-217019a3c83a.png)




