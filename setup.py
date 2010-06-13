#!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
setup.py

Created by Jacob C. on 2010-06-13.
Copyright (c) 2010 Spaceship No Future. All rights reserved.
"""

__author__ = "SNF Labs <jacob@spaceshipnofuture.org>"

import os
import os.path

def create_data_directories():
    required_directories = [
        "data",
        os.path.join("data", "cache"),
        os.path.join("data", "logs"),
        os.path.join("data", "output"),
        os.path.join("data", "output", "images")
    ]
    for directory in required_directories:
        if not os.path.isdir(directory):
            os.makedirs(directory)