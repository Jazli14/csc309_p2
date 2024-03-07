## CSC309 Views and URLs

1. **User Authentication Views:**
   - Login View: `/login/`
   - Registration View: `/register/`
   - Profile View: `/profile/`

2. **Contacts Views:**
   - [GET]Contacts List View: `/contacts/`
   - [POST]Add Contact View: `/contacts/`
   - [DELETE]Delete Contact View: `/contacts/<contact_id>/`

3. **Calendar Views:** [Calender CRUD Implementation](https://github.com/Jazli14/csc309_p2/issues/1#issue-2172656711)
   - [GET]Calendar Detail View: `/calendar/<calendar_id>/`
   - [POST]Calendar Creation View: `/calendar/`
   - [PUT]Edit Calendar View: `/calendar/<calendar_id>/`
   - [DELETE]Delete Calendar View: `/calendar/<calendar_id>/`

5. **Time Block Views:**
   - [GET]Time Blocks List View: `/calendar/<calendar_id>/timeblocks/`
   - [POST]Add Time Block View: `/calendar/<calendar_id>/timeblocks/`
   - [PUT]Edit Time Block View: `/timeblocks/<timeblock_id>/`
   - [DELETE]Delete Time Block View: `/timeblocks/<timeblock_id>/`

6. **Invitation Views:**
   - [time-permitting] [GET]Invitation Email View: `/meeting/<meeting_id>/invitation/`
   - [time-permitting] [POST]Respond to Invitation View: `/meeting/<meeting_id>/response/`

7. **Scheduling Views:**
   - [time-permitting] [GET]Suggested Schedules View: `/meeting/<meeting_id>/suggestion/`
   - [time-permitting] [POST]Select Schedule View: `/meeting/<meeting_id>/suggestion/`

8. **Reminder Views:**
   - [time-permitting] Reminder View: `/reminder/` 

