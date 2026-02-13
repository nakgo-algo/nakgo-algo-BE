from pydantic import BaseModel, ConfigDict, Field


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    nickname: str
    email: str | None = None
    profileImage: str | None = Field(default=None, alias="profile_image")
    isAdmin: bool = False

    @classmethod
    def model_validate(cls, obj, **kwargs):
        instance = super().model_validate(obj, **kwargs)
        if hasattr(obj, "role"):
            instance.isAdmin = obj.role == "admin"
        return instance
