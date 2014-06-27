from django.core.exceptions import ObjectDoesNotExist
from organization.models import Organization

def get_organization_by_id(organization_id):
    
    is_valid = True
    result = None

    try:
        organization = Organization.objects.get(pk=organization_id)
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = organization

    return result

def get_organizations_by_name():
    organization_list = Organization.objects.all().order_by('organization_name')
    return organization_list
