# Copyright 2011 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import splunk.clilib.cli_common
import re

'''
Functions for retriveing settigs from splunkgit conf file.
Author: Emre Berge Ergenekon, Petter Eriksson
'''
SPLUNKGIT_GIT_SETTINGS = splunk.clilib.cli_common.getConfStanza('splunkgit','git')
SPLUNKGIT_GITHUB_SETTINGS = splunk.clilib.cli_common.getConfStanza('splunkgit','github')
SPLUNK_SETTINGS = splunk.clilib.cli_common.getConfStanza('splunkgit','splunk')

class GithubUserRepo(object):

    def __init__(self, user, repo):
        self._user = user
        self._repo = repo

    def get_user(self):
        return self._user

    def get_repo(self):
        return self._repo

def git_repo_addresses():
    return SPLUNKGIT_GIT_SETTINGS['repo_addresses']

def github_user_login_name():
    return SPLUNKGIT_GITHUB_SETTINGS['user_login_name']

def github_repo_name():
    return SPLUNKGIT_GITHUB_SETTINGS['repo_name']

def splunk_user_name():
    return SPLUNK_SETTINGS['user']

def splunk_password():
    return SPLUNK_SETTINGS['password']

def github_user_repos():
    space_separated_repo_addresses = git_repo_addresses()
    repo_addresses = space_separated_repo_addresses.split(' ')
    return github_user_repos_from_repo_addresses(repo_addresses)

def github_user_repos_from_repo_addresses(repo_addresses):
    github_user_repos = []
    for repo_address in repo_addresses:
        github_user_repo = github_user_repo_from_repo_address(repo_address)
        if github_user_repo is not None:
            github_user_repos.append(github_user_repo)
    return github_user_repos

def github_user_repo_from_repo_address(repo_address):
    user_match = re.search('(?<=github\.com.)(.*)(?=/)', repo_address) # match anything after github.com until /
    if user_match is not None:
        user = user_match.group(0)
        repo_match = re.search("(?<=%s/)(.*?\.git)" % user, repo_address) # match <something>.git after user/
        if repo_match is not None:
            repo = repo_match.group(0)
            return GithubUserRepo(user, repo)
    return None

if __name__ == '__main__':
    print git_repo_addresses()
