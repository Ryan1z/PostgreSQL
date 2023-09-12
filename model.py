from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
import datetime 

db = SQLAlchemy()

class Member(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    account = Column(String(50))
    passwd = Column(String(50))
    gender = Column(Boolean)
    created_time = Column(DateTime(timezone=True), default=datetime.datetime.now())

class Organisation(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    owner_id = Column(Integer,ForeignKey(Member.id, ondelete="SET NULL"),nullable=True)
    
    @property
    def owner(self):
        if self.owner_id is not None:
            member_info = Member.query.get(self.owner_id)
            return {
                "name": member_info.name,
                "account": member_info.account,
                "gender": member_info.gender,
            }