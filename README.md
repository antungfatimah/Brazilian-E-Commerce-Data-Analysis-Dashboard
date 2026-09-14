# Proyek Analisis Data: E-Commerce Public Dataset ✨

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Struktur Direktori
```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   └───(seluruh file dataset .csv)
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Run Notebook
Notebook `notebook.ipynb` sudah dijalankan (executed) dan bisa dibuka langsung dengan Jupyter/Google Colab.
```
jupyter notebook notebook.ipynb
```
Notebook ini juga menyimpan `dashboard/main_data.csv`, yaitu data hasil wrangling yang dipakai oleh dashboard.

## Run Streamlit App
```
cd dashboard
streamlit run dashboard.py
```
Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.
