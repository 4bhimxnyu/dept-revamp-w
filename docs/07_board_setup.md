# Setting up the Jira board and GitHub repository

The guidelines require evidence of an Agile tool (Jira or Trello) and a GitHub repository. Both need your own accounts, so these two steps are yours to do. About 20 minutes.

## Jira (free plan)

1. Go to atlassian.com → Jira → create a free site → create a project with the **Scrum** template. Name it "Department Website Revamp".
2. Import the backlog with Jira's CSV import and choose `docs/jira_import.csv`. The menu location changes between Jira versions; search Jira's help for "import issues from CSV". If the import is not offered on your plan, create the 18 stories by hand from the CSV (about 10 minutes).
3. Map the columns: Summary → Summary, Issue Type → Issue Type, Priority → Priority, Story Points → Story point estimate, Description → Description, Labels → Labels.
4. Open **Backlog**. Create Sprint 1, Sprint 2 and Sprint 3 and drag the stories into them (the `sprint-1` / `sprint-2` / `sprint-3` labels tell you which). Leave the three `deferred` stories in the backlog.
5. Assign each story to the team member who owns it.
6. Start and complete each sprint with its real dates, moving stories across To Do → In Progress → Done as the work was actually done.
7. **Reports** → Burndown chart and Velocity chart are generated automatically. Take a screenshot of each for the report.

### If you prefer Trello

Create a board with lists: Product Backlog, Sprint Backlog, In Progress, In Review, Done. Add one card per story (copy the Summary and Description from the CSV), add labels for priority, a checklist for acceptance criteria, and assign members.

## GitHub

The project folder is already a Git repository with a commit history.

```bash
# create an empty repository on github.com first (no README), then:
git remote add origin https://github.com/<your-username>/department-website.git
git push -u origin main
```

After the push, the **Actions** tab runs the test suite automatically on every push (`.github/workflows/tests.yml`).

For individual contribution evidence, each team member should make their own commits from their own GitHub account. Good first commits: fill in your name and role in `docs/02_sprint_plan.md` and `docs/05_project_report.md`, and add one test for the part you own.
