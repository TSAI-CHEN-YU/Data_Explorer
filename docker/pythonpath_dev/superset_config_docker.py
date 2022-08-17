#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This is an example "local" configuration file. In order to set/override config
# options that ONLY apply to your local environment, simply copy/rename this file
# to docker/pythonpath/superset_config_docker.py
# It ends up being imported by docker/superset_config.py which is loaded by
# superset/config.py
#



# Maximum number of rows displayed in SQL Lab UI Is set to avoid out of memory
DISPLAY_MAX_ROW = 10

#Default row limit for SQL Lab queries. Is overridden by setting a new limit in the SQL Lab UI
DEFAULT_SQLLAB_LIMIT  =  10

# Ignore the warning
CACHE_NO_NULL_WARNING = True

# Flask App Builder configuration
# Your App secret key
SECRET_KEY = 'Stanley1127'


APP_NAME = "Explorer"
FAVICONS = [{"href": "/static/assets/images/custom_favicon.png"}]
APP_ICON = "/static/assets/images/custom_logo.png"