def test_list_orders(client):
    response = client.get(url="/order/list")
    expected = []
    assert len(response.json()) == 200
    assert response.status_code == 200


def test_get_order(client):
    response = client.post(
        url="/get-order",
        json={"id": "123"}
    )
    expected = {
        'basket': [
            {
                'id': '1',
                'name': 'chicken',
                'quantity': '2'}
        ],
        'id': '123'
    }
    assert response.json() == expected
    assert response.status_code == 201


def test_get_order_not_found(client):
    response = client.post(
        url="/get-order",
        json={"id": "1234"}
    )
    assert response.status_code == 500
