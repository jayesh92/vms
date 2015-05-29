from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from organization.models import Organization

#need to check that this organization is not currently associated with a user (otherwise the user gets cascade deleted)
def delete_organization(organization_id):

    result = True

    organization = get_organization_by_id(organization_id)
    #check if there are currently any users associated with this organization
    #this might be difficult to maintain as different types of users are added on
    volunteers_in_organization = organization.volunteer_set.all()
    administrators_in_organization = organization.administrator_set.all()
    
    #can only delete an organization if no users are currently associated with it
    if organization and (not volunteers_in_organization) and (not administrators_in_organization):
        organization.delete()
    else:
        result = False

    return result

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
        organization = Organization.objects.get(name__icontains=organization_name)
    except MultipleObjectsReturned:
        is_valid = False
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = organization

    return result

def get_organizations_ordered_by_name():
    organization_list = Organization.objects.all().order_by('name')
    return organization_list
