from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import organisation_router_model
# from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from model import db, Organisation, Member

# Swagger APIs' authorization format
security_params = [{"bearer": []}]

class  Orgs(MethodResource):
    # GET_ALL
    @doc(description='Get Users info.', tags=['Org'], security=security_params)
    @use_kwargs(organisation_router_model.UserGetSchema, location="query")
    @marshal_with(organisation_router_model.UserGetResponse, code=200)
    # @jwt_required()
    def get(self, **kwargs):
        filter_name = kwargs.get("name")
        
        if filter_name:
            organisationes = Organisation.query.filter(Organisation.name.ilike(f"%{filter_name}%")).all()
            # members = Member.query.filter_by(name=filter_name).all()
        else:
            organisationes = Organisation.query.all()

        organisation_info = [{
            "id": organisations.id,
            "name": organisations.name,
            "owner_id": organisations.owner_id
        } for organisations in organisationes] 
        return util.success(organisation_info)

    # POST
    @doc(description='Create User.', tags=['Org'])
    @use_kwargs(organisation_router_model.UserPostSchema, location="form")
    @marshal_with(organisation_router_model.UserCommonResponse, code=201)
    # @jwt_required()
    def post(self, **kwargs):
        organisation = Organisation(**kwargs)
        db.session.add(organisation)
        db.session.commit()
        return util.success()
    

class Org(MethodResource):
    @doc(description='Update User info.', tags=['Org'])
    @marshal_with(organisation_router_model.UsersGetResponse, code=201)
    def get(self, id):
        organ = Organisation.query.filter_by(id=id).first()
        
        organisation_info = {
            "id": organ.id,
            "name": organ.name,
            "owner": organ.owner,
        }
        return util.success(organisation_info)
    
    @doc(description='Update User info.', tags=['Org'])
    @use_kwargs(organisation_router_model.UserPatchSchema, location="form")
    @marshal_with(organisation_router_model.UserCommonResponse, code=201)
    def patch(self, id, **kwargs):
        Org_info = Organisation.query.filter_by(id=id).first()
        if Org_info is None:
            return util.failure({"message":"User not found"})
        
        kwargs = {k: v for k, v in kwargs.items() if v is not None or v != ""}
        owner_id = kwargs.get("owner_id")
        if owner_id is not None:
            Member_info = Member.query.filter_by(id=owner_id).first()
            if Member_info is None:
                return util.failure({"message":"User not found"})
            
        Organisation.query.filter(Organisation.id == id).update(kwargs)
        db.session.commit()

        return util.success()
    
    @doc(description='Delete User info.', tags=['Org'])
    @marshal_with(None, code=204)
    def delete(self, id):
        Organisation.query.filter_by(id=id).delete()
    
        db.session.commit()
        return util.success()