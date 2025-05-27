#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 80
    APP_ID = os.environ.get("MicrosoftAppId", "f8d649ca-02e3-4ad7-8725-4536a1f792d1")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "MYI8Q~GgJ_Z0yuIMER7ByyixY31b-WeAuXft5bJl")
