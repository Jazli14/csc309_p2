## CSC309 Views and URLs

1. **User Authentication Views:**
   - [POST] Register User: `/accounts/users/`
   - [POST] Login User: `/accounts/users/<user_id>/`
   - [DELETE] Delete User: `/accounts/users/<user_id>/`
   - [PATCH] Edit User: `/accounts/users/<user_id>/`
   - [GET] Retrieve User ID: `/accounts/users/<user_id>/`

2. **Contacts Views:**
   - [GET] Contacts List View: `/accounts/<user_id>/contacts/`
   - [POST] Add Contact View: `/accounts/<user_id>/contacts/`
   - [DELETE] Delete Contact View: `/accounts/<user_id>/contacts/<contact_id>/`

3. **Calendar Views:** [Calender CRUD Implementation](https://github.com/Jazli14/csc309_p2/issues/1#issue-2172656711)
   - [GET] Calendar Detail View: `api/calendar/<calendar_id>/`
   - [GET] Retrieve All Calendars: `api/calendar/`
   - [POST] Calendar Creation View: `api/calendar/`
   - [PUT] Edit Calendar View: `api/calendar/<calendar_id>/`
   - [DELETE] Delete Calendar View: `api/calendar/<calendar_id>/`
   - [PATCH] adding student View: `api/calendar/<calendar_id>/add_student`

5. **Time Block Views:** [Timeblock CRUD Implementation](https://github.com/Jazli14/csc309_p2/issues/4)
   - [GET] Time Blocks List View: `api/calendar/<calendar_id>/timeblocks/`
   - [POST] Add Time Block View: `api/calendar/<calendar_id>/timeblocks/`
   - [PUT] Edit Time Block View: `api/timeblocks/<timeblock_id>/`
   - [DELETE] Delete Time Block View: `api/timeblocks/<timeblock_id>/`

6. **Invitation Views:**
   - [time-permitting] [GET] Invitation Email View: `/meeting/<meeting_id>/invitation/`
   - [time-permitting] [POST] Respond to Invitation View: `/meeting/<meeting_id>/response/`

7. **Scheduling Views:**
   - [time-permitting] [GET] Suggested Schedules View: `/meeting/<meeting_id>/suggestion/`
   - [time-permitting] [POST] Select Schedule View: `/meeting/<meeting_id>/suggestion/`

8. **Reminder Views:**
   - [time-permitting] Reminder View: `/reminder/` 

