from flask import Flask
from flask_graphql import GraphQLView
from  graphene import Schema
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv




load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from gql.mutations import Mutation
from gql.queries import Query

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





