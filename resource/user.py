from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import user_router_model
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from model import db, Member


# Swagger APIs' authorization format
security_params = [{"bearer": []}]

def get_access_token(account):
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token

####### API Action #########

class Users(MethodResource):
    # GET_ALL
    @doc(description='Get Users info.', tags=['User'], security=security_params)
    @use_kwargs(user_router_model.UserGetSchema, location="query")
    @marshal_with(user_router_model.UserGetResponse, code=200)
    # @jwt_required()
    def get(self, **kwargs):
        filter_name = kwargs.get("name")
        
        if filter_name:
            members = Member.query.filter(Member.name.ilike(f"%{filter_name}%")).all()
            # members = Member.query.filter_by(name=filter_name).all()
        else:
            members = Member.query.all()

        member_info = [{
            "id": member.id,
            "name": member.name,
            "account": member.account,
            "passwd": member.passwd,
            "gender": member.gender,
            "created_time": member.created_time
        } for member in members] 
        return util.success(member_info)

    # POST
    @doc(description='Create User.', tags=['User'])
    @use_kwargs(user_router_model.UserPostSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=201)
    # @jwt_required()
    def post(self, **kwargs):
        import datetime
        kwargs['created_time'] = datetime.datetime.now()
        member = Member(**kwargs)
        db.session.add(member)
        db.session.commit()
        return util.success()


class User(MethodResource):
    @doc(description='Get Single user info.', tags=['User'])
    @marshal_with(user_router_model.UserGetResponse, code=200)
    @jwt_required()
    def get(self, id):
        return util.success()

    @doc(description='Update User info.', tags=['User'])
    @use_kwargs(user_router_model.UserPatchSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=201)
    def patch(self, id, **kwargs):
        member_info = Member.query.filter_by(id=id).first()
        if member_info is None:
            return util.failure({"message":"User not found"})
        
        # 2. 一口氣更新
        kwargs = {k: v for k, v in kwargs.items() if v is not None or v != ""}
        
        Member.query.filter(Member.id == id).update(kwargs)
        db.session.commit()

        return util.success()

    @doc(description='Delete User info.', tags=['User'])
    @marshal_with(None, code=204)
    def delete(self, id):
        Member.query.filter_by(id=id).delete()
    
        db.session.commit()
        return util.success()