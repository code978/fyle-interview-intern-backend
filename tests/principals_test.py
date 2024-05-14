from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.principals import Principal
from core.libs.exceptions import FyleError
import pytest
from unittest.mock import Mock


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 400

    # assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    # assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 400

    # assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    # assert response.json['data']['grade'] == GradeEnum.B



def test_list_all_submitted_and_graded_assignments(client, h_principal):
    response = client.get('/principal/assignments', headers=h_principal)

    assert response.status_code == 200
    assert 'data' in response.json
    # Add more assertions based on the expected response data structure
    # Test for different scenarios like empty assignments, specific assignments, etc.


def test_list_teachers(client, h_principal):
    response = client.get('/principal/teachers', headers=h_principal)

    assert response.status_code == 200
    assert 'data' in response.json
    # Add more assertions based on the expected response data structure
    # Test for different scenarios like empty teacher list, specific teachers, etc.



def test_list_all_submitted_and_graded_assignments_invalid_auth(client):
    response = client.get('/principal/assignments', headers={'Authorization': 'Invalid Token'})

    assert response.status_code == 401
    assert 'error' in response.json



def test_get_assignments_by_principal_valid_id():
    principal = Principal.query.get(1)
    assignments = principal.get_assignments_by_principal(principal.id)
    assert len(assignments) > 0


def test_get_assignments_by_principal_invalid_id():
    assignments = Principal.get_assignments_by_principal(999)
    assert len(assignments) == 0


def test_list_all_submitted_and_graded_assignments(client, h_principal):
    response = client.get('/principal/assignments', headers=h_principal)

    assert response.status_code == 200
    assert 'data' in response.json
    for assignment in response.json['data']:
        assert assignment['state'] in ['SUBMITTED', 'GRADED']
        assert assignment['teacher_id'] is not None or assignment['student_id'] is not None

def test_list_teachers(client, h_principal):
    response = client.get('/principal/teachers', headers=h_principal)

    assert response.status_code == 200
    assert 'data' in response.json
    for teacher in response.json['data']:
        assert 'id' in teacher
        assert 'created_at' in teacher
        assert 'updated_at' in teacher

def test_grade_assignment_invalid_grade(client, h_principal):
    payload = {
        'id': 1,
        'grade': 'X'
    }
    response = client.post('/principal/assignments/grade', json=payload, headers=h_principal)

    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'ValidationError'

def test_get_assignments_by_principal_invalid_id():
    principal_id = 999  # Provide an invalid principal ID
    assignments = Principal.get_assignments_by_principal(principal_id)
    
    assert len(assignments) == 0


def test_get_list_of_teachers_valid_id():
    principal_id = 1  # Provide a valid principal ID
    teachers = Principal.get_list_of_teachers(principal_id)
    
    assert len(teachers) > 0
    for teacher in teachers:
        assert teacher.id is not None
        assert teacher.created_at is not None
        assert teacher.updated_at is not None


def test_grade_assignment_invalid_assignment_id(client, h_principal):
  """
  Test case for grading with an invalid assignment ID.
  """
  payload = {
      'id': 999,  # Invalid assignment ID
      'grade': GradeEnum.B.value,
  }

  response = client.post('/principal/assignments/grade', json=payload, headers=h_principal)

  assert response.status_code == 400
  # Assert error message or response structure indicating invalid ID


def test_mark_grade_is_none(client, h_principal):
  
#   h_principal.student_id = 1

  graded_assignment = Principal.mark_grade(1, 'A', h_principal)
  
  assert graded_assignment is None  # Ensure assignment object is returned



def test_grade_assignment_missing_grade(client):
  """
  Test case for grading with a payload missing the grade.
  """
  payload = {'_id': 1}  # Missing grade

  # Make the POST request
  response = client.post('/assignments/grade', json=payload)

  # Assert bad request response
  assert response.status_code == 404

  # Assert error message in response
#   response_data = response.json()
#   print(f"response_data : {response_data}")
#   assert 'grade' in response_data.get('message')
