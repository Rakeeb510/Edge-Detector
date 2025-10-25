# Edge Detector

## Project Description
This is an interactive, web-based application developed using Python and Streamlit for visual experimentation with classical edge detection algorithms. The interface allows users to upload an image and dynamically adjust algorithm-specific parameters (Sobel, Laplacian, and Canny) to observe their effects in real-time.

## Setup and Installation Instructions
1.  **Prerequisites:** Ensure you have Python 3.12 installed.
2.  **Clone the Repository:**
    ```bash
    git clone YOUR_GITHUB_REPOSITORY_URL
    cd YOUR_REPOSITORY_NAME
    ```
3.  **Install Dependencies:** This project requires Streamlit and OpenCV.
    ```bash
    pip install streamlit opencv-python numpy
    ```

## How to Run the Application
1.  Navigate to the project directory in your terminal.
2.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
3.  The application will automatically open in your default web browser at `localhost:8501`.

## Features Implemented
* **Image Upload:** Supports JPG, PNG, and BMP formats.
* **Dual Display Layout:** Input (Original) and Output (Processed) views are arranged side-by-side.
* **Algorithms:** Implemented Canny, Sobel, and Laplacian edge detection.
* **Dynamic Controls:** Intuitive sliders and select boxes for real-time parameter modification, including Canny thresholds, Sobel direction, and kernel sizes.
* **Parameter Reset:** A dedicated button in the sidebar resets all algorithm parameters to their initial default values.
* **User Interface:** Clean, centered, and user-friendly design.
