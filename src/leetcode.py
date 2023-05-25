import json
from requests import post

url = "https://leetcode.com/graphql/"
order = [None, "FRONTEND_ID", "AC_RATE", "DIFFICULTY"]
sort = ["ASCENDING", "DESCENDING"]

def random_problem(**kwarg):
    query = """
    query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {
        randomQuestion(categorySlug: $categorySlug, filters: $filters) {
            questionId
            title
            titleSlug
            content
            difficulty
            status
            acRate
            likes
            dislikes
            topicTags{name, slug}
        }
    }
    """
    variables = {
        "categorySlug": "",
        "filters": {
            "difficulty": kwarg.get("diff", None),
            "tags": [],
            "searchKeywords": "",
        },
    }

    data = json.dumps({"query": query, "variables": variables})
    response = post(url, headers={"Content-type": "application/json"}, data=data)
    if response.status_code == 200:
        return {"ok": True, "result": response.json()["data"]["randomQuestion"]}

    else:
        return {"ok": False, "result": "error!!"}

# TODO 특정 조건의 문제를 불러오는 함수
# def problem_list(**kwarg):
#     query = """
#     query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
#     problemsetQuestionList: questionList(
#         categorySlug: $categorySlug
#         limit: $limit
#         skip: $skip
#         filters: $filters
#     ) {
#         total: totalNum
#         questions: data {
#             acRate
#             difficulty
#             freqBar
#             frontendQuestionId: questionFrontendId
#             isFavor
#             paidOnly: isPaidOnly
#             status
#             title
#             titleSlug
#             topicTags {
#                 name
#                 id
#                 slug
#                 }
#             hasSolution
#             hasVideoSolution
#         }
#     }
# }
#     """
#     variables = {
#         "categorySlug": "",
#         "filters": {
#             "orderBy": order[kwarg.get("order", 0)],
#             "sortOrder": sort[kwarg.get("sort", 0)],
#             "difficulty": kwarg.get("diff", None),
#         },
#         "limit": kwarg.get("limit", 5),
#         "skip": kwarg.get("skip", 0),
#     }

#     data = json.dumps({"query": query, "variables": variables})
#     response = post(url, headers={"Content-type": "application/json"}, data=data)
#     if response.status_code == 200:
#         problems = response.json()["data"]["problemsetQuestionList"]["questions"]
#         for p in problems:
#             print(p)
#             print("////////")

#         return {
#             "ok": True,
#             "result": response.json()["data"]["problemsetQuestionList"]["questions"],
#         }

#     else:
#         return {"ok": False, "result": "error!!"}
