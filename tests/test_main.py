import requests as r

from core.config import get_target


def test_healthcheck():
    response = r.get(f"{get_target()}/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "true"}


def test_config_get_not_item():
    response = r.get(f"{get_target()}/config", params={"service": "managed-k8s"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Service <<managed-k8s>> not found"}


def test_config_delete_not_item():
    response = r.delete(f"{get_target()}/config", params={"service": "managed-k8s"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Service <<managed-k8s>> not found"}


def test_config_put_not_item():
    response = r.put(f"{get_target()}/config", 
    json={
            "service": "managed-k8s",
            "data": [
              {
                "key1": "value1"
              },
              {
                "key2": "value2"
              }
            ]
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Service <<managed-k8s>> not found"}


def test_config_post_new_item():
    response = r.post(f"{get_target()}/config", 
    json={
            "service": "managed-k8s",
            "data": [
              {
                "key1": "value1"
              },
              {
                "key2": "value2"
              }
            ]
        }
    )
    assert response.status_code == 201
    assert response.json() == {
      "success": True,
      "detail": "Successfully created"
    }

def test_config_get_item_after_post():
    response = r.get(f"{get_target()}/config", params={"service": "managed-k8s"})
    assert response.status_code == 200
    assert response.json() == {
      "key1": "value1",
      "key2": "value2"
    }


def test_config_put_new_item_no_values():
    response = r.put(f"{get_target()}/config", 
    json={
            "service": "managed-k8s",
            "data": [
                {
                    "test_key_1": "learn"
                }
            ]
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Config <<test_key_1>> not found"}


def test_config_put_new_item_values_exists():
    response = r.put(f"{get_target()}/config", 
    json={
          "service": "managed-k8s",
          "data": [
            {
              "key1": "value1"
            },
            {
              "key2": "value2"
            }
          ]
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Key <<key1>> already have <<value1>> value"}


def test_config_put_new_item_values():
    response = r.put(f"{get_target()}/config", 
    json={
          "service": "managed-k8s",
          "data": [
            {
              "key1": "learn"
            },
            {
              "key2": "golang"
            }
          ]
        }
    )
    assert response.status_code == 200
    assert response.json() == {
      "success": True,
      "detail": "Successfully updated"
    }


def test_config_get_item_after_put():
    response = r.get(f"{get_target()}/config", params={"service": "managed-k8s"})
    assert response.status_code == 200
    assert response.json() == {
      "key1": "learn",
      "key2": "golang"
    }


def test_config_put_new_item_values_version_diff():
    response = r.put(f"{get_target()}/config", 
    json={
          "service": "managed-k8s",
          "data": [
            {
              "key1": "now"
            }
          ]
        }
    )
    assert response.status_code == 200
    assert response.json() == {
      "success": True,
      "detail": "Successfully updated"
    }


def test_version_get_history():
    response = r.get(f"{get_target()}/version/history", params={"service": "managed-k8s"})
    assert response.status_code == 200
    assert response.json() == {
      "key2": {
        "value": "golang",
        "version": 2,
        "prev_version": {
          "value": "value2",
          "version": 1,
          "prev_version": None
        }
      },
      "key1": {
        "value": "now",
        "version": 3,
        "prev_version": {
          "value": "learn",
          "version": 2,
          "prev_version": {
            "value": "value1",
            "version": 1,
            "prev_version": None
          }
        }
      }
    }


def test_version_get_last_version():
    response = r.get(f"{get_target()}/version", params={"service": "managed-k8s"})
    assert response.status_code == 200
    assert response.json() == {
      "key2": "golang",
      "key1": "now"
    }


def test_version_get_2_version():
    response = r.get(f"{get_target()}/version", params={
        "service": "managed-k8s",
        "version": 2
        }
    )
    assert response.status_code == 200
    assert response.json() == {
      "key2": "golang",
      "key1": "learn"
    }


def test_version_get_1_version():
    response = r.get(f"{get_target()}/version", params={
        "service": "managed-k8s",
        "version": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {
      "key2": "value2",
      "key1": "value1"
    }


def test_config_delete_new_item():
    response = r.delete(f"{get_target()}/config", params={"service": "managed-k8s"})
    assert response.status_code == 200
    assert response.json() == {
      "success": True,
      "detail": "Successfully deleted"
    }
