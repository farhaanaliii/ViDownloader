"""
Unit tests for vidownloader.core.http module.
Tests HTTP request functionality, retry logic, and error handling.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from vidownloader.core.http import (
    get, post, head,
    _should_retry, _calculate_delay,
    ConnectionError, TimeoutError,
    DEFAULT_RETRYABLE_CODES
)


class TestRetryLogic:
    """Tests for retry logic helper functions."""

    def test_should_retry_with_default_codes(self):
        """Test retry logic with default retryable codes."""
        assert _should_retry(429) is True
        assert _should_retry(500) is True
        assert _should_retry(503) is True
        assert _should_retry(404) is False
        assert _should_retry(200) is False

    def test_should_retry_with_custom_codes(self):
        """Test retry logic with custom retryable codes."""
        custom_codes = [400, 404]
        assert _should_retry(404, custom_codes) is True
        assert _should_retry(500, custom_codes) is False

    def test_calculate_delay_exponential_backoff(self):
        """Test exponential backoff calculation."""
        delay_0 = _calculate_delay(0, base_delay=1.0, backoff_factor=2.0)
        delay_1 = _calculate_delay(1, base_delay=1.0, backoff_factor=2.0)
        delay_2 = _calculate_delay(2, base_delay=1.0, backoff_factor=2.0)
        
        assert delay_0 == 1.0
        assert delay_1 == 2.0
        assert delay_2 == 4.0

    def test_calculate_delay_respects_max_delay(self):
        """Test that calculated delay respects max_delay."""
        delay = _calculate_delay(10, base_delay=1.0, max_delay=10.0, backoff_factor=2.0)
        assert delay == 10.0

    def test_calculate_delay_custom_parameters(self):
        """Test delay calculation with custom parameters."""
        delay = _calculate_delay(2, base_delay=0.5, backoff_factor=3.0)
        assert delay == 0.5 * (3.0 ** 2)


class TestHttpGet:
    """Tests for the GET request function."""

    @patch('vidownloader.core.http.curl_requests.request')
    def test_get_successful_request(self, mock_request):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        
        response = get("https://example.com")
        
        assert response == mock_response
        mock_request.assert_called_once()

    @patch('vidownloader.core.http.curl_requests.request')
    def test_get_with_params(self, mock_request):
        """Test GET request with query parameters."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        params = {"key": "value", "foo": "bar"}
        get("https://example.com", params=params)
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["params"] == params

    @patch('vidownloader.core.http.curl_requests.request')
    def test_get_with_custom_headers(self, mock_request):
        """Test GET request with custom headers."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        headers = {"User-Agent": "Test Agent"}
        get("https://example.com", headers=headers)
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["headers"] == headers

    @patch('vidownloader.core.http.curl_requests.request')
    @patch('vidownloader.core.http.time.sleep')
    def test_get_retries_on_retryable_status(self, mock_sleep, mock_request):
        """Test that GET retries on retryable status codes."""
        mock_response_fail = Mock()
        mock_response_fail.ok = False
        mock_response_fail.status_code = 503
        
        mock_response_success = Mock()
        mock_response_success.ok = True
        mock_response_success.status_code = 200
        
        mock_request.side_effect = [mock_response_fail, mock_response_success]
        
        response = get("https://example.com", retries=2)
        
        assert response == mock_response_success
        assert mock_request.call_count == 2
        mock_sleep.assert_called_once()

    @patch('vidownloader.core.http.curl_requests.request')
    def test_get_raises_on_non_retryable_status(self, mock_request):
        """Test that GET raises on non-retryable status codes."""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.raise_for_status = Mock(side_effect=Exception("Not Found"))
        mock_request.return_value = mock_response
        
        with pytest.raises(Exception):
            get("https://example.com", retries=2)


class TestHttpPost:
    """Tests for the POST request function."""

    @patch('vidownloader.core.http.curl_requests.request')
    def test_post_with_data(self, mock_request):
        """Test POST request with form data."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        data = {"key": "value"}
        post("https://example.com", data=data)
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["data"] == data
        assert call_kwargs["method"] == "POST"

    @patch('vidownloader.core.http.curl_requests.request')
    def test_post_with_json(self, mock_request):
        """Test POST request with JSON payload."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        json_data = {"key": "value", "number": 123}
        post("https://example.com", json_data=json_data)
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["json"] == json_data


class TestHttpHead:
    """Tests for the HEAD request function."""

    @patch('vidownloader.core.http.curl_requests.request')
    def test_head_request(self, mock_request):
        """Test HEAD request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        response = head("https://example.com")
        
        assert response == mock_response
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["method"] == "HEAD"


class TestErrorHandling:
    """Tests for error handling."""

    @patch('vidownloader.core.http.curl_requests.request')
    def test_timeout_error_handling(self, mock_request):
        """Test timeout error is properly handled."""
        from curl_cffi.requests import RequestsError
        
        mock_request.side_effect = RequestsError("timeout occurred")
        
        with pytest.raises(TimeoutError, match="Request timed out"):
            get("https://example.com", retries=0)

    @patch('vidownloader.core.http.curl_requests.request')
    def test_connection_error_handling(self, mock_request):
        """Test connection error is properly handled."""
        from curl_cffi.requests import RequestsError
        
        mock_request.side_effect = RequestsError("connect failed")
        
        with pytest.raises(ConnectionError, match="Connection failed"):
            get("https://example.com", retries=0)

    @patch('vidownloader.core.http.curl_requests.request')
    @patch('vidownloader.core.http.time.sleep')
    def test_retry_on_exception(self, mock_sleep, mock_request):
        """Test that requests retry on exceptions."""
        from curl_cffi.requests import RequestsError
        
        mock_response = Mock()
        mock_response.ok = True
        
        mock_request.side_effect = [
            RequestsError("temporary error"),
            mock_response
        ]
        
        response = get("https://example.com", retries=2)
        
        assert response == mock_response
        assert mock_request.call_count == 2
        mock_sleep.assert_called_once()

    @patch('vidownloader.core.http.curl_requests.request')
    def test_exhausted_retries_raises_error(self, mock_request):
        """Test that exhausted retries raises the last error."""
        from curl_cffi.requests import RequestsError
        
        mock_request.side_effect = RequestsError("persistent error")
        
        with pytest.raises(Exception):
            get("https://example.com", retries=2)
        
        assert mock_request.call_count == 3


class TestRequestOptions:
    """Tests for various request options."""

    @patch('vidownloader.core.http.curl_requests.request')
    def test_follow_redirects_option(self, mock_request):
        """Test that follow_redirects option is passed."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        get("https://example.com", follow_redirects=False)
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["allow_redirects"] is False

    @patch('vidownloader.core.http.curl_requests.request')
    def test_verify_ssl_option(self, mock_request):
        """Test that verify_ssl option is passed."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        get("https://example.com", verify_ssl=False)
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["verify"] is False

    @patch('vidownloader.core.http.curl_requests.request')
    def test_timeout_option(self, mock_request):
        """Test that timeout option is passed."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        get("https://example.com", timeout=60)
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["timeout"] == 60

    @patch('vidownloader.core.http.curl_requests.request')
    def test_impersonate_chrome(self, mock_request):
        """Test that requests impersonate Chrome."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        get("https://example.com")
        
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["impersonate"] == "chrome"
