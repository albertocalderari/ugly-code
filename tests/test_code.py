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
    assert response.json() == 'item not found'
    assert response.status_code == 500


def test_post_new_order(client):
    response = client.post(
        url="/create-order",
        json={
            "id": "1234",
            'basket': [
                {
                    'id': '1',
                    'name': 'chicken',
                    'quantity': '2'}
            ]
        }
    )
    assert response.json() == {'message': 'item added'}
    assert response.status_code == 200


def test_post_existing_order(client, dynamo_client):
    response = client.post(
        url="/create-order",
        json={
            "id": "2",
            'basket': [
                {
                    'id': '1',
                    'name': 'chicken',
                    'quantity': '200'}
            ]
        }
    )
    assert response.json() == {'message': 'item added'}
    assert response.status_code == 200

    actual = dynamo_client.get_item(
        TableName='orders',
        Key={
            'id': {
                'S': "2",
            }
        }
    )
    assert actual['Item'] == {
        'basket': {
            'L': [
                {'M':
                    {
                        'id': {'S': '1'},
                        'name': {'S': 'chicken'},
                        'quantity': {'S': '200'}}
                }
            ]
        },
        'id': {'S': '2'}
    }


def test_update_order(client, dynamo_client):
    response = client.post(
        url="/update-order",
        json={
            "id": "2",
            'basket': [
                {
                    'id': '1',
                    'name': 'chicken',
                    'quantity': '200'}
            ]
        }
    )
    assert response.json() == {'message': 'item added'}
    assert response.status_code == 200

    actual = dynamo_client.get_item(
        TableName='orders',
        Key={
            'id': {
                'S': "2",
            }
        }
    )
    assert actual['Item'] == {
        'basket': {
            'L': [
                {'M':
                    {
                        'id': {'S': '1'},
                        'name': {'S': 'chicken'},
                        'quantity': {'S': '200'}}
                }
            ]
        },
        'id': {'S': '2'}
    }


def test_update_order_not_found(client, dynamo_client):
    response = client.post(
        url="/update-order",
        json={
            "id": "2000",
            'basket': [
                {
                    'id': '1',
                    'name': 'chicken',
                    'quantity': '200'}
            ]
        }
    )
    assert response.json() == 'could not write item'
    assert response.status_code == 200
