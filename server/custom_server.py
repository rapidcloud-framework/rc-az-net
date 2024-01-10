#!/usr/bin/env python3

__author__ = "Jaime Zelada"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "jzelada@kinect-consulting.com"

import logging
import json
import pprint

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from msgraph.core import GraphClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from commands.kc_metadata_manager.azure_metadata import Metadata

# import module
import traceback
import os

logger = logging.getLogger("server")
logger.setLevel(logging.INFO)


def pp(d):
    print(pprint.pformat(d))


def get_resource_groups(params):
    # Acquire a credential object using CLI-based authentication.
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    group_list = resource_client.resource_groups.list()
    resource_groups = []
    sorted_entities = sorted(group_list, key=lambda x: x.name.lower(), reverse=False)
    rc_rgs = list(filter(lambda x: x.tags is not None and x.tags.get('profile') is not None and x.tags.get('profile') == params.get('env') ,sorted_entities))
    other_rgs = list(filter((lambda x: x.tags is None) ,sorted_entities))
    additional_rgs = list(filter((lambda x: x.tags is not None and x.tags.get('profile') is None) ,sorted_entities))

    final_list = rc_rgs + other_rgs + additional_rgs
    
    # for item in list(final_list):
    #     print(item.name)

    #sorted_entities = sorted(group_list, key=lambda x: x.name.lower(), reverse=False)
    for group in list(final_list):
        output_dict = {}
        is_rc = ""
        if not group.tags:
            label = f"{group.name} ({group.location})"
        else:
            if group.tags is not None:
                if group.tags.get('profile') is not None:
                    if group.tags.get('profile').lower() == params.get('env').lower():
                        is_rc = "value"
            if is_rc == '':
                label = f"{group.name} ({group.location})"
            else:
                label = f"{group.name} ({group.location}) (Managed by Rapid Cloud)"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = group.name
        output_dict['value']['scope'] = group.id
        resource_groups.append(output_dict)
    return resource_groups


def get_key_vaults():
    # Acquire a credential object using CLI-based authentication.
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()

    kv_client = KeyVaultManagementClient(credential, subscription_id)
    entities = kv_client.vaults.list()

    vaults = []

    for vault in list(entities):
        output_dict = {}
        label = f"{vault.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = vault.name
        vaults.append(output_dict)
    return vaults


def get_locations():
    # Acquire a credential object using CLI-based authentication.
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()

    subs_client = SubscriptionClient(credential)
    entities = subs_client.subscriptions.list_locations(subscription_id)

    locations = []

    for location in list(entities):
        output_dict = {}
        label = f"{location.display_name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = location.name
        locations.append(output_dict)
    return locations


def get_object_ids():
    # Acquire a credential object using CLI-based authentication.
    try:
        credential = ClientSecretCredential(
            client_id=os.environ["AZURE_CLIENT_ID"], client_secret=os.environ["AZURE_CLIENT_SECRET"], tenant_id=os.environ["AZURE_TENANT_ID"])
        graph_client = GraphClient(credential=credential)
        users = graph_client.get('/users?$select=displayName,id')
        service_principal = graph_client.get(
            '/applications?$select=displayName,id')
        entities_users = json.dumps(users.json())
        ent_users = json.loads(entities_users)
        entities_sps = json.dumps(service_principal.json())
        ent_sps = json.loads(entities_sps)

    except Exception as e:
        traceback.print_exc()
    # For the users
    users = []
    for user in list(ent_users.get('value')):
        output_dict = {}
        # print(user.get('displayName'))
        label = f"{user.get('displayName')}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = user.get('id')
        users.append(output_dict)
    # For the applications
    for user in list(ent_sps.get('value')):
        output_dict = {}
        # print(user.get('displayName'))
        label = f"{user.get('displayName')}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = user.get('id')
        users.append(output_dict)
    return users


def get_route_tables():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.route_tables.list_all()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    rc_route_tables = list(filter(lambda x: x.tags is not None and x.tags.get(
        'managed') == 'rc', sorted_entities))
    route_tables = []

    for route_table in list(rc_route_tables):
        output_dict = {}
        label = f"{route_table.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = route_table.name
        route_tables.append(output_dict)

    return route_tables


def get_vnets():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.virtual_networks.list_all()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    rc_vnets = list(filter(lambda x: x.tags is not None and x.tags.get(
        'managed') == 'rc', sorted_entities))
    vnets = []

    for vnet in list(rc_vnets):
        output_dict = {}
        label = f"{vnet.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = vnet.name
        vnets.append(output_dict)

    return vnets


def get_vnets_ids():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.virtual_networks.list_all()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    rc_vnets = list(filter(lambda x: x.tags is not None and x.tags.get(
        'managed') == 'rc', sorted_entities))
    vnets = []

    for vnet in list(rc_vnets):
        output_dict = {}
        label = f"{vnet.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = vnet.id
        vnets.append(output_dict)

    return vnets


def get_log_workspaces():
    # Acquire a credential object using CLI-based authentication.
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()

    log_client = LogAnalyticsManagementClient(credential, subscription_id)
    entities = log_client.workspaces.list()

    workspaces = []

    for workspace in list(entities):
        output_dict = {}
        label = f"{workspace.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = workspace.name
        workspaces.append(output_dict)
    return workspaces


def get_nsgs():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.network_security_groups.list_all()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    rc_nsgs = list(filter(lambda x: x.tags is not None and x.tags.get(
        'managed') == 'rc', sorted_entities))
    nsgs = []

    for nsg in list(rc_nsgs):
        output_dict = {}
        label = f"{nsg.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = nsg.id
        nsgs.append(output_dict)

    return nsgs


def get_watchers():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.network_watchers.list_all()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    rc_watchers = list(filter(lambda x: x.tags is not None and x.tags.get(
        'managed') == 'rc', sorted_entities))
    watchers = []

    for watcher in list(rc_watchers):
        output_dict = {}
        label = f"{watcher.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = watcher.name
        watchers.append(output_dict)

    return watchers


def get_storage_accounts():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)
    entities = storage_client.storage_accounts.list()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    storage_accounts = []

    for storage_account in list(sorted_entities):
        output_dict = {}
        label = f"{storage_account.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = storage_account.id
        storage_accounts.append(output_dict)

    return storage_accounts


def get_subnets():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    vnets = network_client.virtual_networks.list_all()
    all_subnets = []
    for vnet in list(vnets):
        for subnet in vnet.subnets:
            subnet.vnet = vnet.name
            all_subnets.append(subnet)
    subnets = []
    for subnet in all_subnets:
        output_dict = {}
        label = f"{subnet.vnet} - {subnet.name}({subnet.address_prefix})"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = subnet.id
        subnets.append(output_dict)

    return subnets


def get_ips():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.public_ip_addresses.list_all()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    rc_ips = list(filter(lambda x: x.tags is not None and x.tags.get(
        'managed') == 'rc', sorted_entities))
    ips = []

    for ip in list(rc_ips):
        output_dict = {}
        label = f"{ip.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = ip.id
        ips.append(output_dict)

    return ips

def get_service_endpoints(location):
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.available_endpoint_services.list(location=location)
    endpoints = []

    for endpoint in list(entities):
        output_dict = {}
        label = f"{endpoint.name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = endpoint.name
        endpoints.append(output_dict)

    return endpoints


def custom_endpoint(action, params, boto3_session, user_session):
    if action == "resource_groups":
        return get_resource_groups(params)
    elif action == "key_vaults":
        return get_key_vaults()
    elif action == "locations":
        return get_locations()
    elif action == "users":
        return get_object_ids()
    elif action == "route_tables":
        return get_route_tables()
    elif action == "vnets":
        return get_vnets()
    elif action == "vnets_ids":
        return get_vnets_ids()
    elif action == "log_workspaces":
        return get_log_workspaces()
    elif action == "nsgs":
        return get_nsgs()
    elif action == "watchers":
        return get_watchers()
    elif action == "storage_accounts":
        return get_storage_accounts()
    elif action == "subnets":
        return get_subnets()
    elif action == "ips":
        return get_ips()
    elif action == "service_endpoints":
        return get_service_endpoints(params.get("location"))
    else:
        pp(f"no such endpoint: {action}")
        return ["no such endpoint"]

    return []
