# United States Superstore Data Analysis 📊

An exploratory data analysis (EDA) project focused on understanding sales performance, profitability, customer segments, and business trends using the **United States Superstore dataset**. The project includes a Jupyter Notebook for detailed analysis and an interactive dashboard built with Streamlit.

## 🚀 Live Dashboard

**Explore the interactive dashboard:** [Open Streamlit App](https://unitedstate-superstore-dataanalysis-duduma6cckcxyv9vnsmtzd.streamlit.app/)

> Replace `YOUR_STREAMLIT_APP_URL` with your deployed Streamlit Community Cloud URL.

## 📌 Project Overview

The goal of this project is to explore the Superstore dataset, identify meaningful patterns, and understand the relationships between sales, profit, quantity, and discounts.

The project combines Python-based exploratory data analysis with an interactive Streamlit dashboard, making the findings easier to explore and understand.

## ✨ Features

- **Data Exploration:** Examine the dataset's structure, columns, data types, and summary statistics.
- **Data Quality Checks:** Investigate missing values, duplicate records, and potential data-quality issues.
- **Sales Analysis:** Explore sales performance and trends over time.
- **Profitability Analysis:** Analyze profit patterns and the relationship between discounts and profitability.
- **Exploratory Data Analysis (EDA):** Use statistical summaries and visualizations to identify patterns and relationships.
- **Interactive Dashboard:** Explore key performance indicators and charts through dashboard filters.
- **Correlation Analysis:** Examine relationships between numerical variables.
- **Business Insights:** Use the analysis to better understand sales and profitability patterns.

## 🛠️ Technologies Used

- **Python** — core programming language
- **Pandas** — data manipulation and analysis
- **NumPy** — numerical operations
- **Matplotlib** — data visualization
- **Jupyter Notebook** — exploratory analysis
- **Streamlit** — interactive dashboard development

## 📂 Project Structure

```text
UnitedState-SuperStore-DataAnalysis/
│
├── data/
│   └── Sample-superstore.xls
│
├── app.py
│
├── UnitedState_SuperStore_data_Analysis.ipynb
│
├── requirements.txt
│
└── README.md
```

- `data/Sample-superstore.xls` — source dataset used for analysis.
- `app.py` — Streamlit dashboard application.
- `UnitedState_SuperStore_data_Analysis.ipynb` — Jupyter Notebook containing the exploratory data analysis.
- `requirements.txt` — Python dependencies required to run the application.
- `README.md` — project documentation.

## 📈 Key Areas of Analysis

### 1. Sales and Profit

Explore overall sales and profit performance and examine how these metrics change over time.

### 2. Discount and Profitability

Investigate the relationship between discount levels and profit to better understand discounting patterns in the dataset.

### 3. Category and Segment Analysis

Explore business performance across product categories, customer segments, and regions using the dashboard's available filters.

### 4. Correlation Analysis

Examine relationships among numerical variables, including sales, profit, quantity, and discount. Correlation can reveal associations but does not establish causation.

## 💻 Run the Project Locally

### Prerequisites

Install Python and Git. Python 3.10 or later is a reasonable starting point; use a version compatible with your installed dependencies.

### 1. Clone the repository

```bash
git clone https://github.com/iftikhar-jafry/UnitedState-SuperStore-DataAnalysis.git
```

### 2. Navigate to the project directory

```bash
cd UnitedState-SuperStore-DataAnalysis
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Make sure `requirements.txt` includes the packages required by the app, including `streamlit`, `pandas`, `numpy`, `matplotlib`, and `xlrd` if the application reads the `.xls` dataset directly.

### 5. Run the Streamlit dashboard

```bash
streamlit run app.py
```

The application will open in your browser. If it does not, Streamlit will display a local URL in the terminal.

## ☁️ Deployment

The dashboard is deployed using **Streamlit Community Cloud**.

To deploy your own version:

1. Push the project to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account.
4. Select the repository, branch, and `app.py` file.
5. Deploy the application.

See the [official Streamlit deployment documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app) for details.

## 🎓 Learning Context

This project was developed as part of my learning journey through the **AI Bootcamp organized by PSEB and atomcamp at Iqra University**.

It provided an opportunity to apply Python and data analysis concepts to a business dataset while developing practical experience in exploratory data analysis, data visualization, and dashboard development.

## 🔮 Learning Outcomes

Through this project, I practiced:

- Working with structured datasets using Pandas and NumPy.
- Performing exploratory data analysis.
- Identifying data-quality issues and examining potential outliers.
- Creating visualizations to communicate findings.
- Exploring relationships between business metrics.
- Building and deploying an interactive dashboard with Streamlit.

## 👨‍💻 Author

**Iftikhar Hussain Jaffari**

Computer Science Graduate | Interested in Data Analytics, Data Engineering, and Artificial Intelligence.

## 🙌 Acknowledgments

- **PSEB** — Pakistan Software Export Board
- **atomcamp** — AI Bootcamp learning opportunity
- **Iqra University** — Bootcamp host institution
- The creators and providers of the Superstore dataset used for this analysis

---

⭐ If you find this project useful, feel free to explore the notebook and interactive dashboard, and share your feedback!
