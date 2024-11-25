from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class User:
    email: str  # Required field
    username: Optional[str] = None
    password: Optional[str] = None
    emailVerified: Optional[bool] = False
    externalId: Optional[str] = None
    fullName: Optional[str] = None
    givenName: Optional[str] = None
    familyName: Optional[str] = None
    middleName: Optional[str] = None
    honorificPrefix: Optional[str] = None
    honorificSuffix: Optional[str] = None
    nickname: Optional[str] = None
    displayName: Optional[str] = None
    pictureUrl: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    phoneNumber: Optional[str] = None
    preferredLanguage: Optional[str] = None
    locale: Optional[str] = None
    timeZone: Optional[str] = None

    # Add on fields
    roles: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a User object from a dictionary."""
        return cls(**{key: data[key] for key in cls.fields() if key in data})

    @classmethod
    def fields(cls) -> List[str]:
        """Returns the list of field names for the User class."""
        return [field.name for field in cls.__dataclass_fields__.values()]

    def to_dict(self):
        """Returns a dictionary representation of the User object, excluding fields with None values."""
        return {key: value for key, value in asdict(self).items() if value is not None}
    
    def __repr__(self):
        """Custom string representation that excludes None fields."""
        non_none_fields = {key: value for key, value in asdict(self).items() if value is not None}
        fields_str = ', '.join(f'{key}={value!r}' for key, value in non_none_fields.items())
        return f'User({fields_str})'