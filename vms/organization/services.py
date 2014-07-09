from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
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

#organization names must unique
def get_organization_by_name(organization_name):

    is_valid = True
    result = None

    try:
        organization = Organization.objects.get(organization_name__icontains=organization_name)
    except MultipleObjectsReturned:
        is_valid = False
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = organization

    return result

def get_organizations_by_name():
    organization_list = Organization.objects.all().order_by('organization_name')
    return organization_list
