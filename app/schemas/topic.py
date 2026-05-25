from pydantic import BaseModel

class TopicCreate(BaseModel):
    title: str
    instruction: str

class TopicUpdate(TopicCreate):
    pass
