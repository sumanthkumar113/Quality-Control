Query Interface (Flask App): This Flask application allows users to search through the ingested logs. It offers functionalities to filter based on:
Log level (error, info, success)
Log message text
Timestamp range
Source API
Regular expressions (optional)
Features Implemented:

Log storage in separate JSON files based on source.
Search functionality across all logs.
Filtering by level, log message text, timestamp range, and source.
Support for regular expressions in search (optional, based on a checkbox selection).
User interface for search queries and displaying results in a table.

Open a terminal and navigate to the project directory.
Run the following command: python app.py
This will start the Flask development server, usually accessible at http://127.0.0.1:5000/ in your web browser.
