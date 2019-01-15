import requests
import os
from githubtoken import bearerToken

def getHeaders():
    if bearerToken:
        return {"Authorization": f"Bearer {bearerToken}"}
    else:
        return {}

def getIssuesPagedRequest(owner, name, cursor): 
    issueQuery = """
        query fetchGithubIssues($owner: String!, $name: String!, $cursor: String) {
            repository(owner: $owner, name: $name) {
                issues(first: 100, after: $cursor) {
                    totalCount
                    pageInfo{
                        hasNextPage
                    }
                    edges{
                        node{
                            number
                        }
                        cursor
                    }
                }
            }
            rateLimit {
                limit
                cost
                remaining
                resetAt
            }
        }
    """
    if cursor == None:
        variables = f"{{\"owner\": \"{owner}\", \"name\": \"{name}\"}}" 
    else:
        variables = f"{{\"owner\": \"{owner}\", \"name\": \"{name}\", \"cursor\": \"{cursor}\" }}" 

    result = requests.post('https://api.github.com/graphql', json={'query': issueQuery, 'variables': variables}, headers=getHeaders()).json()
    return result


def getReactionsForIssueBody(owner, name, issueNumber, cursor): 
    issueQuery = """
        query fetchReactions($owner: String!, $name: String!, $issueNumber: Int!, $cursor: String) {
            repository(owner: $owner, name: $name) {
                issue(number: $issueNumber){
                    reactions(first: 100, after: $cursor){
                        totalCount
                        pageInfo{
                            hasNextPage
                        }
                        edges{
                            node{
                                content
                            }
                        cursor
                    }
                }
            }
        }
        rateLimit {
            limit
            cost
            remaining
            resetAt
        }
}
    """
    if cursor == None:
        variables = f"{{\"owner\": \"{owner}\", \"name\": \"{name}\", \"issueNumber\": {issueNumber}}}" 
    else:
        variables = f"{{\"owner\": \"{owner}\", \"name\": \"{name}\", \"issueNumber\": {issueNumber}, \"cursor\": \"{cursor}\" }}" 

    result = requests.post('https://api.github.com/graphql', json={'query': issueQuery, 'variables': variables}, headers=getHeaders()).json()
    return result

def getReactionsForCommentsRequest(owner, name, issueNumber, cursor):
    query = """
        query fetchComments($owner: String!, $name: String!, $issueNumber: Int!, $cursor: String) {
            repository(owner: $owner, name: $name) {
                issue(number: $issueNumber){
                    comments(first: 100, after: $cursor){
                        totalCount
                        pageInfo{
                            hasNextPage
                        }
                        edges{
                            node{
                                id
                                reactions(first: 100) {
                                    nodes{
                                        content
                                    }
                                }
                            }
                            cursor
                        }
                    }
                }
            }
            rateLimit {
                limit
                cost
                remaining
                resetAt
            }
        }
    """
    if cursor == None:
        variables = f"{{\"owner\": \"{owner}\", \"name\": \"{name}\", \"issueNumber\": {issueNumber}}}" 
    else:
        variables = f"{{\"owner\": \"{owner}\", \"name\": \"{name}\", \"issueNumber\": {issueNumber}, \"cursor\": \"{cursor}\" }}" 

    result = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=getHeaders()).json()
    return result