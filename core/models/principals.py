from core import db
from core.libs import helpers
from core.models.assignments import Assignment, AssignmentStateEnum
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.apis.responses import APIResponse


class Principal(db.Model):
    __tablename__ = 'principals'
    id = db.Column(db.Integer, db.Sequence('principals_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Principal %r>' % self.id
    
    @classmethod
    def get_assignments_by_principal(cls, principal_id):
        return db.session.query(Assignment).join(
            cls, cls.id == Principal.id, isouter=True).filter(
                cls.id == principal_id,
                Assignment.state != AssignmentStateEnum.DRAFT).all()


    @classmethod
    def get_list_of_teachers(cls, principal_id):
        print('get_list_of_teachers')
        return cls.query.with_entities(cls.id, cls.created_at, cls.updated_at).all()

    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(grade is not None, 'assignment with empty grade cannot be graded')
        
        if assignment.state == AssignmentStateEnum.DRAFT:
            if assignment.teacher_id is not None:
                assertions.assert_valid(assignment.teacher_id == auth_principal.teacher_id, 'This assignment belongs to a different teacher')
            else:
                assertions.assert_valid(assignment.student_id == auth_principal.student_id, 'This assignment belongs to a different student')

            assignment.grade = grade
            assignment.state = AssignmentStateEnum.GRADED
            db.session.flush()

            return assignment
        else:
            assertions.assert_valid('This assignment is already graded')
            # return APIResponse.respond(data={'message': 'This assignment is already graded'})


