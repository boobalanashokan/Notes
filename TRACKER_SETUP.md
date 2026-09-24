# MLOps GitHub Tracker Setup

## Normal workflow

1.  Keep your study notes as Markdown files anywhere under the
    repository.
2.  Mark a topic complete explicitly, for example:

``` markdown
## Linux — Filesystem & shell
Status: Done
```

or:

``` markdown
## Linux — Filesystem & shell
- [x] pwd / ls / cd
- [x] cp / mv / rm
- [x] mkdir / touch
- [x] cat / less / head / tail
- [x] grep / find
- [x] pipes and redirection
- [x] wildcards and quoting
```

3.  Run:

``` bash
python scripts/tracker.py
```

4.  Review the generated files, then commit/push.

GitHub Actions also runs the same generator after pushes to `main` or
`master`.

## Regex note detection

The script intentionally does not treat the existence of a note as
completion. It looks for explicit regex-detected completion signals:

-   `Status: Done`
-   `status: completed`
-   checked topic headings/tasks such as `## [x] Topic`
-   all listed subtopics checked under the matching topic section

If no explicit completion is found, the previous `TRACKER.md` checkbox
is preserved.

## README dashboard

The dashboard is isolated between:

``` markdown
<!-- TRACKER-DASHBOARD:START -->
...
<!-- TRACKER-DASHBOARD:END -->
```

Delete everything between those markers to remove the dashboard. The
detailed roadmap remains in `TRACKER.md`.

The dashboard intentionally has **no week-by-week chart/table**.

## Existing README index automation

Your existing README index markers can remain. The tracker generator
only owns the `TRACKER-DASHBOARD` markers and does not modify the
`INDEX` markers.
