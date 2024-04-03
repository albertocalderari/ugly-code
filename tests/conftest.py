
@fixture()
def dynamo_client(tenant_objects, my_group, monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    with mock_dynamodb():
        for t in tenant_objects:
            t.save()
        yield DynamoClient()