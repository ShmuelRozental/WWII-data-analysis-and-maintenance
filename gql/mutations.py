import graphene

from conn import db
from conn.db import SessionLocal
from gql.queries import GraphQLMission
from models.models import Mission, Target, Country, City, TargetType

class AddMission(graphene.Mutation):
    class Arguments:
        mission_date = graphene.Date(required=True)
        airborne_aircraft = graphene.Float()
        attacking_aircraft = graphene.Float()
        bombing_aircraft = graphene.Float()
        aircraft_returned = graphene.Float()
        aircraft_failed = graphene.Float()
        aircraft_damaged = graphene.Float()
        aircraft_lost = graphene.Float()

    mission = graphene.Field(GraphQLMission)

    def mutate(self, info, **kwargs):
        mission = Mission(**kwargs)
        session = SessionLocal()  # Create a new session
        try:
            session.add(mission)
            session.commit()
            return AddMission(mission=mission)
        except Exception as e:
            session.rollback()
            raise e  # Raise the error for handling
        finally:
            session.close()

class AddTarget(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        target_industry = graphene.String(required=True)
        city_id = graphene.Int(required=True)
        target_type_id = graphene.Int()
        target_priority = graphene.Int()

    target = graphene.Field(TargetType)

    def mutate(self, info, **kwargs):
        target = Target(**kwargs)
        session = SessionLocal()  # Create a new session
        try:
            session.add(target)
            session.commit()
            return AddTarget(target=target)
        except Exception as e:
            session.rollback()
            raise e  # Raise the error for handling
        finally:
            session.close()

class UpdateAttackResult(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        aircraft_returned = graphene.Float()
        aircraft_failed = graphene.Float()
        aircraft_damaged = graphene.Float()
        aircraft_lost = graphene.Float()

    mission = graphene.Field(GraphQLMission)

    def mutate(self, info, mission_id, **kwargs):
        session = SessionLocal()  # Create a new session
        mission = session.query(Mission).get(mission_id)
        if mission:
            for key, value in kwargs.items():
                setattr(mission, key, value)
            session.commit()
            return UpdateAttackResult(mission=mission)
        session.rollback()
        return UpdateAttackResult(mission=None)

class DeleteMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, mission_id):
        session = SessionLocal()  # Create a new session
        mission = session.query(Mission).get(mission_id)
        if mission:
            session.delete(mission)
            session.commit()
            return DeleteMission(success=True)
        session.rollback()
        return DeleteMission(success=False)

class Mutation(graphene.ObjectType):
    add_mission = AddMission.Field()
    add_target = AddTarget.Field()
    update_attack_result = UpdateAttackResult.Field()
    delete_mission = DeleteMission.Field()