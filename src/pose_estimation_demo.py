# Bare Minimum Pose Estimation Code

# Step 1:
import cv2     # OpenCV for video processing
import mediapipe as mp   # MediaPipe for pose estimation
import time     # To calculate the FPS (frames per second)


# Step 2: # Initialize the MediaPipe Pose model for pose detection and drawing utilities
mpDraw = mp.solutions.drawing_utils  # Drawing utilities for landmarks
mpPose = mp.solutions.pose  # Pose module for pose estimation
pose = mpPose.Pose()  # Create an instance of the Pose model


# Step 3: Open the video file for processing (it could be an image or webcam)
cam = cv2.VideoCapture(0)  # '3.mp4' is the input video


# Step 4: Create a resizable window for displaying the video
# cv2.namedWindow("Video Playback", cv2.WINDOW_NORMAL)  # Make window resizable
# cv2.resizeWindow("Video Playback", 1280, 720)  # Resize the window to 1280x720


# Step 5: Initialize previous time for FPS calculation
prevTime = 0


# Step 6: Start the video processing loop
while True:
    success, img = cam.read()  # Read a frame from the video
    if not success:  # If the frame is not read successfully, break the loop
        break
    img = cv2.resize(img, (640, 480))  # Resize frame to 640x480 pixels for faster processing


    # Step 7: Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed, break the loop
        break


    # Step 8: Convert the frame from BGR (OpenCV default) to RGB (required by MediaPipe)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    # Step 9: Process the frame to get the pose landmarks
    results = pose.process(imgRGB)


    # Step 10: Print the pose landmarks for debugging purposes
    print(results.pose_landmarks)

    # Step 11: If pose landmarks are detected in the frame
    if results.pose_landmarks:
        # Draw the pose landmarks on the frame using MediaPipe's drawing function
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        # Loop through all detected landmarks
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape  # Get the height, width, and channels of the image
            # print(id, lm)  # Print the ID and coordinates of each landmark

            # Convert the normalized landmark coordinates to pixel values
            cx, cy = int(lm.x * w), int(lm.y * h)

            # Draw a circle at each landmark's position (cx, cy) with a radius of 4
            cv2.circle(img, (cx, cy), 4, (255, 0, 0), cv2.FILLED)  # Draw red circles

    # Step 12: Calculate the current time to compute the FPS
    currTime = time.time()  # Get the current time
    fps = 1 / (currTime - prevTime)  # FPS = 1 / (time difference between current and previous frame)
    prevTime = currTime  # Update the previous time to the current time


    # Step 13: Display the FPS value on the image
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


    # Step 14: Display the processed image with pose landmarks and FPS
    cv2.imshow("Video Playback", img)


# Step 15: Release the video capture object and close all OpenCV windows when the loop ends
cam.release()  # Release the camera or video file
cv2.destroyAllWindows()  # Close all OpenCV windows

