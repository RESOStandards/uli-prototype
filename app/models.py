from mongoengine import *
import datetime
class Member(Document):
    MemberNationalAssociationId = StringField()
    MemberFirstName = StringField()
    MemberLastName = StringField()
    MemberEmail = StringField()
    LicenseInfo = ListField()
    date_created = DateTimeField(default=datetime.datetime.utcnow)

    def to_json(self):
        return {
            "ULI": str(self.pk),
            "MemberNationalAssociationId": self.MemberNationalAssociationId,
            "MemberFirstName": self.MemberFirstName,
            "MemberLastName": self.MemberLastName,
            "MemberEmail": self.MemberEmail,
            "LicenseInfo": self.LicenseInfo
        }

# class LicenseInfo:
#     def __init__(self, agency, type, number):
#         self.agency = agency
#         self.type = type
#         self.number = number

# class SearchBase:
#     pass
# class SearchRequest:
#     pass
# class SearchResponse:
#     pass
# class RegistryRequest:
#     pass
# class RegistryResponse:
#     pass
# class Error:
#     pass