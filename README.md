# Dicoding_EC-Analysis
This project is a remake of the Dicoding Academy assignment, E-Commerce Data Analysis, with enhanced data analysis and visualization. The goal is to answer various business questions related to an e-commerce company’s performance.

## Key Objectives
- **Company's Sales and Revenue**: Analyzing the company's sales and revenue on a month-to-month basis to understand trends and business performance.
- **Customer Locations**: Identifying where customers are making their transactions by analyzing the geographical distribution of customer locations.
- **Location Relationships**: Examining the correlation between customer locations and seller locations involved in transactions to identify regional patterns within the e-commerce ecosystem.

## Raw Dataset
[Kaggle: Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Tools
- **Visual Studio Code**: An IDE for writing, debugging, and running Python scripts in a streamlined development environment.
- **Jupyter Notebook**: A code documentation tool that allows the use of both Markdown for text and Python for coding.
- **Python**: A high-level programming language for data analysis.
- **Anaconda Prompt**: A command-line interface for managing Anaconda environments and running Python scripts.
- **Command Prompt (Terminal)**: A basic command-line tool for file navigation and executing commands.
- **Git Bash**: A command-line tool for interacting with Git repositories and running Unix commands.

## Python Libraries
- **os**: Library for interacting with the local operating system, including reading raw data files.
- **pandas**: Library for handling and cleaning datasets.
- **matplotlib**: Library for creating data visualizations.
- **seaborn**: Library for creating advanced statistical plots.
- **numpy**: Library for numerical operations in Python.
- **babel**: Library for handling locale-aware formatting for dates, times, numbers, and currencies.
- **streamlit**: Framework for building interactive dashboards from Python scripts.

## Process Overview
1. **Data Wrangling**: Gathered, assessed, and cleaned the raw datasets to ensure they are in a usable format.
2. **Exploratory Data Analysis (EDA)**: Explored the cleaned datasets to gain meaningful insights.
3. **Visualization and Explanatory Analysis**: Analyzed the cleaned datasets and highlight the key findings through visualization.
4. **Visualization in Streamlit**: Integrated the analysis and visualizations into a local website using Streamlit.

## How to Run Streamlit Dashboard Locally
### Setup Environment - Anaconda
Create and activate the environment, then install the required libraries.

```
conda create --name main-ds python=3.9
conda activate main-ds
pip install streamlit babel
```
### Setup Environment - Shell/Terminal
Navigate to the project directory.
```
cd ..
cd .. <!-- Back to C -->
cd <!-- Full Path to "submission" Folder -->
cd Dashboard
```
### Run Streamlit Application
Run the Streamlit application via the terminal. This will launch the dashboard in your default browser.
```
streamlit run dashboard.py
```

## File Structure
```
│  
├── data/                                       # Raw dataset folder  
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
│   └── .gitattributes                          # Git LFS configuration for large files (>25MB)
├── main_data.csv                               # Preprocessed dataset
├── notebook.ipynb                              # Jupyter notebook for data preprocessing, analysis, and visualization
├── dashboard.py                                # Streamlit app script
├── requirements.txt                            # List of dependencies for the project
└── README.md                                   # Project documentation
```

## Future Work
This project can be further enhanced by implementing the following ideas:
- **Advanced Analysis Techniques**: Apply advanced analytical techniques such as RFM analysis, geoanalysis, clustering, and regression to uncover deeper insights from the data.
- **Deploying to Streamlit Cloud**: Deploy the dashboard to Streamlit Cloud for easier access and collaboration.
- **Integrate with Machine Learning Models**: Enhance the dashboard by integrating it with machine learning models to provide predictive analytics.
