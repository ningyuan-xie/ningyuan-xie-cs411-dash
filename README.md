## Table of Contents
- [1. Title: GradXplorer (R1, R2)](#1-title-gradxplorer-r1-r2)
- [2. Purpose (R4, R5)](#2-purpose-r4-r5)
  - [2.1 Application Scenario](#21-application-scenario)
  - [2.2 Target Users](#22-target-users)
  - [2.3 Objectives](#23-objectives)
- [3. Demo (R3)](#3-demo-r3)
- [4. Installation (R6, R7, R8)](#4-installation-r6-r7-r8)
  - [4.1 Option 1: Install Packages from requirements.txt](#41-option-1-install-packages-from-requirementstxt)
  - [4.2 Option 2: Use Conda Environment from environment.yml](#42-option-2-use-conda-environment-from-environmentyml)
  - [4.3 Run the Application](#43-run-the-application)
- [5. Usage (R9, R12)](#5-usage-r9-r12) 
    - [5.1 Widget 1: Top 10 Trending Keywords in Publications (R6, R7, R11)](#51-widget-1-top-10-trending-keywords-in-publications-r6-r7-r11)
    - [5.2 Widget 2: User-selected Favorite Keywords (R6, R11)](#52-widget-2-user-selected-favorite-keywords-r6-r11)
    - [5.3 Widget 3: Faculty Members Relevant to Selected Keywords (R6, R10, R11)](#53-widget-3-faculty-members-relevant-to-selected-keywords-r6-r10-r11)
    - [5.4 Widget 4: Faculty Members with the Highest KRC for Selected Keywords (R6, R7, R11)](#54-widget-4-faculty-members-with-the-highest-krc-for-selected-keywords-r6-r7-r11)
    - [5.5 Widget 5: Top 10 Keywords in Faculty Interests from Selected Universities (R8, R10, R11)](#55-widget-5-top-10-keywords-in-faculty-interests-from-selected-universities-r8-r10-r11)
    - [5.6 Widget 6: Top 10 Universities Collaborated with Selected Universities (R6, R8, R11)](#56-widget-6-top-10-universities-collaborated-with-selected-universities-r6-r8-r11)
- [6. Design](#6-design)
    - [6.1 Frontend (Dash Plotly) (R9, R12)](#61-frontend-dash-plotly-r9-r12)
    - [6.2 Middle Layer (Flask & Python)](#62-middle-layer-flask--python)
    - [6.3 Database Layer (MySQL, MongoDB, Neo4j) (R6, R7, R8)](#63-database-layer-mysql-mongodb-neo4j-r6-r7-r8)
- [7. Implementation](#7-implementation)
  - [7.1 Detailed Implementation](#71-detailed-implementation)
  - [7.2 Frameworks & Libraries](#72-frameworks--libraries)
- [8. Database Techniques (R13, R14, R15)](#8-database-techniques-r13-r14-r15)
  - [8.1 Indexing (R13)](#81-indexing-r13)
  - [8.2 Prepared Statements (R14)](#82-prepared-statements-r14)
  - [8.3 Transactions (R15)](#83-transactions-r15)
- [9. Contributions](#9-contributions)

## 1. Title: GradXplorer <span style="color:red">(R1, R2)</span>
**Navigate academia, discover top schools, and find leading researchers with ease!**

All the datasets and code used are available in this repository.

## 2. Purpose <span style="color:red">(R4, R5)</span>

### 2.1 Application Scenario
Students preparing for graduate school applications often struggle to find reliable information on:  
- **Top universities** in their fields of interest
- **Leading researchers** and their affiliated institutions
- **Trending academic topics** shaping research today

**GradXplorer** centralizes this information, making it accessible and easy to explore.

### 2.2 Target Users
- **Undergraduate students** considering graduate school
- **Researchers** seeking collaboration opportunities
- **Professionals** exploring further education in academia

### 2.3 Objectives
- **Guide** users in identifying the best academic programs for their field.
- **Highlight** influential researchers and their contributions.
- **Assist** potential scholars in understanding the current trending topics.

Stay ahead in the academic world with **GradXplorer**!


## 3. Demo <span style="color:red">(R3)</span>
**Link to video demo:** https://mediaspace.illinois.edu/media/t/1_gezkl50u


## 4. Installation <span style="color:red">(R6, R7, R8)</span>
Only the given datasets (MySQL from MP4, MongoDB from MP3, and Neo4j from MP3) are used for this application. For environment setup, there are two options available below. After installation, simply run the third command below to start the application.

### 4.1 Option 1: Install Packages from requirements.txt
```bash
pip install -r requirements.txt
```

### 4.2 Option 2: Use Conda Environment from environment.yml
```bash
conda env create -f environment.yml
conda activate cs411
```

### 4.3 Run the Application
```bash
python app/app.py
```


## 5. Usage <span style="color:red">(R9, R12)</span>
**GradXplorer** provides an intuitive web-based interface for exploring academic data. After running the main entry file `app.py`, the application will launch at [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

### 5.1 Widget 1: Top 10 Trending Keywords in Publications <span style="color:red">(R6, R7, R11)</span>
This widget provides a high-level view of research trends by displaying the top 10 trending keywords for a selected year. 

Users can choose from one of the two database sources and adjust the slider to specify a year, and the widget will update accordingly.

Database **MongoDB** and **MySQL** are used to store and retrieve this data.

### 5.2 Widget 2: User-selected Favorite Keywords <span style="color:red">(R6, R11)</span>
After viewing the top 10 trending keywords, users can configure their favorite keywords from the list for further research. 

By default, the selection includes five pre-selected AI-related themes, and users can add or remove favorite keywords as needed. In addition, a pie chart will reflect the current selection in real-time.

This control widget will also change the input keywords selection for **Widget 3** and **Widget 4** below.

Database **MySQL** is used to store and retrieve this data.

### 5.3 Widget 3: Faculty Members Relevant to Selected Keywords <span style="color:red">(R6, R10, R11)</span>
Using the configured keyword selection dynamically generated by **Widget 2**, this widget lists all relevant faculty members and their affiliated universities.

Users can also **delete or restore faculty records** in the backend database during research and selection. A separate viewer provides a real-time count of faculty members currently in the database, reflecting these changes dynamically. These updates will impact the backend database **MySQL**.

Database **MySQL** is used to store and retrieve this data.

### 5.4 Widget 4: Faculty Members with the Highest KRC for Selected Keywords <span style="color:red">(R6, R7, R11)</span>
This widget helps identify top faculty members based on their **Keyword-Relevant Citation (KRC) score**. 

Users can choose from one of the two database sources, select a pre-selected keyword dynamically generated by **Widget 2**, and pick a university to view faculty with the highest KRC scores in the selected field.

Database **MongoDB** and **MySQL** are used to store and retrieve this data.

### 5.5 Widget 5: Top 10 Keywords in Faculty Interests from Selected Universities <span style="color:red">(R8, R10, R11)</span>
This widget identifies the most common research keywords among faculty at a specific university, complementing the insights from **Widget 1**.

Users can also **delete or restore keywords** in the backend database, with real-time updates displayed in a separate viewer that tracks the number of keywords currently stored in the database. These updates will impact the backend database **Neo4j**.

Database **Neo4j** is used to store and retrieve this data.

### 5.6 Widget 6: Top 10 Universities Collaborated with Selected Universities <span style="color:red">(R6, R8, R11)</span>
This widget visualizes institutional research collaborations. Specifically, users can select a university to view its **top 10 collaborating institutions** including the number of coauthors, helping them understand academic partnerships and research networks.

Users can also click on the generated sunburst chart to view basic information about the selected university, including its name, total faculty count, and logo if available. For universities with strong CS programs, the $\frac{\text{number of coauthors}}{\text{total faculty count}}$ ratio among their collaborating institutions is usually higher.

Database **Neo4j** and **MySQL** are used to store and retrieve this data.


## 6. Design

**GradXplorer** follows a **dashboard-driven** approach using Dash Plotly to present interactive data visualizations. Overall, the application is structured using a **three-tier architecture**:

### 6.1 Frontend (Dash Plotly) <span style="color:red">(R9, R12)</span>
Provides an interactive user interface with data filtering and visualization features. This is achieved through a combination of **six** Dash widgets, including bar charts, pie charts, data tables, and sunburst charts. They are arranged in a rectangular layout that is aesthetically pleasing and easy to navigate.

### 6.2 Middle Layer (Flask & Python)
Handles business logic, processes user requests, and acts as an intermediary between the frontend and the database. More details on the middle layer can be found in the **Implementation** section.

### 6.3 Database Layer (MySQL, MongoDB, Neo4j) <span style="color:red">(R6, R7, R8)</span>
Stores relational, document, and graph Academic World data for efficient retrieval. Specifically: widget 1 and 4 use **MongoDB**; widget 1, 2, 3, 4, and 6 use **MySQL**; widget 5 and 6 use **Neo4j**.


## 7. Implementation

### 7.1 Detailed Implementation

- `app.py` – Main entry point for the application, structured using standard Dash app logic: app initialization, database initialization, layout setting, callback functions, and application execution. Most functions are defined in separate files to follow good software engineering practices and modularization.
- `mysql_utils.py` – Defines functions to connect and disconnect from MySQL, as well as functions for querying, deleting, and restoring backend data.
- `mongodb_utils.py` – Defines functions to connect and disconnect from MongoDB, along with functions for querying backend data.
- `neo4j_utils.py` – Defines functions to connect and disconnect from Neo4j, as well as functions for querying, deleting, and restoring backend data.
- `layout_utils.py` – Defines various Python classes to construct configurable widgets for reusability, including `GraphWidget`, `ControlWidget`, `TableWidget`, `CountDisplayWidget`, `DeleteWidget`, `RestoreWidget`, and `RefreshWidget`.
- `layout.py` – Uses self-defined widget classes to structure the actual application layout; also provides various IDs for each widget.
- `callbacks-utils.py` – Contains helper functions for various graphing functions used in `callbacks.py`, including `create_bar_chart`, `create_pie_chart`, `create_data_table`, `create_sunburst_chart`, `create_section_header`, and `create_info_table`.
- `callbacks.py` – Applies the callback decorator to the functions from the aforementioned `*_utils.py` files, linking them to the corresponding widgets through widget IDs from `layout.py`. This file contains all the callback functions that handle user interactions and update the dashboard accordingly.


### 7.2 Frameworks & Libraries
- **Pandas** – Used for DataFrame operations necessary to plot certain graphs.
- **Dash Plotly** – Used for building interactive dashboards.
- **Flask** – Handles backend logic and API requests.  
- **Database-related Frameworks** – Libraries used to interact with backend databases: `mysql.connector`, `pymongo`, and `neo4j`.


## 8. Database Techniques <span style="color:red">(R13, R14, R15)</span>

### 8.1 Indexing <span style="color:red">(R13)</span>
- `mongodb_utils.py` constructs indexes to optimize query performance for the following two functions:
  - `find_most_popular_keywords_mongo(year)`
  - `find_top_faculties_with_highest_KRC_keyword(keyword, affiliation)`
- `mysql_utils.py` also constructs indexes to optimize query performance for the following function:
  - `find_most_popular_keywords_sql(year)`

### 8.2 Prepared Statements <span style="color:red">(R14)</span>
- `mysql_utils.py` applies prepared statements to prevent **SQL injection attacks** by separating query logic from input parameters:
  - `find_faculty_relevant_to_keyword(keyword: str)`

### 8.3 Transactions <span style="color:red">(R15)</span>
- `mysql_utils.py` uses transactions during deletion and restoration to ensure **atomicity**, maintain **data consistency**, and provide **isolation**:
  - `delete_faculty(faculty_id)`
  - `restore_faculty()`
- `neo4j_utils.py` also uses transactions during deletion and restoration for the following functions:
  - `delete_keyword(keyword_id)`
  - `restore_keyword()`


## 9. Contributions
**This app is solely developed by Ningyuan Xie.**
