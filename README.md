# README

## Project Title: SMS Data Processing Application

### Overview

This project is a full-stack application designed to process, analyze, and visualize SMS data from MTN MoMo, a prominent Mobile Payment Service Provider in Rwanda. This application handles XML data, performs data cleaning and categorization, storse the data in an sqlite3 database, and provides a frontend interface for data visualization.

### Objectives

- **Process SMS Data**: Read and parse the provided XML file containing approximately 1600 SMS messages.
- **Clean and Categorize Data**: Implement data cleaning techniques to ensure data integrity and categorize messages based on their type.
- **Database Management**: Store the processed SMS data in a relational database for efficient querying and analysis.
- **Frontend Development**: Build an interactive dashboard to visualize insights derived from the SMS data, allowing for easy analysis.

### Technologies Used

- **Backend**:

  - Python (Flask) for server-side logic
  - XML parsing libraries (`xml.etree.ElementTree` in Python)
  - SQL database (sqlite3)

- **Frontend**:
  - HTML / CSS / Javascript for creating the user interface

### Getting started

1. **Setup Development Environment**:

   - Install necessary software (Python).
   - Set up a version control system (Git).

2. **Clone Repo**:

- git clone git@github.com:eldrige/MoMo_Stat_App.git.

3. **Setup virtual env**:

   - python3 -m venv env
   - source env/bin/activate

4. **Install Flask**:

   - pip install flask

5. **Run the Application**:

   - python3 app.py

### Repository Link

- [Momo Stat App](https://github.com/eldrige/MoMo_Stat_App)
