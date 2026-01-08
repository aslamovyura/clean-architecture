import uuid
import pytest
import requests

def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


def post_to_add_batch(api_url, ref, sku, qty, eta):
    r = requests.post(
        f"{api_url}/add_batch", json={"ref": ref, "sku": sku, "qty": qty, "eta": eta}
    )
    assert r.status_code == 201


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
@pytest.skip(reason="An API is required, no way to test it now.")
def test_happy_path_returns_201_and_allocated_batch(api_url):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref("1")
    laterbatch = random_batchref("2")
    otherbatch = random_batchref("3")
    post_to_add_batch(api_url, laterbatch, sku, 100, "2011-01-02")
    post_to_add_batch(api_url, earlybatch, sku, 100, "2011-01-01")
    post_to_add_batch(api_url, otherbatch, othersku, 100, None)
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}

    r = requests.post(f"{api_url}/allocate", json=data)

    assert r.status_code == 201
    assert r.json()["batchref"] == earlybatch


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
@pytest.skip(reason="An API is required, no way to test it now.")
def test_unhappy_path_returns_400_and_error_message(api_url):
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    r = requests.post(f"{api_url}/allocate", json=data)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"