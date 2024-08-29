import graphene
import accounts.schema
import products.schema


class Query(accounts.schema.Query,products.schema.Query,graphene.ObjectType):
    pass

class Mutation(accounts.schema.Mutation,products.schema.Mutation,graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,mutation=Mutation)