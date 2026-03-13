Multi-User Python Todo CLI

A Command Line Interface (CLI) Todo application built with Python. This project features user management, task persistence via JSON, and basic sorting/filtering capabilities.

## 🚀 Features
* **User Management:** Create, delete, and switch between multiple user profiles.
* **Persistent Storage:** Each user has their own dedicated `.json` file for data persistence.
* **Task Customization:** Add tasks with priorities (1-5), tags, and optional due dates.
* **Smart Organization:** Sort tasks by priority, creation date, or due date.
    * Filter tasks by specific tags.
* **Data Integrity:** Uses a generic `JSONStorage` class with object injection for reusable data handling.
