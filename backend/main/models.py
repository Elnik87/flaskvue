from backend.main import db


class TODOSes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    boss = db.Column(db.String(20), nullable=False)
    important = db.Column(db.Boolean, default=True)

    def get_dict(self):
        item_dict = {
            "id": self.id,
            "content": self.content,
            "boss": self.boss,
            "important": self.important
        }
        return item_dict

    def __repr__(self):
        return "<TODOS id: {}, title: {}".format(self.id, self.title)
