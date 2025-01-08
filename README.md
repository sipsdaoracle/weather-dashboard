# 30 Days DevOps Challenge - Weather Dashboard

Day 1: Building a weather data collection system using AWS S3 and OpenWeather API

# Weather Data Collection System - DevOps Day 1 Challenge

## Project Overview
This project is a Weather Data Collection System that demonstrates core DevOps principles by combining:
- External API Integration **(OpenWeather API)**
- Cloud Storage **(AWS S3)**
- Version Control **(Git)**
- Automated Testing
- CI/CD Pipeline
- Data Visualization **(AWS QuickSight)**
- Python Development
- Error Handling
- Environment Management

## Features
- Fetches real-time weather data for multiple cities
- Displays temperature (°F), humidity, and weather conditions
- Automatically stores weather data in AWS S3
- Implements error logging for API fetch and S3 upload failures
- Provides visualizations of historical weather data using AWS QuickSight
- Includes automated unit tests with mocking for error scenarios
- Uses a CI/CD pipeline for continuous integration and deployment
- Supports multiple cities tracking
- Timestamps all data for historical tracking

## Technical Architecture
- **Language:** Python 3.x
- **Cloud Provider:** AWS (S3)
- **External API:** OpenWeather API
- **Dependencies:** 
  - boto3 (AWS SDK)
  - python-dotenv
  - requests

## Project Structure
````
weather-dashboard/
  src/
    __init__.py
    weather_dashboard.py
  tests/
  data/
  .env
  .gitignore
  requirements.txt
  ````

## Setup Instructions
1. Clone the repository:
```git clone https://github.com/ShaeInTheCloud/30days-weather-dashboard.git```

2. Install dependencies:
``
 pip install -r requirements.txt
``
3. Configure environment variables (.env):
``` 
OPENWEATHER_API_KEY=your_api_key
AWS_BUCKET_NAME=your_bucket_name
```
5. Configure AWS credentials:
```aws configure```

6. Run the application:
```python src/weather_dashboard.py```

## What I Learned

1. **AWS S3 Bucket Management:**
   -  Creating and managing cloud storage in AWS for storing weather data.


2. **Environment Management:** 
   - Secure handling of API keys using .env files.


3. **Python** best practices for API integration


4. **CI/CD Pipelines:** 
   - Setting up automated testing and deployment with GitHub Actions.


5. **Data Visualization with AWS QuickSight:**
   - Building interactive dashboards for exploring historical weather data.


6. **Git workflow** for project development


7.  Automated testing


8. **Error Logging:** 
   - Implementing error handling and logging for API and cloud service failures.


9. **Cloud** resource management


## Future Enhancements

- Add weather forecasting
- Add more cities

## Demo
1. ![Screenshot (103).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28103%29.png)
2. **S3 Bucket:**
   3. ![Screenshot (104).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28104%29.png)
3. E**rror Logging Implented:**
   4. ![Screenshot (120).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28120%29.png)
4. **QuickSight and dataset setup:**
   5. ![Screenshot (122).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28122%29.png)
6. Visualization:
   7. ![Screenshot (123).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28123%29.png)
## Errors Encountered

### 1. AWS S3 Bucket Permissions Denied
    Problem: Encountered permission errors when attempting to upload data to AWS S3.

- Solution: The issue was resolved by ensuring the AWS IAM user had sufficient permissions,AmazonS3FullAccess, to allow data uploads.```

### 2.  Incorrect Data Formatting for AWS QuickSight
    Problem: Data uploaded to S3 was not properly formatted for use in AWS QuickSight, preventing data visualization.
- Solution:  Ensured that the datasource  was correctly formatted as (manifest file), which allowed QuickSight to process and visualize the data correctly.

### 3. Automated Testing Coverage and Setup Issues
    Problem: The initial setup for automated testing was incomplete, with insufficient test coverage.

- Solution: Expanded the test coverage, ensuring that various scenarios (e.g., API failures, empty data) are properly tested.```


