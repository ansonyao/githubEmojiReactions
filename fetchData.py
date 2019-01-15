from pprint import PrettyPrinter
from gqlquery import getIssuesPagedRequest, getReactionsForIssueBody, getReactionsForCommentsRequest
import time

pp = PrettyPrinter(indent=4)

def getReactions(owner, name):
    results = {}
    issuesNumbers = getIssues(owner, name)
    for number in issuesNumbers:
        issueReactions = getReactionsOfIssue(owner, name, number) 
        results = mergeReactionDict(results, issueReactions)
    return results

def mergeReactionDict(oldDict, additionalDict):
    newDict = oldDict.copy()
    for key in additionalDict:
        if key in newDict:
            newDict[key] = newDict[key] + additionalDict[key]
        else:
            newDict[key] = additionalDict[key]
    return newDict

def getIssues(owner, name):
    issueNumbers = []
    cursor = None
    hasNextPage = True

    def getId(obj):
        return obj['node']['number']
    while hasNextPage:
        result = getIssuesPagedRequest(owner, name, cursor)
        hasNextPage = result['data']['repository']['issues']['pageInfo']['hasNextPage']
        issues = result['data']['repository']['issues']['edges']
        issueNumbers.extend(map(getId, issues))
        if len(issues) > 0:
            cursor = issues[-1]['cursor']
        if result['data']['rateLimit']['remaining'] < 100:
            time.sleep(60 * 60)
    return issueNumbers

def getReactionsOfIssue(owner, name, issueNumber):
    issueBodyReactions = getReactionsOfIssueBody(owner, name, issueNumber)
    issueCommentReactions = getReactionsOfIssueComments(owner, name, issueNumber)
    result = mergeReactionDict(issueBodyReactions, issueCommentReactions)
    pp.pprint(f"issue {issueNumber}:")
    pp.pprint(result)
    return result


def getReactionsOfIssueBody(owner, name, issueNumber):
    results = {}
    cursor = None
    hasNextPage = True

    def getContent(obj):
        return obj['node']['content']
    while hasNextPage:
        result = getReactionsForIssueBody(owner, name, issueNumber, cursor)
        reactions = result['data']['repository']['issue']['reactions']
        hasNextPage = reactions["pageInfo"]['hasNextPage']
        if len(reactions["edges"]) > 0:
            cursor = reactions["edges"][-1]["cursor"]
        contents = map(getContent, reactions["edges"])

        for content in contents:
            if content in results:
                results[content] += 1
            else:
                results[content] = 1

        if result['data']['rateLimit']['remaining'] < 100:
            time.sleep(60 * 60)
    return results

def getReactionsOfIssueComments(owner, name, issueNumber):
    results = {}
    cursor = None
    hasNextPage = True

    def getContent(obj):
        return obj['node']['reactions']
    while hasNextPage:
        result = getReactionsForCommentsRequest(owner, name, issueNumber, cursor)
        comments = result['data']['repository']['issue']['comments']
        hasNextPage = comments["pageInfo"]['hasNextPage']
        if len(comments["edges"]) > 0:
            cursor = comments["edges"][-1]["cursor"]
        reactions = map(getContent, comments["edges"])
        
        for reaction in reactions:
            for node in reaction["nodes"]:
                content = node["content"]
                if content in results:
                    results[content] += 1
                else:
                    results[content] = 1
        if result['data']['rateLimit']['remaining'] < 100:
            time.sleep(60 * 60)
    return results