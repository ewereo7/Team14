"""Shared fictional data for the Make-It-All prototype.

Owner: Person 6 (Design / Data / QA).  Everyone else only READS this file.

Every record is fictional. Dates are fixed (not "today") so every screen and
every screenshot tells the same story.

Usage:
    from sample_data import get_sample_data
    data = get_sample_data()
"""
from copy import deepcopy
from datetime import date

# ---- Agreed task contract (do not rename fields without telling the team) ----
TASK_FIELDS = (
    "id", "project_id", "title", "assigned_to",
    "start_date", "end_date", "status", "progress", "estimated_hours",
)
STATUSES = ("Completed", "In Progress", "Scheduled", "At Risk")
ROLES = ("Employee", "Team Leader", "Manager")

# Workload warning thresholds (unfinished tasks / estimated hours)
WORKLOAD_TASK_LIMIT = 5
WORKLOAD_HOURS_LIMIT = 64

EMPLOYEES = [
    {"id": 1, "name": "James Shah",    "email": "james.shah@make-it-all.co.uk",    "role": "Manager",     "team": "Management"},
    {"id": 2, "name": "Noah Okafor",   "email": "noah.okafor@make-it-all.co.uk",   "role": "Team Leader", "team": "Web"},
    {"id": 3, "name": "Hannah Reid",   "email": "hannah.reid@make-it-all.co.uk",   "role": "Team Leader", "team": "Platform"},
    {"id": 4, "name": "Amira Hussain", "email": "amira.hussain@make-it-all.co.uk", "role": "Employee",    "team": "Web"},
    {"id": 5, "name": "Ben Johnson",   "email": "ben.johnson@make-it-all.co.uk",   "role": "Employee",    "team": "Web"},
    {"id": 6, "name": "Chloe Nguyen",  "email": "chloe.nguyen@make-it-all.co.uk",  "role": "Employee",    "team": "Web"},
    {"id": 7, "name": "Kash Patel",    "email": "kash.patel@make-it-all.co.uk",    "role": "Employee",    "team": "Platform"},
    {"id": 8, "name": "Erin Walsh",    "email": "erin.walsh@make-it-all.co.uk",    "role": "Employee",    "team": "Platform"},
]

# leader_id is an employee id (same style as PROJECTS); "name" matches EMPLOYEES["team"]
TEAMS = [
    {"id": 11, "name": "Management", "leader_id": 1},
    {"id": 12, "name": "Web",        "leader_id": 2},
    {"id": 13, "name": "Platform",   "leader_id": 3},
]

PROJECTS = [
    {"id": 21, "name": "Website Redesign",        "leader_id": 2, "start_date": "2026-10-26", "end_date": "2026-11-27",
     "description": "Refresh the public website and product pages."},
    {"id": 22, "name": "Customer Portal Upgrade", "leader_id": 3, "start_date": "2026-10-28", "end_date": "2026-12-04",
     "description": "Move the customer portal to the new platform."},
    {"id": 23, "name": "Office Printing Rollout", "leader_id": 3, "start_date": "2026-11-02", "end_date": "2026-11-20",
     "description": "Replace shared printers and document the new process."},
]

# (id, project_id, title, assignee_id, start, end, status, progress, hours)
_TASKS = [
    (1,  21, "Stakeholder interviews",       2, "2026-10-26", "2026-10-28", "Completed",   100, 6),
    (2,  21, "Wireframes",                   4, "2026-10-27", "2026-10-30", "Completed",   100, 12),
    (3,  21, "UI design",                    4, "2026-10-29", "2026-11-06", "In Progress",  55, 24),
    (4,  21, "Content migration",            6, "2026-11-02", "2026-11-13", "In Progress",  30, 20),
    (5,  21, "Front-end build",              5, "2026-11-04", "2026-11-18", "In Progress",  20, 32),
    (6,  21, "Accessibility review",         6, "2026-11-12", "2026-11-17", "Scheduled",     0, 8),
    (7,  21, "Browser and device testing",   5, "2026-11-16", "2026-11-24", "At Risk",       0, 16),
    (8,  21, "Launch",                       2, "2026-11-25", "2026-11-27", "Scheduled",     0, 6),
    (9,  22, "Requirements workshop",        3, "2026-10-28", "2026-10-30", "Completed",   100, 6),
    (10, 22, "Data model",                   7, "2026-10-30", "2026-11-10", "In Progress",  60, 18),
    (11, 22, "Login and permissions",        7, "2026-11-04", "2026-11-20", "At Risk",      25, 30),
    (12, 22, "Task list screens",            8, "2026-11-09", "2026-11-25", "In Progress",  15, 24),
    (13, 22, "Reporting dashboard",          8, "2026-11-16", "2026-12-01", "Scheduled",     0, 26),
    (14, 22, "User acceptance testing",      3, "2026-11-26", "2026-12-04", "Scheduled",     0, 14),
    (15, 23, "Compare printer suppliers",    7, "2026-11-02", "2026-11-06", "In Progress",  70, 8),
    (16, 23, "Order and install printers",   8, "2026-11-09", "2026-11-16", "Scheduled",     0, 12),
    (17, 23, "Write printing paper guide",   5, "2026-11-16", "2026-11-20", "Scheduled",     0, 4),
    (18, 21, "Update footer and legal pages", 5, "2026-11-05", "2026-11-09", "In Progress",  40, 6),
    (19, 21, "SEO checks",                   5, "2026-11-10", "2026-11-13", "Scheduled",     0, 5),
    (20, 21, "Fix navigation bugs",          5, "2026-11-06", "2026-11-10", "In Progress",  10, 7),
]

TOPICS = [
    {"id": 31, "name": "Software Development"},
    {"id": 32, "name": "Software Issues"},
    {"id": 33, "name": "Printing"},
    {"id": 34, "name": "Hardware Setup"},
]

# (id, topic_id, author_id, title, body, created, [(reply_id, author_id, body, created)])
_POSTS = [
    (1, 33, 5, "How to order printing paper",
     "Order through the Facilities form. Standard A4 is approved up to 10 reams. Anything larger needs team leader sign-off.",
     "2026-10-20", [(1, 6, "Does this include coloured paper?", "2026-10-21"),
                    (2, 5, "Yes, but select 'Specialist' on the form.", "2026-10-21")]),
    (2, 32, 7, "Login page loops back after sign-in",
     "Cause: stale session cookie. Fix: clear cookies for the portal domain, then sign in again.",
     "2026-10-22", [(3, 8, "Fixed it for me, thanks.", "2026-10-22")]),
    (3, 31, 4, "Branch naming rules",
     "Use feature/<short-name>. Open a pull request and ask one teammate to review before merging.",
     "2026-10-23", []),
    (4, 34, 8, "Connecting to the second-floor printer",
     "Install the driver from the shared drive, then add the printer by IP address 10.0.2.45.",
     "2026-10-24", [(4, 7, "Worked on Windows 11 too.", "2026-10-25")]),
    (5, 32, 6, "Images not loading on the staging site",
     "Check the CDN path in the settings file. A missing trailing slash caused broken image links.",
     "2026-10-26", []),
    (6, 32, 4, "Slow dashboard on large projects",
     "Add an index on project_id and load tasks in one query instead of one per row.",
     "2026-10-27", [(5, 7, "Can confirm: 4 seconds down to under 1.", "2026-10-27")]),
]

# Which fictional person each role-picker option signs in as (employee ids)
ROLE_USERS = {"Employee": 4, "Team Leader": 2, "Manager": 1}


def get_sample_data():
    """Return a fresh deep copy so one page can never change another page's data."""
    name = {e["id"]: e["name"] for e in EMPLOYEES}
    tasks = [{
        "id": i, "project_id": pid, "title": title, "assigned_to": name[who],
        "start_date": start, "end_date": end, "status": status,
        "progress": prog, "estimated_hours": hours,
    } for (i, pid, title, who, start, end, status, prog, hours) in _TASKS]
    posts = [{
        "id": i, "topic_id": topic, "author": name[author], "title": title,
        "body": body, "created": created,
        "replies": [{"id": r[0], "author": name[r[1]], "body": r[2], "created": r[3]} for r in replies],
    } for (i, topic, author, title, body, created, replies) in _POSTS]
    return deepcopy({
        "employees": EMPLOYEES, "teams": TEAMS, "projects": PROJECTS, "tasks": tasks,
        "topics": TOPICS, "posts": posts,
        "role_users": {role: name[i] for role, i in ROLE_USERS.items()},
    })


# ---------------------------- helpers other pages can reuse ----------------------------
def tasks_for(data, person=None, project_id=None):
    return [t for t in data["tasks"]
            if (person is None or t["assigned_to"] == person)
            and (project_id is None or t["project_id"] == project_id)]


def project_progress(data, project_id):
    """Average task progress for a project, 0-100 (whole number)."""
    ts = tasks_for(data, project_id=project_id)
    return round(sum(t["progress"] for t in ts) / len(ts)) if ts else 0


def workload(data):
    """List of dicts (person, open_tasks, hours, overloaded), busiest first."""
    out = []
    for e in data["employees"]:
        if e["role"] == "Manager":
            continue
        open_ts = [t for t in tasks_for(data, person=e["name"]) if t["status"] != "Completed"]
        hours = sum(t["estimated_hours"] for t in open_ts)
        out.append({"person": e["name"], "open_tasks": len(open_ts), "hours": hours,
                    "overloaded": len(open_ts) >= WORKLOAD_TASK_LIMIT or hours >= WORKLOAD_HOURS_LIMIT})
    return sorted(out, key=lambda w: (-w["open_tasks"], w["person"]))


def parse_date(text):
    return date.fromisoformat(text)


def validate_data(data):
    """Return a list of problems (empty list means the data is consistent)."""
    problems = []
    names = {e["name"] for e in data["employees"]}
    emp_ids = {e["id"] for e in data["employees"]}
    projects = {p["id"]: p for p in data["projects"]}
    topic_ids = {t["id"] for t in data["topics"]}

    for label, rows in (("employee", data["employees"]), ("team", data["teams"]), ("project", data["projects"]),
                        ("task", data["tasks"]), ("topic", data["topics"]), ("post", data["posts"])):
        ids = [r["id"] for r in rows]
        if len(ids) != len(set(ids)):
            problems.append(f"duplicate {label} ids")

    emails = [e["email"] for e in data["employees"]]
    if len(emails) != len(set(emails)):
        problems.append("duplicate employee emails")
    for e in data["employees"]:
        if not e["email"].endswith("@make-it-all.co.uk"):
            problems.append(f"{e['name']}: not a staff email address")

    for t in data["tasks"]:
        tag = f"task {t.get('id')} '{t.get('title')}'"
        if set(TASK_FIELDS) - set(t):
            problems.append(f"{tag}: missing fields")
            continue
        proj = projects.get(t["project_id"])
        if proj is None:                       problems.append(f"{tag}: unknown project")
        if t["assigned_to"] not in names:      problems.append(f"{tag}: unknown assignee")
        if t["status"] not in STATUSES:        problems.append(f"{tag}: bad status")
        if not 0 <= t["progress"] <= 100:      problems.append(f"{tag}: progress out of range")
        if parse_date(t["end_date"]) < parse_date(t["start_date"]):
            problems.append(f"{tag}: ends before it starts")
        if t["status"] == "Completed" and t["progress"] != 100:
            problems.append(f"{tag}: completed but progress is not 100")
        if t["status"] == "Scheduled" and t["progress"] != 0:
            problems.append(f"{tag}: scheduled but progress is not 0")
        if proj and not (proj["start_date"] <= t["start_date"] and t["end_date"] <= proj["end_date"]):
            problems.append(f"{tag}: outside its project dates")

    team_names = {t["name"] for t in data["teams"]}
    by_id = {e["id"]: e for e in data["employees"]}
    for e in data["employees"]:
        if e["team"] not in team_names:
            problems.append(f"{e['name']}: unknown team '{e['team']}'")
    for t in data["teams"]:
        leader = by_id.get(t["leader_id"])
        if leader is None:
            problems.append(f"team '{t['name']}': unknown leader")
        elif leader["team"] != t["name"]:
            problems.append(f"team '{t['name']}': leader {leader['name']} belongs to a different team")
    for p in data["projects"]:
        if p["leader_id"] not in emp_ids:
            problems.append(f"project '{p['name']}': unknown leader")
    for po in data["posts"]:
        if po["topic_id"] not in topic_ids: problems.append(f"post {po['id']}: unknown topic")
        if po["author"] not in names:       problems.append(f"post {po['id']}: unknown author")
        for r in po["replies"]:
            if r["author"] not in names:    problems.append(f"reply {r['id']}: unknown author")
    return problems


if __name__ == "__main__":
    d = get_sample_data()
    issues = validate_data(d)
    print("Data OK" if not issues else "\n".join(issues))
    for w in workload(d):
        print(w)
