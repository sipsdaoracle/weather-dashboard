import pytest
from unittest.mock import patch, MagicMock
from weather_dashboard import WeatherDashboard


@pytest.fixture
def dashboard():
    return WeatherDashboard()


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


def test_fetch_weather(dashboard):
    with patch("requests.get") as mock_get:
        # Mock API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"weather": [{"description": "clear"}]}

        result = dashboard.fetch_weather("Seattle")
        assert result["weather"][0]["description"] == "clear"


def test_save_to_s3(dashboard):
    with patch.object(dashboard.s3_client, "put_object") as mock_put:
        mock_put.return_value = MagicMock()

        weather_data = {"main": {"temp": 70}, "weather": [{"description": "clear"}]}
        success = dashboard.save_to_s3(weather_data, "Seattle")

        assert success
        mock_put.assert_called_once()
