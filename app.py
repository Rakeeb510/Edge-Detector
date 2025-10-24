import streamlit as st
import cv2
import numpy as np
import time # Import time for a quick visual delay, if needed, though not strictly necessary

# --- Configuration and Logo/Favicon ---
# Setting the page config for a better look and feel
st.set_page_config(
    page_title="Edge Detector",
    page_icon="📸", 
    layout="wide" # Using wide layout for better side-by-side viewing
)

# --- 1. Parameter Widgets ---

def get_canny_params():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Gaussian Blur (Pre-filter)")
    # ADDED UNIQUE KEY
    sigma = st.sidebar.slider("Sigma (Gaussian Blur)", 0.0, 5.0, 1.0, 0.1, key='canny_sigma', help="Sigma value for the preceding Gaussian filter.") 
    
    st.sidebar.subheader("Canny Thresholds")
    # ADDED UNIQUE KEYS
    lower_threshold = st.sidebar.slider("Lower Threshold (minVal)", 0, 255, 50, key='canny_minval', help="Minimum threshold for edge linking.")
    upper_threshold = st.sidebar.slider("Upper Threshold (maxVal)", 0, 255, 150, key='canny_maxval', help="Maximum threshold for initial edge detection.")
    
    st.sidebar.subheader("Kernel/Aperture Size")
    # ADDED UNIQUE KEY
    aperture_size = st.sidebar.selectbox("Kernel Size (Aperture)", (3, 5, 7), index=0, key='canny_aperture', help="Size of the Sobel kernel used for finding image gradients.")
    
    return {
        'sigma': sigma,
        'minVal': lower_threshold,
        'maxVal': upper_threshold,
        'aperture_size': aperture_size
    }

def get_sobel_params():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Gradient Direction")
    # ADDED UNIQUE KEY
    direction = st.sidebar.selectbox("Gradient Direction", ("X and Y (Combined)", "X only", "Y only"), key='sobel_direction', help="Select the direction(s) for gradient calculation.")
    
    st.sidebar.subheader("Kernel/Aperture Size")
    # ADDED UNIQUE KEY
    ksize = st.sidebar.selectbox("Kernel Size (ksize)", (3, 5, 7), index=0, key='sobel_ksize', help="Size of the Sobel kernel.")

    return {
        'direction': direction,
        'ksize': ksize
    }

def get_laplacian_params():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Kernel/Aperture Size")
    # ADDED UNIQUE KEY
    ksize = st.sidebar.selectbox("Kernel Size (ksize)", (1, 3, 5, 7), index=1, key='laplacian_ksize', help="Size of the Laplacian kernel.") 
    
    return {
        'ksize': ksize
    }


# --- 2. Image Processing Logic (No Change) ---

def process_image(image, algorithm, params):
    # All algorithms operate on grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = gray 

    if algorithm == "Canny":
        sigma = params['sigma']
        
        if sigma > 0.0:
            ksize_gauss = int(sigma * 4 + 1)
            if ksize_gauss % 2 == 0: ksize_gauss += 1
            if ksize_gauss < 3: ksize_gauss = 3
            
            blurred = cv2.GaussianBlur(gray, (ksize_gauss, ksize_gauss), sigma)
        else:
            blurred = gray

        processed_image = cv2.Canny(
            blurred, 
            params['minVal'], 
            params['maxVal'], 
            apertureSize=params['aperture_size']
        )
        
    elif algorithm == "Sobel":
        ksize = params['ksize']
        direction = params['direction']
        
        ddepth = cv2.CV_16S 
        
        grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=ksize)
        
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        
        if direction == "X only":
            processed_image = abs_grad_x
        elif direction == "Y only":
            processed_image = abs_grad_y
        else: # X and Y (Combined)
            processed_image = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        
    elif algorithm == "Laplacian":
        ksize = params['ksize']
        
        ddepth = cv2.CV_16S 
        
        laplacian = cv2.Laplacian(gray, ddepth, ksize=ksize)
        processed_image = cv2.convertScaleAbs(laplacian)
        
    return processed_image


# --- 3. UI Layout and Control Logic ---

def reset_params_to_defaults():
    # List of all parameter keys used in the widgets
    param_keys = [
        'algorithm_select', # Also reset the algorithm selector
        'canny_sigma', 'canny_minval', 'canny_maxval', 'canny_aperture',
        'sobel_direction', 'sobel_ksize',
        'laplacian_ksize'
    ]
    
    # Delete all parameter keys from session state
    for key in param_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    # Rerun the app to force widgets to re-initialize with their default values
    st.rerun()


def edge_detection_ui():
    st.sidebar.header("Controls")
    
    # Select an edge detection algorithm
    algorithm = st.sidebar.selectbox(
        "Select Algorithm:",
        ("Canny", "Sobel", "Laplacian"), 
        key='algorithm_select' # UNIQUE KEY ADDED HERE
    )
    
    st.sidebar.success(f"Selected: **{algorithm}**") 
    
    st.sidebar.subheader(f"{algorithm} Parameters")
    
    # Dynamically display parameters based on the selected algorithm
    params = {}
    if algorithm == "Canny":
        params = get_canny_params()
    elif algorithm == "Sobel":
        params = get_sobel_params()
    elif algorithm == "Laplacian":
        params = get_laplacian_params()

    
    # --- Reset button at the bottom of the sidebar ---
    st.sidebar.markdown("---")
    st.sidebar.button("Reset Parameters", on_click=reset_params_to_defaults, help="Resets all algorithm parameters to their starting default values.")
    st.sidebar.markdown("---")
    
    # Check if an image is uploaded
    if st.session_state['original_image'] is not None:
        original_image = st.session_state['original_image']
        
        original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        processed_image = process_image(original_image, algorithm, params)
        
        # The UI must consist of two primary displays: Input and Output side-by-side.
        col1, col2 = st.columns(2)
        
        # --- Display Input ---
        with col1:
            # Centered title for Input
            st.markdown("<h2 style='text-align: center;'>Input</h2>", unsafe_allow_html=True) 
            st.image(original_image_rgb, caption='Original Image', use_container_width=True) 
            
        # --- Display Output ---
        with col2:
            # Centered title for Output
            st.markdown("<h2 style='text-align: center;'>Output</h2>", unsafe_allow_html=True) 
            
            # Convert 1-channel edge map to 3-channel BGR, then to RGB for Streamlit display
            processed_image_bgr = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
            processed_image_rgb = cv2.cvtColor(processed_image_bgr, cv2.COLOR_BGR2RGB)
            
            st.image(processed_image_rgb, caption=f'{algorithm} Edge Map', use_container_width=True) 
            
    else:
        # File uploader section will be displayed here by the main function
        pass


# --- 4. Application Entry Point ---

def main():
    # Centered Title
    st.markdown("<h1 style='text-align: center;'>Edge Detector</h1>", unsafe_allow_html=True)
    # Centered Description
    st.markdown("<p style='text-align: center;'>Experiment with Sobel, Laplacian, and Canny algorithms and their parameters in real-time.</p>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png", "bmp"]) 

    if uploaded_file is not None:
        if 'last_uploaded_name' not in st.session_state or st.session_state['last_uploaded_name'] != uploaded_file.name:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            st.session_state['original_image'] = original_image
            st.session_state['last_uploaded_name'] = uploaded_file.name 

    edge_detection_ui() 
    
# Initialize session state for the image storage
if 'original_image' not in st.session_state:
    st.session_state['original_image'] = None
if 'last_uploaded_name' not in st.session_state:
    st.session_state['last_uploaded_name'] = None
    
if __name__ == '__main__':
    main()