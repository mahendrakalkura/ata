# -*- coding: utf-8 -*-

from boto3 import client
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from docker import Client
from simplejson import dumps


def index(request):
    return render(request, 'index.html')


def refresh(request):
    containers = []
    docker = get_docker()
    # I am not using `all=True` because only running containers are to be
    # listed.
    for container in docker.containers():
        container = docker.inspect_container(container['Id'])
        id = container['Id']
        name = container['Name'].lstrip('/')
        status = get_status(container['State']['Status'])
        current_version = get_version(container['Config']['Image'])
        containers.append(dict(
            id=id,
            name=name,
            status=status,
            current_version=current_version,
            new_version=None,
            spinner=False,
            urls=dict(
                check=reverse('check', args=[id]),
                update=reverse('update', args=[id]),
            ),
        ))
    return HttpResponse(dumps(containers), content_type='application/json')


def check(request, id):
    docker = get_docker()
    container = docker.inspect_container(id)
    image = docker.inspect_image(container['Config']['Image'])
    registry, repository = get_registry_repository(image['RepoTags'])
    images = get_boto_images(registry, repository)
    # I am sending back the new version associated with the image.
    # The actual version check logic is embedded inside the template, which
    # will be evaluated by Angular.
    new_version = get_new_version(images)
    data = dict(new_version=new_version)
    return HttpResponse(dumps(data), content_type='application/json')


@require_http_methods(['POST'])
def update(request, id):
    docker = get_docker()
    container = docker.inspect_container(id)
    image = docker.inspect_image(container['Image'])
    registry, repository = get_registry_repository(image['RepoTags'])
    images = get_boto_images(registry, repository)
    new_version = get_new_version(images)
    repository = get_repository(image['RepoTags'])
    # docker pull ...
    docker.pull(repository=repository, tag=new_version, stream=False)
    # docker stop ...
    docker.stop(id)
    # docker rm ...
    docker.remove_container(id)
    # docker run ...
    container = docker.create_container(
        image='{repository:s}:{new_version:s}'.format(
            repository=repository,
            new_version=new_version,
        ),
    )
    docker.start(container=container['Id'])
    return HttpResponse(dumps({}), content_type='application/json')


def get_boto():
    return client(
        'ecr',
        aws_access_key_id=settings.BOTO['aws_access_key_id'],
        aws_secret_access_key=settings.BOTO['aws_secret_access_key'],
        region_name=settings.BOTO['region_name'],
    )


def get_boto_images(registry, repository):
    images = []
    client = get_boto()
    next_token = None
    while True:
        kwargs = dict(
            registryId=registry,
            repositoryName=repository,
            maxResults=100,
            nextToken=next_token if next_token else '',
        )
        if not kwargs['nextToken']:
            del kwargs['nextToken']
        response = client.list_images(**kwargs)
        if 'imageIds' in response:
            for image in response['imageIds']:
                digest = ''
                if 'imageDigest' in image:
                    digest = image['imageDigest']
                tag = ''
                if 'imageTag' in image:
                    tag = image['imageTag']
                if digest and tag:
                    images.append(dict(digest=digest, tag=tag))
        if 'nextToken' in response:
            next_token = response['nextToken']
        if not next_token:
            break
    return images


def get_docker():
    return Client(base_url=settings.DOCKER)


def get_new_version(images):
    '''
    Input: [
        {
            'digest': $digest,
            'tag': $tag
        },
        ...,
        ...,
        ...,
    ]
    Output: $tag of the last item in the alphabetically sorted input
            (excluding empty tags)
    '''
    image_versions = [image['tag'] for image in images]
    image_versions = sorted(image_versions)
    return image_versions[-1]


def get_registry_repository(items):
    # Input: $registry/$repository:$version,
    # Output: $registry and $repository (separately)
    for item in items:
        try:
            item = item.split('/', 1)
            item[0] = item[0].split('.', 1)
            item[1] = item[1].split(':', 1)
            return item[0][0], item[1][0]
        except IndexError:
            pass
    return '', ''


def get_repository(items):
    '''
    Input: [
        $registry/$repository:$version,
        ...,
        ...,
        ...,
    ]
    Output: $version of the first item in the input
    '''
    for item in items:
        try:
            item = item.split(':', 1)
            return item[0]
        except IndexError:
            pass
    return ''


def get_status(status):
    return status.title()


def get_version(version):
    # Input: $registry/$repository:$version
    # Output: $version
    return version.split(':')[-1]


def is_update_available(versions, version):
    if versions[-1] != version:
        return True
    return False
