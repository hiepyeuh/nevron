# from io import BytesIO
# from unittest.mock import AsyncMock, MagicMock, patch
# import pytest
# from loguru import logger
# from PIL import Image
# from requests_html import HTMLSession
# import tweepy

# from src.core.exceptions import TwitterError
# from src.tools.twitter import (
#     get_twitter_conn_v1,
#     get_twitter_conn_v2,
#     upload_media_v1,
#     post_twitter_thread,
# )


# @pytest.fixture
# def mock_tool_logger(monkeypatch):
#     """Mock logger for tool testing."""
#     mock_debug = MagicMock()
#     mock_error = MagicMock()
#     monkeypatch.setattr(logger, "debug", mock_debug)
#     monkeypatch.setattr(logger, "error", mock_error)
#     return mock_debug, mock_error


# @pytest.fixture
# def mock_twitter_settings():
#     """Mock Twitter API settings."""
#     with patch("src.tools.twitter.settings") as mock_settings:
#         mock_settings.TWITTER_API_KEY = "test_api_key"
#         mock_settings.TWITTER_API_SECRET_KEY = "test_api_secret"
#         mock_settings.TWITTER_ACCESS_TOKEN = "test_access_token"
#         mock_settings.TWITTER_ACCESS_TOKEN_SECRET = "test_access_secret"
#         return mock_settings


# @pytest.fixture
# def mock_tweepy_v1():
#     """Mock Tweepy API v1.1 client."""
#     mock_auth = MagicMock()
#     mock_client = MagicMock()

#     with patch("tweepy.OAuth1UserHandler", return_value=mock_auth) as mock_handler, \
#          patch("tweepy.API", return_value=mock_client) as mock_api:
#         mock_auth.set_access_token = MagicMock()
#         yield mock_client


# @pytest.fixture
# def mock_tweepy_v2():
#     """Mock Tweepy API v2 client."""
#     with patch("tweepy.Client") as mock_client_class:
#         mock_client = MagicMock()
#         mock_client_class.return_value = mock_client
#         return mock_client


# def test_get_twitter_conn_v1(mock_twitter_settings, mock_tweepy_v1):
#     """Test Twitter API v1.1 connection creation."""
#     with patch("tweepy.OAuth1UserHandler") as mock_handler:
#         mock_auth = MagicMock()
#         mock_handler.return_value = mock_auth

#         # act:
#         client = get_twitter_conn_v1()

#         # assert:
#         mock_handler.assert_called_once_with(
#             mock_twitter_settings.TWITTER_API_KEY,
#             mock_twitter_settings.TWITTER_API_SECRET_KEY
#         )
#         mock_auth.set_access_token.assert_called_once_with(
#             mock_twitter_settings.TWITTER_ACCESS_TOKEN,
#             mock_twitter_settings.TWITTER_ACCESS_TOKEN_SECRET
#         )
#         tweepy.API.assert_called_once_with(mock_auth)


# def test_get_twitter_conn_v2(mock_twitter_settings, mock_tweepy_v2):
#     """Test Twitter API v2 connection creation."""
#     # act:
#     client = get_twitter_conn_v2()

#     # assert:
#     assert client == mock_tweepy_v2
#     tweepy.Client.assert_called_once_with(
#         consumer_key=mock_twitter_settings.TWITTER_API_KEY,
#         consumer_secret=mock_twitter_settings.TWITTER_API_SECRET_KEY,
#         access_token=mock_twitter_settings.TWITTER_ACCESS_TOKEN,
#         access_token_secret=mock_twitter_settings.TWITTER_ACCESS_TOKEN_SECRET,
#     )


# @pytest.mark.asyncio
# async def test_upload_media_v1_success(mock_tool_logger, mock_tweepy_v1):
#     """Test successful media upload."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     url = "http://example.com/image.jpg"
#     media_id = "12345"

#     # Mock HTML session
#     mock_session = MagicMock()
#     mock_response = MagicMock()
#     mock_response.content = b"fake_image_data"
#     mock_session.get.return_value = mock_response

#     # Mock image processing
#     mock_image = MagicMock(spec=Image.Image)
#     mock_image.convert.return_value = mock_image

#     # Mock media upload
#     mock_media = MagicMock()
#     mock_media.media_id = media_id
#     mock_tweepy_v1.media_upload.return_value = mock_media

#     with patch("src.tools.twitter.HTMLSession", return_value=mock_session), \
#          patch("src.tools.twitter.Image.open", return_value=mock_image), \
#          patch("src.tools.twitter.get_twitter_conn_v1", return_value=mock_tweepy_v1):
#         # act:
#         result = await upload_media_v1(url)

#     # assert:
#     assert result == media_id
#     mock_session.get.assert_called_once_with(url, headers=pytest.ANY)
#     mock_image.convert.assert_called_once_with("L")
#     mock_tweepy_v1.media_upload.assert_called_once()
#     mock_debug.assert_called_once()
#     mock_error.assert_not_called()


# @pytest.mark.asyncio
# async def test_upload_media_v1_error(mock_tool_logger):
#     """Test media upload error handling."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     url = "http://example.com/image.jpg"

#     # Mock session with error
#     mock_session = MagicMock()
#     mock_session.get.side_effect = Exception("Network error")

#     with patch("src.tools.twitter.HTMLSession", return_value=mock_session):
#         # act:
#         result = await upload_media_v1(url)

#     # assert:
#     assert result is None
#     mock_error.assert_called_once()
#     mock_debug.assert_not_called()


# @pytest.mark.asyncio
# async def test_post_twitter_thread_success(mock_tool_logger, mock_tweepy_v2):
#     """Test successful thread posting."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     tweets = {
#         "tweet1": "First tweet",
#         "tweet2": "Second tweet"
#     }
#     tweet_ids = [12345, 67890]

#     # Mock tweet responses
#     mock_tweepy_v2.create_tweet.side_effect = [
#         MagicMock(data={"id": tweet_id}) for tweet_id in tweet_ids
#     ]

#     with patch("src.tools.twitter.get_twitter_conn_v2", return_value=mock_tweepy_v2), \
#          patch("asyncio.sleep"):  # Mock sleep to speed up test
#         # act:
#         result = await post_twitter_thread(tweets)

#     # assert:
#     assert result == tweet_ids
#     assert mock_tweepy_v2.create_tweet.call_count == 2
#     mock_debug.assert_called()
#     mock_error.assert_not_called()


# @pytest.mark.asyncio
# async def test_post_twitter_thread_with_media(
#     mock_tool_logger, mock_tweepy_v1, mock_tweepy_v2
# ):
#     """Test thread posting with media."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     tweets = {"tweet1": "Tweet with media"}
#     media_url = "http://example.com/image.jpg"
#     tweet_id = 12345
#     media_id = "67890"

#     # Mock media upload
#     with patch("src.tools.twitter.upload_media_v1", return_value=media_id):
#         # Mock tweet creation
#         mock_tweepy_v2.create_tweet.return_value = MagicMock(data={"id": tweet_id})

#         with patch("src.tools.twitter.get_twitter_conn_v2", return_value=mock_tweepy_v2), \
#              patch("asyncio.sleep"):
#             # act:
#             result = await post_twitter_thread(tweets, media_url=media_url)

#         # assert:
#         assert result == [tweet_id]
#         mock_tweepy_v2.create_tweet.assert_called_once_with(
#             text=tweets["tweet1"],
#             media_ids=[media_id]
#         )


# @pytest.mark.asyncio
# async def test_post_twitter_thread_error(mock_tool_logger, mock_tweepy_v2):
#     """Test error handling in thread posting."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     tweets = {"tweet1": "Test tweet"}
#     mock_tweepy_v2.create_tweet.side_effect = Exception("API Error")

#     with patch("src.tools.twitter.get_twitter_conn_v2", return_value=mock_tweepy_v2), \
#          pytest.raises(TwitterError):
#         # act:
#         await post_twitter_thread(tweets)

#     # assert:
#     mock_error.assert_called_once()
#     mock_debug.assert_not_called()
