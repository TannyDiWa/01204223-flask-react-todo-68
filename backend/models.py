from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base) 

class TodoItem(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)
    comments: Mapped[list["Comment"]] = relationship(back_populates="todo",cascade="all, delete")
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "comments": [
                comment.to_dict() for comment in self.comments
            ]
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String(250))
    ### สังเกตว่าในการประกาศด้านล่าง มีการระบุ ondelete ด้วย
    todo_id: Mapped[int] = mapped_column(ForeignKey('todo_item.id', ondelete="CASCADE"))

    todo: Mapped["TodoItem"] = relationship(back_populates="comments")
    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "todo_id": self.todo_id
        }