from core import db
from core.libs import helpers
from core.models.assignments import Assignment, AssignmentStateEnum
from core.apis.decorators import AuthPrincipal


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
    def submit(cls, _id, grade, auth_principal: AuthPrincipal, teacher_id):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.state != AssignmentStateEnum.DRAFT, 'assignment is still in draft state and cannot be graded')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')

        assignment.grade = grade
        assignment.teacher_id = teacher_id
        db.session.flush()

        return assignment

