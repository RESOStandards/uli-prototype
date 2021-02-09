

def format_uli(licensee):
    item = {}
    item = {
        "uli": str(licensee["_id"]),
        "MemberEmail": hide_MemberEmail(licensee["MemberEmail"]),
        "MemberFirstName": licensee["MemberFirstName"],
        "MemberLastName": licensee["MemberLastName"],
        "license_data": licensee["license_data"],
        "MemberNationalAssociationId": licensee["MemberNationalAssociationId"]
    }
    return item

def hide_MemberEmail(MemberEmail):
    m = MemberEmail.split('@')
    return f'{m[0][0]}{"*"*(len(m[0])-2)}{m[0][-1] if len(m[0]) > 1 else ""}@{m[1]}'


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

