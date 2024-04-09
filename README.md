# PhonePe-Pulse-Data-Visualization-and-Exploration
A live Geo Visualization Streamlit dashboard that displays information and insights from the PhonePe pulse Github repository in an interactive and visually appealing manner.

# Libraries/Modules needed required

  1. Plotly - (To plot and visualize the data)
  2. Pandas - (To Create a DataFrame with the scraped data)
  3. MySql server- (To store and retrieve the data)
  4. Streamlit - (To Create Graphical user Interface)
  5. json - (To load the json files)
  6. PIL - The Python Imaging Library, used for opening, manipulating, and saving many different image file formats.

# Approach:
  Step 1:
        Data Extraction: The data is obtained from the Phonepe pulse Github repository using scripting techniques and cloned for further processing.

  Step 2:
        Data Transformation: The extracted data is formatted into a suitable structure, ensuring it is clean and ready for analysis. Pre-processing tasks may be performed           as necessary.

  Step 3:
        Database Integration: The transformed data is inserted into a MySQL database, offering efficient storage and retrieval capabilities.
        
  Step 4:
        Live Geo Visualization Dashboard: Python's Streamlit and Plotly libraries are utilized to create an interactive and visually appealing dashboard. This dashboard             presents the data in real-time, enabling users to explore the insights effectively.
        
  Step 5:
        Database Integration with the Dashboard: The relevant data is fetched from the MySQL database and seamlessly integrated into the dashboard, ensuring the displayed           information is up-to-date and accurate.
        
  Step 6:
        User-Selectable Dropdown Options: The dashboard incorporates a minimum of 10 distinct dropdown options, providing users with the ability to select and view various          facts and figures of interest. This feature enhances the customization and flexibility of the dashboard.
