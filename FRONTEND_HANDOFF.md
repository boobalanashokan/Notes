# Frontend Handoff Guide

## Project overview
This is a React-based study tracker app. It helps a learner manage a curriculum track, track progress, review roadmap topics, create new tracks, and upload notes that get mapped to a relevant topic.

The frontend is built around a selected learning track. The app loads data from the backend, displays it in a set of pages, and lets the user manage study progress.

---

## Main frontend files

### `frontend/src/App.jsx`
This is the main app shell and router.

Functions:
- Wraps the app in `TrackProvider`
- Sets up `BrowserRouter`
- Shows the top navigation bar
- Handles route definitions for:
  - `/` → Dashboard
  - `/notes` → Notes
  - `/roadmap` → Roadmap
  - `/projects` → Projects
  - `/skills` → Skills
  - `/add-track` → Add Track
  - `/upload` → Upload Notes

It also includes the track selector at the top so the user can switch between different study tracks.

### `frontend/src/TrackContext.jsx`
This file contains the shared app state for the selected track.

It manages:
- `tracks`: list of available tracks
- `trackId`: currently selected track
- `trackName`: name of the active track
- `loading`: whether the data is still loading
- `error`: any fetch error state

It loads the tracks on startup by calling `getTracks()`, saves the selected track to `localStorage`, and keeps the UI synced.

### `frontend/src/api.js`
This is the API utility layer for the frontend.

It wraps backend requests and handles:
- response parsing
- JSON decoding
- error messages
- file upload handling

Main functions:
- `getTracks()`
- `getTrackStats(trackId)`
- `getTrack(trackId)`
- `uploadFiles(trackId, files)`
- `getMappingOptions(trackId, areaId, topicId)`
- `previewMapping(trackId, areaId, topicId, payload)`
- `approveMapping(trackId, areaId, topicId, payload)`

This keeps all API logic in one place instead of spreading it across pages.

### `frontend/src/App.css`
This file contains the app’s styling.

It defines:
- top nav appearance
- card styles
- progress bars
- filter panels
- topic/area layout
- upload area styles
- buttons and success/error states
- responsive mobile behavior

The app uses a clean dashboard-style visual system with white cards on a soft gray background.

---

## Frontend pages and what each one does

### Dashboard
File: `frontend/src/pages/Dashboard.jsx`

Purpose:
- Shows completion status for the selected track
- Displays overall progress as a percentage
- Shows topic totals and completed counts
- Shows per-area progress bars

Behavior:
- Reads `trackId` and `trackName` from `useTrack()`
- Calls `getTrackStats(trackId)`
- Renders progress for the whole track and each area

This is the home screen and the main summary page.

### Roadmap
File: `frontend/src/pages/Roadmap.jsx`

Purpose:
- Displays all track areas and topics in an expandable structure
- Lets the user filter by area and by done/not done status

Behavior:
- Calls `getTrack(trackId)`
- Builds filter options from the track data
- Lets user expand or collapse an area
- Shows:
  - topic name
  - status badge
  - week number
  - subtopics
  - learning outcome
  - project task

This is the most content-heavy page for learning structure.

### Projects
File: `frontend/src/pages/Projects.jsx`

Purpose:
- Extracts all topics with a `project_task`
- Displays them as project cards
- Lets the user filter project cards by status

Behavior:
- Reads the full selected track
- Flattens topics from all areas
- Keeps only topics that have a project task
- Filters by All / Done / Not Done

This page turns roadmap content into practical project tasks.

### Skills
File: `frontend/src/pages/Skills.jsx`

Purpose:
- Shows skill mastery progress by area
- Sorts areas by completion percentage

Behavior:
- Calls `getTrackStats(trackId)`
- Sorts the area stats by percent complete
- Displays completed counts for each area

This page is a more summarized skill/progress view.

### Notes
File: `frontend/src/pages/Notes.jsx`

Purpose:
- Shows topic details in a browsable structure
- Lets the user expand a topic to view more information

Behavior:
- Loads the selected track
- Maps each area and topic
- Shows metadata like week, subtopics, outcomes, and task info
- Includes a placeholder note that says full content viewing is coming soon

This page is used for topic browsing and note-oriented reading.

### Add Track
File: `frontend/src/pages/AddTrack.jsx`

Purpose:
- Lets the user create a new study track from a JSON curriculum

Behavior:
- User pastes a single JSON object
- App validates the JSON format
- Shows the number of areas and topics
- Sends the data to the backend via `POST /tracks`
- Reports success or failure with commit/save details

This is the curriculum creation flow.

### Upload Notes
File: `frontend/src/pages/UploadNotes.jsx`

Purpose:
- Lets the user upload notes/files
- Maps uploaded files to curriculum topics
- Previews and approves the generated note content

Main features:
- drag-and-drop upload
- multiple file upload
- file type validation
- area/topic selection
- status selection
- valid subtopic selection
- note text input
- preview of generated note section
- append/overwrite choice if a file already exists
- approval and save

This is the most advanced workflow in the app and likely the most important feature from a product perspective.

---

## Upload flow in detail
The upload page is a multi-step workflow.

1. User picks one or more files.
2. App validates file extensions (`.pdf`, `.png`, `.jpg`, `.jpeg`).
3. User uploads files to the backend using `uploadFiles()`.
4. The backend returns saved local file paths.
5. Each uploaded file becomes an entry in the UI.
6. For each file entry, the user chooses:
   - area
   - topic
   - completion status
   - relevant subtopics
   - note text
7. The user clicks Preview.
8. The app calls `previewMapping()`.
9. The backend returns a preview of the new content and whether the target file already exists.
10. The user may choose Append or Overwrite.
11. The user clicks Approve.
12. The frontend calls `approveMapping()` and saves the result.

This is a controlled, review-before-save workflow for adding notes into the track curriculum.

---

## Design / usability notes
The current UI is clean and practical, with the following characteristics:

- dark header/navigation
- soft neutral background
- white content cards
- rounded corners and subtle shadows
- blue progress bars to indicate completion
- simple filter panels and forms
- status badges for done/not done

Overall style:
- functional
- lightweight
- dashboard-driven
- easy to build on

This is a good base for a better product-style redesign, but it is not yet a more premium or polished user experience.

---

## Current strengths
- Clear app structure
- Good separation of concerns
- Shared state is centralized
- Each page is focused on a specific purpose
- API logic is centralized in one module
- Good foundation for future redesign or enhancement

---

## Areas that may need improvement
- visual polish and modern product styling
- more consistent spacing system
- stronger typography hierarchy
- better dashboard storytelling
- nicer empty/loading states
- more refined mobile experience
- more premium button and card treatments

---

## Summary
This frontend is a study-tracking dashboard that allows users to:
- switch tracks
- see progress by topic and area
- browse roadmap material
- see project tasks
- create new curriculum tracks
- upload notes and map them to the correct topic
- preview and approve content before saving

It is a functional and structured application with a strong base for future UI improvements.

---

## Hand-off note for a designer or developer
If someone else is taking over, the easiest way to understand this project is:

- the app starts from `App.jsx`
- state lives in `TrackContext.jsx`
- API requests live in `api.js`
- each page is independent and responsible for one workflow
- styling is centralized in `App.css`

A redesign or visual refresh should focus on the CSS and layout system rather than the page logic, because the business logic is already fairly well organized.
