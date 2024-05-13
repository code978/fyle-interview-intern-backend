from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
import pytest
from core.libs.exceptions import FyleError

def test_handle_fyle_error(client):
    with pytest.raises(FyleError) as e:
        raise FyleError(400, 'Test error message')

    response = client.get('/non-existent-route')
    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == FyleError(400, 'Test error message').to_dict()['message']


def test_handle_validation_error(client):
    with pytest.raises(ValidationError) as e:
        raise ValidationError({'field': ['Invalid value']})

    response = client.post('/endpoint', json={'field': 'invalid'})
    assert response.status_code == 404
    assert response.json['error'] == 'ValidationError'
    assert response.json['message'] == {'field': ['Invalid value']}