# Agile Methodology

## Overview

For my project, I am using a Github Project board. I'm utilising Github's milestones to track my progress, as well as their `.yml` issue templates for creating templates for Bugs, User stories and Epics. I have also set up simple workflows that will automatically move issues to the appropriate columns as they are created and closed.

## Project Board

The project board is split into 4 columns:

- Backlog
- To Do
- In Progress
- Done

The backlog column is where I store all of my issues that I have created. I then move them into the To Do column when I am ready to start working on them. Once I have started working on them, I will move them into the In Progress column. Once I have completed the issue, I will move it into the Done column.

## Milestones

I had initially created three phrases for the project, which were:

- Development Phase 1 (One week and a half)
- Development Phase 2 (Two weeks)
- Testing and Development Phase (1 week)

After considering the purpose of the Agile methodology, I decided to break down the project into smaller milestones. I have created 5 milestones, which are:

- Sprint 1 (One week)
- Sprint 2 (One week)
- Sprint 3 (One week)
- Sprint 4 (5 days)
- Testing and Development Phase (5 days)

## Issues

I have created three issue templates, which are:

- Bug
- User Story
- Epic

I created the templates as `.yml` files so that it takes advantage of Github's [issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates) feature. One great advantage of `.yml` templates is that you can automatically add the issue to a project board, which isn't possible with `.md` templates.

## Workflows

I enabled three of the set workflows on the project (two were already enabled):

- [Automatically add project cards to the backlog column](https://github.com/users/stephendawsondev/projects/5/workflows/13073386)

- [Automatically move project cards to the done column when issues are closed](https://github.com/users/stephendawsondev/projects/5/workflows/13068501)

- [Authomatically add any reopened issues to the Todo column](https://github.com/users/stephendawsondev/projects/5/workflows/13073840)
