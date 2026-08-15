from pydantic import BaseModel


class TextAnalysis(BaseModel):
    summary: str
    sentiment: str
    main_topic: str