from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

class Transfer(db.Model):
    __tablename__ = 'transfers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)        # Internal DB id
    transfer_id = db.Column(db.String, unique=True, nullable=False)         # Custom transfer id
    status = db.Column(db.String, nullable=False)                           # "here we go", "rumor", "loan"
    player_name = db.Column(db.String, nullable=False)
    player_face_url = db.Column(db.String)                                  # URL to player's face image
    from_club = db.Column(db.String)
    to_club = db.Column(db.String)
    transfer_amount = db.Column(db.Float)                                   # Use None if undisclosed
    position = db.Column(db.String)
    transfer_time = db.Column(db.Date)
    from_club_logo_url = db.Column(db.String)                               # URL to "from" club logo
    to_club_logo_url = db.Column(db.String)                                 # URL to "to" club logo

    def as_dict(self):
        # Utility to serialize object for API output
        return {
            "id": self.id,
            "transfer_id": self.transfer_id,
            "status": self.status,
            "player_name": self.player_name,
            "player_face_url": self.player_face_url,
            "from_club": self.from_club,
            "to_club": self.to_club,
            "transfer_amount": self.transfer_amount,
            "position": self.position,
            "transfer_time": self.transfer_time.isoformat() if self.transfer_time else None,
            "from_club_logo_url": self.from_club_logo_url,
            "to_club_logo_url": self.to_club_logo_url,
        }