from flask import Blueprint
from flask import jsonify
from core import db
from core.libs import helpers
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.principals import Principal
from core.apis.decorators import AuthPrincipal

from .schema import AssignmentSchema, AssignmentSubmitSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


"""
List all submitted and graded assignments
"""


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_submitted_and_graded_assignments(p):
    """
    ### GET /principal/assignments

    List all submitted and graded assignments
    """
    principal_assignments = Principal.get_assignments_by_principal(p.principal_id)
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)



@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """
    List all the teachers
    """

    list_teachers = Principal.get_list_of_teachers(p.principal_id)
    list_teachers_dump = AssignmentSchema().dump(list_teachers, many=True)
    return APIResponse.respond(data=list_teachers_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):

  """Grade an assignment"""

  grade_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

  graded_assignment = Principal.submit(
      _id=grade_assignment_payload._id,
      teacher_id=grade_assignment_payload.teacher_id,
      auth_principal=p,
      grade=grade_assignment_payload.grade
  )
  db.session.commit()
  graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
  return APIResponse.respond(data=graded_assignment_dump)

