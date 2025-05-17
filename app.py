import cv2
import streamlit as st
import pandas as pd
import numpy as np

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

def get_color_name(R, G, B, colors_df):
    minimum = float('inf')
    closest_color = "Unknown"
    for _, row in colors_df.iterrows():
        d = abs(R - row["R"]) + abs(G - row["G"]) + abs(B - row["B"])
        if d < minimum:
            minimum = d
            closest_color = row["name"]
    return closest_color

def main():
    st.title("🎨 Color Detection Tool")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image, use_column_width=True)
        
        if st.session_state.get('click', False):
            x, y = st.session_state.click.x, st.session_state.click.y
            if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                r, g, b = image[y, x]
                color_name = get_color_name(r, g, b, load_colors())
                st.success(f"Color: {color_name} | RGB: ({r}, {g}, {b})")
                st.color_picker("", value=f"#{r:02x}{g:02x}{b:02x}", disabled=True)

        st.session_state.click = st.image_clicker("Click on the image")

if __name__ == "__main__":
    main()
    try:
    import cv2
    import numpy as np
except ImportError as e:
    import streamlit as st
    st.error(f"Failed to import required packages: {e}")
    st.stop()  # Prevent the app from running without dependencies
