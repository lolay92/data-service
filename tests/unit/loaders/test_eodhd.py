import pytest
from src.data_services.loaders.eodhd import Eodhd
from unittest import mock
from src.data_services.loaders.eodhd import InvalidEodKeyError


def test_eodhd_init(dummy_eodhd):
    expected_params = {
        "api_token": dummy_eodhd.api_key,
        "fmt": "json",
    }
    expected_root_url = "https://eodhistoricaldata.com/api"
    expected_API_name = "EODHISTORICALDATA"

    assert dummy_eodhd.params == expected_params
    assert dummy_eodhd.ROOT_URL == expected_root_url
    assert dummy_eodhd.API.name == expected_API_name


@mock.patch.dict("src.data_services.loaders.base.os.environ", {}, clear=True)
def test_eodhd_invalidkeyerror():
    with pytest.raises(
        InvalidEodKeyError, match="EODHISTORICALDATA api_key cannot be None!"
    ):
        Eodhd()


@pytest.mark.parametrize(
    "limit, search_query, json_response_value",
    [
        (20, "AAPl", [{"data": "findings_AAPl_search"}]),
        (30, "MCD", [{"data": "findings_MCD_search"}]),
    ],
)
@mock.patch("src.data_services.loaders.eodhd.requests.Response")
@mock.patch("src.data_services.loaders.eodhd.requests.Session.get")
def test_search(
    mock_request_get,
    mock_response,
    dummy_eodhd,
    limit,
    search_query,
    json_response_value,
):
    mock_response.json.return_value = json_response_value
    mock_request_get.return_value = mock_response
    search_query = search_query
    assert dummy_eodhd.search(search_query, limit) == json_response_value
    url = f"{dummy_eodhd.ROOT_URL}/search/{search_query}"
    mock_request_get.assert_called_with(url=url, params=dummy_eodhd.params)


@mock.patch("src.data_services.loaders.eodhd.requests.Response")
@mock.patch("src.data_services.loaders.eodhd.requests.Session.get")
def test_exchange_traded_tickers(mock_request_get, mock_response, dummy_eodhd):
    mock_response.json.return_value = [{"data": "example"}]
    mock_request_get.return_value = mock_response

    exchange_code = "US"
    assert dummy_eodhd.exchange_traded_tickers(exchange_code) == [{"data": "example"}]
    url = f"{dummy_eodhd.ROOT_URL}/exchange-symbol-list/{exchange_code}"
    mock_request_get.assert_called_with(url=url, params=dummy_eodhd.params)


def test_ohlcv():
    pass


# use dataquery fixture
# Mock _fetch_json async function ==> return json value
# Mock aiohttp.ClientSession.get ==>
