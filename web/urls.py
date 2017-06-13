# !/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import user,account,home,asset

urlpatterns = (
    url(r'^login$',account.LoginView.as_view()),
    url(r'^logout$',account.LogoutView.as_view()),
    url(r'^index$',home.IndexView.as_view()),
    url(r'^cmdb_index$',home.CMDBView.as_view()),
    url(r'^chart-(?P<chart_type>\w+)$',home.ChartView.as_view()),
    url(r'^asset$', asset.AssetListView.as_view()),
    url(r'^assets$', asset.AssetJsonView.as_view()),
    url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+)$',asset.AssetDetailView.as_view()),
    url(r'^add_asset$',asset.AddAssetView.as_view()),
    url(r'^idc$', asset.IDCListView.as_view()),
    url(r'^idc_json$', asset.IDCJsonView.as_view()),
)