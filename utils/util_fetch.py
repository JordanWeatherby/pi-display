import json
import logging
import requests
import os
import time
import hashlib

CACHE_DIR = "cache"
CACHE_RETENTION_TIME = 86400  # 24 hours in seconds

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)


def _clear_old_caches():
    logging.info("Clearing old cache files...")
    now = time.time()
    for filename in os.listdir(CACHE_DIR):
        filepath = os.path.join(CACHE_DIR, filename)
        if os.path.isfile(filepath):
            try:
                if now - os.path.getmtime(filepath) > CACHE_RETENTION_TIME:
                    os.remove(filepath)
                    logging.info(f"Removed old cache file: {filepath}")
            except OSError as e:
                logging.warning(f"Error removing cache file {filepath}: {e}")


_clear_old_caches()


def _get_cache_filepath(url):
    # Create a simple hash of the URL for the filename
    return os.path.join(CACHE_DIR, hashlib.md5(url.encode()).hexdigest() + ".json")


def _save_to_cache(url, data):
    filepath = _get_cache_filepath(url)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"timestamp": time.time(), "data": data}, f)


def _load_from_cache(url, cache_timeout=300):
    filepath = _get_cache_filepath(url)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                cached_data = json.load(f)
                if time.time() - cached_data["timestamp"] < cache_timeout:
                    logging.info(f"Using cached data for {url}")
                    return cached_data["data"]
                else:
                    logging.info(f"Cached data for {url} is stale.")
            except json.JSONDecodeError:
                logging.warning(f"Error decoding cache file: {filepath}")
    return None


def fetch(url, cache_timeout=300):
    cached_result = _load_from_cache(url, cache_timeout)
    if cached_result:
        return cached_result

    try:
        r = requests.get(url)
        r.encoding = "utf-8"
        result = json.loads(r.text)
        _save_to_cache(url, result)
        return result
    except requests.exceptions.RequestException:
        logging.exception("Could not fetch: " + url)
        if cached_result:
            logging.info(f"Returning stale cached data for {url}")
            return cached_result
        return None


def fetch_with_headers_params(url, headers, params, cache_timeout=300):
    # For simplicity, combine URL, headers, and params into a single string for caching key
    cache_key = (
        url + json.dumps(headers, sort_keys=True) + json.dumps(params, sort_keys=True)
    )
    cached_result = _load_from_cache(cache_key, cache_timeout)
    if cached_result:
        return cached_result

    try:
        r = requests.get(url, headers=headers, params=params)
        result = json.loads(r.text)
        _save_to_cache(cache_key, result)
        return result
    except requests.exceptions.RequestException:
        logging.exception("Could not fetch with headers and params: " + url)
        if cached_result:
            logging.info(f"Returning stale cached data for {url}")
            return cached_result
        return None
