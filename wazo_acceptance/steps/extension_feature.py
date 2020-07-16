# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('the "{extension_name}" extension is enabled')
def given_the_extension_is_enabled(context, extension_name):
    context.helpers.extension_feature.enable(extension_name)



@given('the "{extension_name}" extension is disabled')
def given_the_extension_is_disabled(context, extension_name):
    context.helpers.extension_feature.disable(extension_name)
