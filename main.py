import cv2
import tkinter as tk
import threading
from datetime import datetime

# Loading the Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initializing video capture
cap = cv2.VideoCapture(0)

# Initialize tkinter GUI
root = tk.Tk()
root.title("Face Blurring App")

# Function to toggle between blurring and drawing a bounding box
def toggle_effect():
    global blur_faces
    blur_faces = not blur_faces

# Function to capture and save a photo with a timestamp-based name
def take_photo():
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        photo_name = f"Photo_{timestamp}.jpg"
        cv2.imwrite(photo_name, frame)
        print(f"Photo Captured: {photo_name}")

# Create tkinter buttons for the functions
effect_button = tk.Button(root, text="Toggle Effect", command=toggle_effect)
photo_button = tk.Button(root, text="Take Photo", command=take_photo)

effect_button.pack()
photo_button.pack()

# Initializing flags for blurring
blur_faces = False

# Function to update the display
def update_display():
    ret, frame = cap.read()

    if blur_faces:
        # Detect faces in the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Apply blurring to the detected face region
            face = frame[y:y+h, x:x+w]
            blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
            frame[y:y+h, x:x+w] = blurred_face

    cv2.imshow("Face Effect App", frame)
    root.after(10, update_display)  # Schedule the update

update_display()

# Using a separate thread to run the waitKey function
display_thread = threading.Thread(target=cv2.waitKey, args=(1,))

# Tkinter event loop
root.mainloop()

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
