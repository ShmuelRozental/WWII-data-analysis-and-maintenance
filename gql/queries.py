import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.models import Mission, Target, Country, City, TargetType

class GraphQLTargetType(SQLAlchemyObjectType):
    class Meta:
        model = TargetType

class GraphQLTarget(SQLAlchemyObjectType):
    class Meta:
        model = Target

class GraphQLMission(SQLAlchemyObjectType):
    class Meta:
        model = Mission

class GraphQLCity(SQLAlchemyObjectType):
    class Meta:
        model = City

class GraphQLCountry(SQLAlchemyObjectType):
    class Meta:
        model = Country
class Query(graphene.ObjectType):
    mission_by_id = graphene.Field(GraphQLMission, mission_id=graphene.Int(required=True))

    def resolve_mission_by_id(self, info, mission_id):
        return Mission.query.get(mission_id)

    missions_by_date_range = graphene.List(
        GraphQLMission,
        start_date=graphene.Date(required=True),
        end_date=graphene.Date(required=True)
    )

    def resolve_missions_by_date_range(self, info, start_date, end_date):
        return Mission.query.filter(Mission.mission_date.between(start_date, end_date)).all()

    missions_by_country = graphene.List(GraphQLMission, country_id=graphene.Int(required=True))

    def resolve_missions_by_country(self, info, country_id):
        return Mission.query.join(Target).join(City).join(Country).filter(Country.country_id == country_id).all()

    missions_by_target_industry = graphene.List(GraphQLMission, target_industry=graphene.String(required=True))

    def resolve_missions_by_target_industry(self, info, target_industry):
        return Mission.query.join(Target).filter(Target.target_industry == target_industry).all()

    missions_aircraft_list = graphene.List(
        graphene.Float, mission_id=graphene.Int(required=True)
    )

    def resolve_missions_aircraft_list(self, info, mission_id):
        mission = Mission.query.get(mission_id)
        if mission:
            return [
                mission.airborne_aircraft,
                mission.attacking_aircraft,
                mission.bombing_aircraft,
                mission.aircraft_returned,
                mission.aircraft_failed,
                mission.aircraft_damaged,
                mission.aircraft_lost
            ]
        return []

    mission_attack_results = graphene.List(
        graphene.Float,
        mission_id=graphene.Int(required=True)
    )

    def resolve_mission_attack_results(self, info, mission_id):
        mission = Mission.query.get(mission_id)
        if mission:
            return [
                mission.aircraft_returned,
                mission.aircraft_failed,
                mission.aircraft_damaged,
                mission.aircraft_lost
            ]
        return []
