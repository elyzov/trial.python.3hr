import json


def test_get_all_products(client):
    response = client.get('/products')

    json_response = json.loads(response.data)

    assert response.status_code == 200
    assert not json_response.get('results')
