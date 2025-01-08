import pytest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from weather_dashboard.weather_dashboard import WeatherDashboard


# Fixture to initialize the WeatherDashboard
@pytest.fixture
def dashboard():
    return WeatherDashboard()


# Test for create_bucket_if_not_exists function
def test_create_bucket_if_not_exists(dashboard):
    with patch.object(dashboard.s3_client, 'head_bucket') as mock_head, \
            patch.object(dashboard.s3_client, 'create_bucket') as mock_create:
        # Mock bucket exists
        mock_head.return_value = None
        dashboard.create_bucket_if_not_exists()
        mock_create.assert_not_called()

        # Mock bucket does not exist
        mock_head.side_effect = Exception("Bucket does not exist")
        dashboard.create_bucket_if_not_exists()
        mock_create.assert_called_once()


# Test for fetch_weather function (valid response)
def test_fetch_weather(dashboard):
    with patch("requests.get") as mock_get:
        # Mock API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"weather": [{"description": "clear"}]}

        result = dashboard.fetch_weather("Seattle")
        assert result["weather"][0]["description"] == "clear"


# Test for fetch_weather function (invalid response)
def test_fetch_weather_invalid_response(dashboard):
    with patch("requests.get") as mock_get:
        # Simulate a failed API call
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = None  # Mock json() to return None
        result = dashboard.fetch_weather("Seattle")
        assert result is None  # Check for fallback or appropriate handling


# Test for save_to_s3_as_csv function (successful upload)
def test_save_to_s3_as_csv(dashboard):
    with patch.object(dashboard.s3_client, "put_object") as mock_put:
        mock_put.return_value = MagicMock()

        weather_data = {"main": {"temp": 70}, "weather": [{"description": "clear"}]}
        success = dashboard.save_to_s3_as_csv(weather_data, "Seattle")

        assert success
        mock_put.assert_called_once()


# Test for save_to_s3_as_csv function (S3 upload failure)
def test_save_to_s3_as_csv_error(dashboard):
    with patch.object(dashboard.s3_client, "put_object") as mock_put:
        # Simulate an S3 error
        mock_put.side_effect = Exception("S3 upload failed")
        weather_data = {"main": {"temp": 70}, "weather": [{"description": "clear"}]}
        success = dashboard.save_to_s3_as_csv(weather_data, "Seattle")
        assert not success


# Test for environment variable setup (AWS credentials)
def test_aws_environment_variables(dashboard):
    with patch.dict("os.environ", {"AWS_ACCESS_KEY_ID": "fake_key", "AWS_SECRET_ACCESS_KEY": "fake_secret"}):
        # Mock API response for weather data
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"weather": [{"description": "clear"}]}

            # Mock S3 put_object method
            with patch.object(dashboard.s3_client, "put_object") as mock_put:
                mock_put.return_value = MagicMock()

                weather_data = {"main": {"temp": 70}, "weather": [{"description": "clear"}]}
                success = dashboard.save_to_s3_as_csv(weather_data, "Seattle")

                assert success
                mock_put.assert_called_once()


# Test for bucket creation when environment variables are missing
def test_missing_aws_credentials(dashboard):
    with patch.dict("os.environ", {}):  # Clear out AWS credentials
        with pytest.raises(KeyError, match="AWS_ACCESS_KEY_ID"):
            dashboard.create_bucket_if_not_exists()
