from typing import Literal

import json
from requests import post


class Base_problem:
    id = None
    title = None
    title_slug = None
    difficulty = None
    ac_rate = None
    topic_tags = []
    likes = None
    dislikes = None
    content = None


class Random_problem(Base_problem):
    def __str__(self):
        return self.id

    def __init__(
        self,
        diff: Literal["EASY", "MEDIUM", "HARD"] = None,
        *tags: Literal[
            "array",
            "atring",
            "hash-table",
            "dynamic-programming",
            "math",
            "sorting",
            "greedy",
            "depth-first-search",
            "database",
            "binary-search",
            "breadth-first-search",
            "tree",
            "matrix",
            "two-pointers",
            "binary-tree",
            "bit-manipulation",
            "heap-priority-queue",
            "stack",
            "graph",
            "prefix-sum",
            "design",
            "simulation",
            "counting",
            "backtracking",
            "sliding-window",
            "union-find",
            "linked-list",
            "ordered-set",
            "monotonic-stack",
            "recursion",
            "enumeration",
            "trie",
            "divide-and-conquer",
            "binary-search-tree",
            "bitmask",
            "queue",
            "number-theory",
            "memoization",
            "segment-tree",
            "geometry",
            "topological-sort",
            "binary-indexed-tree",
            "hash-function",
            "game-theory",
            "shortest-path",
        ]
    ):
        query = """
query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {
        randomQuestion(categorySlug: $categorySlug, filters: $filters) {
            frontendQuestionId: questionFrontendId
            questionId
            title
            titleSlug
            difficulty
            acRate
            topicTags {
                name
                id
                slug
                }
            likes
            dislikes
            content
        }
    }
        """
        variables = {
            "categorySlug": "",
            "filters": {
                "difficulty": diff,
                "tags": tags,
                "searchKeywords": "",
            },
        }

        data = json.dumps({"query": query, "variables": variables})
        response = post(url, headers={"Content-type": "application/json"}, data=data)
        if response.status_code == 200:
            problem = response.json()["data"]["randomQuestion"]
            if problem:
                self.id = problem["frontendQuestionId"]
                self.title = problem["title"]
                self.title_slug = problem["titleSlug"]
                self.difficulty = problem["difficulty"]
                self.ac_rate = float(problem["acRate"])
                self.topic_tags = problem["topicTags"]
                self.likes = int(problem["likes"])
                self.dislikes = int(problem["dislikes"])
                self.content = problem["content"]


url = "https://leetcode.com/graphql/"
order = [None, "FRONTEND_ID", "AC_RATE", "DIFFICULTY"]
sort = ["ASCENDING", "DESCENDING"]
topic_tag = {
    "names": [
        "Array",
        "String",
        "Hash Table",
        "Dynamic Programming",
        "Math",
        "Sorting",
        "Greedy",
        "Depth-First Search",
        "Database",
        "Binary Search",
        "Breadth-First Search",
        "Tree",
        "Matrix",
        "Two Pointers",
        "Binary Tree",
        "Bit Manipulation",
        "Heap (Priority Queue)",
        "Stack",
        "Graph",
        "Prefix Sum",
        "Design",
        "Simulation",
        "Counting",
        "Backtracking",
        "Sliding Window",
        "Union Find",
        "Linked List",
        "Ordered Set",
        "Monotonic Stack",
        "Recursion",
        "Enumeration",
        "Trie",
        "Divide and Conquer",
        "Binary Search Tree",
        "Bitmask",
        "Queue",
        "Number Theory",
        "Memoization",
        "Segment Tree",
        "Geometry",
        "Topological Sort",
        "Binary Indexed Tree",
        "Hash Function",
        "Game Theory",
        "Shortest Path",
    ],
    "slugs": [
        "array",
        "atring",
        "hash-table",
        "dynamic-programming",
        "math",
        "sorting",
        "greedy",
        "depth-first-search",
        "database",
        "binary-search",
        "breadth-first-search",
        "tree",
        "matrix",
        "two-pointers",
        "binary-tree",
        "bit-manipulation",
        "heap-priority-queue",
        "stack",
        "graph",
        "prefix-sum",
        "design",
        "simulation",
        "counting",
        "backtracking",
        "sliding-window",
        "union-find",
        "linked-list",
        "ordered-set",
        "monotonic-stack",
        "recursion",
        "enumeration",
        "trie",
        "divide-and-conquer",
        "binary-search-tree",
        "bitmask",
        "queue",
        "number-theory",
        "memoization",
        "segment-tree",
        "geometry",
        "topological-sort",
        "binary-indexed-tree",
        "hash-function",
        "game-theory",
        "shortest-path",
    ],
}


### 그래프큐엘 쿼리 참고

# 랜덤 문제 고르기
# query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {
#         randomQuestion(categorySlug: $categorySlug, filters: $filters) {
#             frontendQuestionId: questionFrontendId
#             questionId
#             title
#             titleSlug
#             difficulty
#             acRate
#             topicTags {
#                 name
#                 id
#                 slug
#                 }
#             likes
#             dislikes
#             content
#             freqBar
#             isFavor
#             paidOnly: isPaidOnly
#             status
#             hasSolution
#             hasVideoSolution
#         }
#     }

# 문제 리스트 불러오기
# query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
#     problemsetQuestionList: questionList(
#         categorySlug: $categorySlug
#         limit: $limit
#         skip: $skip
#         filters: $filters
#     ) {
#         total: totalNum
#         questions: data {
#             frontendQuestionId: questionFrontendId
#             questionId
#             title
#             titleSlug
#             difficulty
#             acRate
#             topicTags {
#                 name
#                 id
#                 slug
#                 }
#             likes
#             dislikes
#             content
#             freqBar
#             isFavor
#             paidOnly: isPaidOnly
#             status
#             hasSolution
#             hasVideoSolution
#         }
#     }
# }

# 변수 (QuestionListFilterInput)
# {
#     "categorySlug": "",
#     "filters": {
#         "orderBy": [None, "FRONTEND_ID", "AC_RATE", "DIFFICULTY"],
#         "sortOrder": ["ASCENDING", "DESCENDING"],
#         "difficulty": ["EAsy", "MEDIUM", "HARD"],
#         "tags": [],
#         "searchKeywords": "",
#         "premiumOnly": true
#     },
#     "limit": 0,
#     "skip": 0,
# }
