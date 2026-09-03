import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


def generate_test_cases(requirement: str):

    prompt = f"""
You are an expert QA engineer.

Generate detailed software test cases for this requirement:

{requirement}

Generate positive, negative, and boundary/edge test cases.

Return ONLY valid JSON.

The JSON must be an array of test case objects.

Each test case must have exactly these fields:

[
  {{
    "test_case_id": "TC_001",
    "requirement_id": "REQ_001",
    "title": "Test case title",
    "description": "Preconditions and description",
    "steps": [
      {{
        "step": "1. First test step",
        "test_data": "Test data",
        "expected_result": "Expected result"
      }},
      {{
        "step": "2. Second test step",
        "test_data": "Test data",
        "expected_result": "Expected result"
      }}
    ],
    "test_results": "Not Executed",
    "priority": "High",
    "severity": "Major",
    "defect_id": "",
    "assignee": "",
    "comment": ""
  }}
]


Coverage rules:

- Analyze the requirement deeply before generating test cases.
- Generate comprehensive test coverage.
- Prefer 25-50 test cases for complex requirements when justified.
- Do not artificially stop at 20 test cases.
- Do not generate test cases just to increase the count.
- Every test case must cover a meaningful scenario or risk.
- Do not create duplicate or nearly identical test cases.
- Make sure important business rules have both positive and negative coverage.
- Make sure boundary conditions are tested.
- Make sure failure and recovery scenarios are tested.
- Cover the requirement from every relevant testing angle.

Consider ALL relevant testing angles below.

For each category, determine whether it applies to the requirement.
If it applies, generate at least 1 meaningful test case for that category.

Testing categories:

1. Positive / happy path
2. Negative scenarios
3. Boundary values
4. Equivalence partitioning
5. Mandatory field validation
6. Empty/null values
7. Invalid data formats
8. Minimum values
9. Maximum values
10. Special characters
11. Business rules
12. Authentication
13. Authorization
14. Different user roles
15. Security
16. API manipulation
17. Data integrity
18. Database validation
19. Integration
20. Error handling
21. Network failures
22. Timeout scenarios
23. Recovery scenarios
24. Duplicate requests
25. Double-click / repeated submission
26. Concurrency
27. Session timeout
28. Performance
29. Browser compatibility
30. Mobile compatibility
31. Accessibility
32. Localization
33. Date/time handling
34. Regression scenarios
35. Usability

Only include categories that are relevant to the requirement.

For every test case:

- Give a unique test case ID.
- Give a meaningful title.
- Include the requirement ID.
- Provide preconditions and description.
- Provide clear and executable test steps.
- Provide appropriate test data.
- Provide expected results.
- Assign priority.
- Assign severity.
- Avoid duplicate or nearly identical test cases.

Each test case should contain 3 to 7 detailed test steps.

Return ONLY valid JSON.
Do not return Markdown.
Do not return ```json.
Return only the JSON array.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove accidental markdown formatting
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError as e:
        print("Gemini returned invalid JSON:")
        print(text)

        raise ValueError(
            f"Gemini returned invalid JSON: {str(e)}"
        )