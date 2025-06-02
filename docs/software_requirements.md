# Software Requirements Specification
Version 1.0 -- 2.06.2025

## 1. Introduction
### 1.1 Purpose

The purpose of this document is definint the requirements for a **Movie Recommendations System**.

This project itself consists in the realization of a web app used for movie recommendations based on the users input.
The main users of the app will be people on the internet looking for recommendations based on their personal preference, with the aim to give them tailored results.

Our project has an **Machine Learning** core, and is part of a data-driven solution.

The aim of this document is guinding software development so that the system is designed efficiently and serves as a reference not only for the development team but also for the stakeholders.

### 1.2 Scope

The scope of this specification includes:
- architecture of the system
- functional and non-functional requirements
- assumptions, contraints and dependecies

The scope of the software itself will be:
1. Searching and selecting movies using a search bar
2. Having in return some movies recommendations based on the previous choices
3. Having the opportunity to change selection, thus, also the output

What we will not provide is:
- a login system, we let the user interact directly with the site without authentication
- no real-time rating updates, given that all our data comes a pre-existing dataset


### 1.3 Definitions

In this document, we will make use of several definitions:
- ML - Machine Learning
- UI - User Interface
- API - Application Programming Interface
- Streamlit - Python library for creating web apps


### 1.4 Intended Audience for this Document
This document is meant to be useful for:
- developers working on the web app, in order to guide the implementation
- ML engineers to align the model output with what we expect to provide to the users
- project reviewers as a guide for evaluation
- anyone that could need it for along-the-line maintanance

## 2. Overall Description
### 2.1 Product Perspective
This webapp is designed to be a standalone project, with a sufficiently simple client-server architecture.

We expect the frontend to be built using **Streamlit**, and to allow users to interact with the webapp by selecting movies.

The backend will then process this selections using a pre-trained, or an online learning, machine learning model (to be defined), that returns movie reccomendations based on the similarity to the users' choices.


### 2.2 Product Functions
As far as *how* the product will work for the users go:
- users will be able to select 5 to 10 movies they enjoy from a premade list (possibly, a search bar)
- the system will then generate a certain number of recommended movies using a ML model
- the recommended movies will then be displayed, possibly along some metadata (title of course, but also genre, rating...)
- users will then have the opportunity to refresh and also modify their selection


### 2.3 User Characteristics
We expect the end users of our system to be:
- **Casual Movie Watchers**: no technical background, so they would probably expect a simple and intuitive system for movie recommendations (hence, no login needed)
- **Project Reviewers**: technical people of the team, who may inspect technical aspects such as performance and usability
- **Developers and maintainers**: also technical people that may refer to the system design for debugging



### 2.4 Constraints
We have to work within several constraints:
- dataset must be preloaded 
- *performance contraints*: model response time should not surpass a few seconds
- no user authentication needed and the application should be publicly accessible


### 2.5 Assumptions and Dependencies

For development, we assume:
1. all team members use Github for version control and collaboration, and Github Projects as far as organizing the work goes
2. required Python packages will be installable via `requirements.txt`
3. the dataset will be clean, preprocessed and suitable for training and testing

For users, we assume:
1. access to a modern browser
2. a stable internet connection


## 3. Specific Requirements
### 3.1 Functional Requirements

There are several **core functional requirements**:
1. The system shall allow users to select 5 to 10 movies from a predefined list
2. The system shall generate and return at least 5 movie recommendations based on previous selections
3. The system sgall display the recommended movies providing the titles and possibly also the gerne, average rating, and a poster image
4. The system shall allow users to change their selection and re-run the recommendation
5. The system shall dynamically load movie data from a preprocessed dataset

Some *nice-to-have* requirements could be:
1. The system may allow filtering recommendations
2. The system may allow sorting recommendations
3. The system may display a similarity score next to each recommendation

The next section is then dedicated to **non-functional requirements**:

### 3.2 Performance Requirements
1. The system shall return recommendations within 2/3 seconds
2. The webapp shall be available for at least 99% of the time during the day
3. The system shall support at least 5 or more concurrent users without degredation of response time


### 3.3 Interface Requirements

1. The UI shall allow users to multi-select 5 to 10 movies from a searchable dropdown menu (or similar)
2. The interface shall display recommended movies, along with some information
3. The app shall show clear error messages when necessary
4. The interface shall be usable on both desktop and mobile

### 3.4 Operational Requirements

1. The model and data shall not require external APIs
2. The system shall not require user accounts or persistent data storage
3. The environment dependencies shall be defined in a `requirements.txt` file

### 3.5 Security Requirements

1. The app shall not accept executable code or scripts as user input
2. All inputs shall be sanitazied and validated before preprocessing
3. The codebase shall not expose anything internal
4. The app shall use public dataset and no personal data

### 3.6 Software Quality Attributes
There are several quality attributes we expect the software to have:
1. **Usability**: the UI shall be minimal and intuitive, with clear instructions and visual feedback
2. **Reliability**: recommendations must always be return (excluding the case of backend failure, in which case the user should be return a feedback)
3. **Availability**: the app should be available for at least 99% of the time of a day
4. **Scalability**: the architecture shall allow the scaling to larger datasets and/or more users if needed
5. **Maintainability**: code shall be **modular** and follow **naming standards**
6. **Performance**: as discussed previously, model response time should stay under 3 seconds (given the current dataset)
7. **Secutiry**: all input have to be validated and to sensitive data stored or transmitted
8. **Reusability**: the model and UI logic shall be written as modular functions and thus, reusable


## 4. Supporting Information
### 4.1 Appendices
As far as the preliminary decisions go, no APIs will be needed.

### 4.2 Index

Appendices – 4.1  
Assumptions – 2.5  
Constraints – 2.4  
Dataset – 2.4, 3.1, 3.4  
Definitions, Acronyms and Abbreviations – 1.3  
Dependencies – 2.5  
Error Handling – 3.3  
Functional Requirements – 3.1  
Interface – 3.3  
Machine Learning – 1.1, 2.1  
Maintainability – 3.6  
Non-Functional Requirements – 3.2–3.6  
Performance – 3.2, 3.6  
Project Scope – 1.2  
Security – 3.5, 3.6  
Software Architecture – 2.1  
Software Quality Attributes – 3.6  
Stakeholders – 1.4, 2.3  
Streamlit – 1.3, 2.1  
Usability – 3.6  
User Characteristics – 2.3  
User Interface – 2.2, 3.3  
Version Control – 2.5  
