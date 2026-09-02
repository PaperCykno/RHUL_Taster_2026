# CTFd setup

Just what needs putting on CTFd for each challenge.

For the website ones I'll send the hosted link once they're up.  
Don't upload any source code, only the player files listed here.

---

## 01 - After the Migration

75 pts - Web

**description**

An old RHUL CSS event portal is still online after a migration.

Most of it looks empty now but some of the old portal was kept for compatibility.

Find the migration reference from the old portal.

Flag format: `rhul{migration_REFERENCE}`

link: `<CHALLENGE_URL>`

**flag**

`rhul{migration_LM-4821}`

**hints if people get stuck**

1. Check if there are any paths that aren't linked on the main page
2. The archived site still loads some files in the background
3. Check the javascript used by the archive page

---

## 02 - The Silent Keyboard

250 pts - Forensics

upload: `capture.pcap`

**description**

We recovered this capture from one of the machines used during setup.

There isn't really any useful network traffic in it, but somebody was using the machine at the time.

Work out what they typed and recover the flag.

**flag**

`rhul{keys_never_forget_7319}`

**hints**

1. A pcap doesn't have to contain normal network traffic
2. Look at the USB traffic
3. The packets are keyboard HID reports. Shift and backspace matter

---

## 03 - Clock Drift

175 pts - Forensics

upload: `clock-drift-evidence.zip`

**description**

We have logs from several systems during the same incident, but none of their clocks were properly synced.

We know the FIRE_TEST happened at exactly `21:30:00`.

Use that to fix the timestamps and work out who accessed the archive.

**flag**

`rhul{0471_committee-admin_220107}`

**hints**

1. Find FIRE_TEST in each log
2. Work out how far each clock is ahead/behind
3. Once the clocks are fixed, look around the archive access

---

## 04 - Ghost Team

400 pts - SQL / Investigation

link: `<CHALLENGE_URL>`

**description**

A team appeared on the event system without going through normal registration.

What we know:

- they're still active
- they have no normal registration
- they have at least 3 correct submissions
- every correct submission came from the same device
- the invite used to make the team was already more than 7 days old

The audit logs from when the team was created are still in the database.

Find the team and follow what happened until you can build the unlock code.

**flag**

`rhul{ghosts_leave_audit_trails}`

**hints**

1. Start by looking at what tables are available
2. Find active teams that don't have a registration
3. Compare correct submissions and devices used
4. Once you've got the team, look at its audit events and creation session

---

## 05 - Inbox 17

50 pts - Email Analysis

link: `<CHALLENGE_URL>`

**description**

4 emails were pulled from a student's inbox.

One of them should be treated as suspicious.

Find the email and submit its mail trace number.

Flag format: `rhul{mx_TRACE}`

**flag**

`rhul{mx_7319}`

**hints**

1. Don't just look at the sender name
2. Check the Reply-To and where links actually go
3. There are technical details for each email

---

## 06 - Old USB

50 pts - Forensics

upload: `minutes_2024.txt`

**description**

We found an old committee USB during a clear-out.

One of the recovered files is called `minutes_2024.txt`, but opening it normally isn't very useful.

Find the archive reference inside it.

Flag format: `rhul{archive_REFERENCE}`

**flag**

`rhul{archive_EX-204}`

**hints**

1. Is it actually a normal txt file?
2. File extensions can be misleading
3. Check what type of file it actually is

---

## 07 - Dead Air

100 pts - Forensics

upload: `recording_17.wav`

**description**

This audio file was recovered during setup for the freshers event.

Listening to it doesn't really give you anything useful.

See what else you can find in it.

Flag format: `rhul{signal_CODE}`

**flag**

`rhul{signal_7319}`

**hints**

1. You don't have to listen to audio to analyse it
2. Try viewing the frequencies over time
3. Any free online spectrogram viewer should work

---

## 08 - Legacy Project

175 pts - Git / Forensics

upload: `event-tools.zip`

**description**

This is an old RHUL CSS project recovered from a backup.

The current files don't contain the service token that used to be there.

We know the token was:

`KEY PART + SERVICE SUFFIX`

Find both parts and put them back together.

Flag format: `rhul{legacy_TOKEN}`

**flag**

`rhul{legacy_7c91}`

**hints**

1. The current files aren't necessarily everything that has existed in the project
2. Check the Git history
3. `git log --all --oneline --graph`
4. If they're still stuck, tell them to look at `release-compat`

---

## files to upload

01 After the Migration - hosted link  
02 Silent Keyboard - `capture.pcap`  
03 Clock Drift - `clock-drift-evidence.zip`  
04 Ghost Team - hosted link  
05 Inbox 17 - hosted link  
06 Old USB - `minutes_2024.txt`  
07 Dead Air - `recording_17.wav`  
08 Legacy Project - `event-tools.zip`

For Ghost Team also don't upload the database/app files.

For the website challenges just put the link on CTFd, don't give out the website source.
