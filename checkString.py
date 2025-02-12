import re
import json

text = """<think>
Alright, let me see what the user is asking for...
</think>

```json
{
    "Area": "Boxmeer canteen",
    "Category": "Other",
    "Company": "BioCore Manufacturing Facility",
    "Description": "Leaving spilled coffee on tables, staining the table and putting a paper plate over it so no one can see the spill",
    "Observation Date": "2020-12-15",
    "Observation Type": "spills in kitchen",
    "Observer": "Neil Hutchinson",
    "Priority Level": 5,
    "Project": null,
    "Severity Level": "Critical",
    "Site": "kitchen",
    "Source": "Boxmeer",
    "Status": "Closed"
}
```"""

# Extract JSON using regex
match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)

if match:
    json_string = match.group(1)
    json_data = json.loads(json_string)
    print(json_data)
else:
    print("No JSON found.")
