import time
from typing import Union

from curl_cffi import requests as curl_requests
from curl_cffi.requests import RequestsError, Response


class ConnectionError(Exception):
    """Exception raised for connection-related errors."""

    pass


class TimeoutError(Exception):
    """Exception raised when a request times out."""

    pass


DEFAULT_RETRYABLE_CODES = [429, 500, 502, 503, 504, 520, 521, 522, 523, 524]


def _should_retry(status_code: int, retryable_codes: list = None) -> bool:
    """Determine if a request should be retried based on the status code."""
    if retryable_codes is None:
        retryable_codes = DEFAULT_RETRYABLE_CODES
    return status_code in retryable_codes


def _calculate_delay(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
) -> float:
    """Calculate the delay for the next retry attempt using exponential backoff."""
    delay = base_delay * (backoff_factor**attempt)
    return min(delay, max_delay)


def _make_request(
    url: str,
    method: str = "GET",
    data: Union[dict, str, bytes] = None,
    json_data: dict = None,
    headers: dict = None,
    params: dict = None,
    timeout: int = 30,
    retries: int = 0,
    retry_delay: float = 1.0,
    retry_backoff: float = 2.0,
    retry_max_delay: float = 60.0,
    retryable_codes: list = None,
    stream: bool = False,
    follow_redirects: bool = True,
    max_redirects: int = 10,
    verify_ssl: bool = True,
) -> Response:
    """
    Core HTTP request function using curl_cffi with retry logic.
    """
    last_exception = None

    for attempt in range(retries + 1):
        try:
            resp = curl_requests.request(
                method=method.upper(),
                url=url,
                params=params,
                headers=headers,
                data=data,
                json=json_data,
                timeout=timeout,
                allow_redirects=follow_redirects,
                max_redirects=max_redirects,
                verify=verify_ssl,
                stream=stream,
                impersonate="chrome",
            )

            if resp.ok:
                return resp

            if attempt < retries and _should_retry(resp.status_code, retryable_codes):
                delay = _calculate_delay(
                    attempt, retry_delay, retry_max_delay, retry_backoff
                )
                time.sleep(delay)
                continue

            resp.raise_for_status()

        except RequestsError as e:
            last_exception = e
            error_msg = str(e).lower()

            if "timeout" in error_msg:
                last_exception = TimeoutError(f"Request timed out: {e}")
            elif "connect" in error_msg or "resolve" in error_msg:
                last_exception = ConnectionError(f"Connection failed: {e}")

            if attempt < retries:
                delay = _calculate_delay(
                    attempt, retry_delay, retry_max_delay, retry_backoff
                )
                time.sleep(delay)
                continue

            raise last_exception

        except Exception as e:
            last_exception = e

            if attempt < retries:
                delay = _calculate_delay(
                    attempt, retry_delay, retry_max_delay, retry_backoff
                )
                time.sleep(delay)
                continue

            raise last_exception


def get(
    url: str,
    params: dict = None,
    headers: dict = None,
    timeout: int = 30,
    retries: int = 0,
    retry_delay: float = 1.0,
    retry_backoff: float = 2.0,
    retry_max_delay: float = 60.0,
    retryable_codes: list = None,
    follow_redirects: bool = True,
    verify_ssl: bool = True,
) -> Response:
    return _make_request(
        url=url,
        method="GET",
        params=params,
        headers=headers,
        timeout=timeout,
        retries=retries,
        retry_delay=retry_delay,
        retry_backoff=retry_backoff,
        retry_max_delay=retry_max_delay,
        retryable_codes=retryable_codes,
        follow_redirects=follow_redirects,
        verify_ssl=verify_ssl,
    )


def post(
    url: str,
    data: Union[dict, str, bytes] = None,
    json_data: dict = None,
    headers: dict = None,
    params: dict = None,
    timeout: int = 30,
    retries: int = 0,
    retry_delay: float = 1.0,
    retry_backoff: float = 2.0,
    retry_max_delay: float = 60.0,
    retryable_codes: list = None,
    follow_redirects: bool = True,
    verify_ssl: bool = True,
) -> Response:
    return _make_request(
        url=url,
        method="POST",
        data=data,
        json_data=json_data,
        params=params,
        headers=headers,
        timeout=timeout,
        retries=retries,
        retry_delay=retry_delay,
        retry_backoff=retry_backoff,
        retry_max_delay=retry_max_delay,
        retryable_codes=retryable_codes,
        follow_redirects=follow_redirects,
        verify_ssl=verify_ssl,
    )


def head(
    url: str,
    headers: dict = None,
    params: dict = None,
    timeout: int = 30,
    follow_redirects: bool = True,
    verify_ssl: bool = True,
) -> Response:
    return _make_request(
        url=url,
        method="HEAD",
        params=params,
        headers=headers,
        timeout=timeout,
        follow_redirects=follow_redirects,
        verify_ssl=verify_ssl,
    )
