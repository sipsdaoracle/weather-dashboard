import os
import json
import logging
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.s3_client = boto3.client('s3', region_name=self.aws_region)

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logging.info(f"Bucket {self.bucket_name} exists.")
        except:
            logging.info(f"Creating bucket {self.bucket_name}.")
            try:
                self.s3_client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.aws_region
                    }
                )
                logging.info(f"Successfully created bucket {self.bucket_name}.")
            except Exception as e:
                logging.error(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data for {city}: {e}")
            return None

    def save_to_s3_as_csv(self, weather_data, city):
        """Save weather data to S3 bucket in CSV format and generate manifest file"""
        if not weather_data:
            return False

        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.csv"

        # Prepare CSV data
        csv_data = [
            [
                city,
                weather_data['main']['temp'],
                weather_data['main']['feels_like'],
                weather_data['main']['humidity'],
                weather_data['weather'][0]['description'],
                timestamp
            ]
        ]

        try:
            # Create CSV content
            csv_content = "city,temperature,feels_like,humidity,description,timestamp\n"
            for row in csv_data:
                csv_content += ','.join(map(str, row)) + '\n'

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=csv_content,
                ContentType='text/csv'
            )
            logging.info(f"Successfully saved CSV data for {city} to S3.")

            # Generate and upload the manifest file
            self.generate_and_upload_manifest(file_name)

            return True
        except Exception as e:
            logging.error(f"Error saving weather data for {city} to S3: {e}")
            return False

    def generate_and_upload_manifest(self, file_key):
        """Generate and upload a manifest file for QuickSight"""
        manifest_data = {
            "fileLocations": [
                {
                    "URIs": [
                        f"https://{self.bucket_name}.s3.{self.aws_region}.amazonaws.com/{file_key}"
                    ]
                }
            ],
            "globalUploadSettings": {
                "format": "CSV"
            }
        }

        manifest_file_name = f"weather-data/manifest.json"

        try:
            # Convert manifest data to JSON string
            manifest_content = json.dumps(manifest_data, indent=2)

            # Upload the manifest to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=manifest_file_name,
                Body=manifest_content,
                ContentType='application/json'
            )
            logging.info(f"Manifest file successfully uploaded to S3 as {manifest_file_name}.")
        except Exception as e:
            logging.error(f"Error generating or uploading manifest file: {e}")


def main():
    logging.info("Starting Weather Dashboard...")
    dashboard = WeatherDashboard()

    # Create S3 bucket if needed
    dashboard.create_bucket_if_not_exists()

    cities = ["Philadelphia", "Seattle", "New York"]

    for city in cities:
        logging.info(f"Fetching weather data for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']

            logging.info(f"Weather data for {city}:")
            logging.info(f"  Temperature: {temp}°F")
            logging.info(f"  Feels like: {feels_like}°F")
            logging.info(f"  Humidity: {humidity}%")
            logging.info(f"  Conditions: {description}")

            # Save to S3 as CSV
            success = dashboard.save_to_s3_as_csv(weather_data, city)
            if success:
                logging.info(f"Weather data for {city} successfully saved to S3.")
        else:
            logging.warning(f"Failed to fetch weather data for {city}.")


if __name__ == "__main__":
    main()
