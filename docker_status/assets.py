# -*- coding: utf-8 -*-

from django_assets import Bundle, register

javascripts = Bundle(
    'bower_components/jquery/dist/jquery.js',
    'bower_components/angular/angular.js',
    'bower_components/angular-loading-bar/build/loading-bar.js',
    'bower_components/bootstrap/dist/js/bootstrap.js',
    'javascripts/all.js',
    filters='rjsmin',
    output='assets.js',
)

stylesheets = Bundle(
    'bower_components/angular-loading-bar/build/loading-bar.css',
    'bower_components/bootstrap/dist/css/bootstrap.css',
    'bower_components/bootstrap/dist/css/bootstrap-theme.css',
    'stylesheets/all.css',
    filters='cssmin',
    output='assets.css',
)

register('javascripts', javascripts)
register('stylesheets', stylesheets)
