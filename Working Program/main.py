import psutil
import time
from datetime import datetime

# Log file to store the tracked time
log_file = r"D:\GitHub Repo\PythonApplicationTracker\Working Program\app_usage_log.txt"

# Store running times in minutes, days, and start date
app_times = {}

# Track total PC run time
pc_time = {"minutes": 0, "days": 0}  

# List of processes to ignore (common system processes, etc.)
ignored_processes = [
    "explorer.exe",    
    "svchost.exe",     
    "System Idle Process.exe",
    "pet.exe",
    "conhost.exe",
    "RuntimeBroker.exe",
    "SteelSeriesCVGameSense.exe",
    "MoUsoCoreWorker.exe",
    "SystemSettings.exe",
    "LsaIso.exe",
    "RtkAudUService64.exe",
    "WMIRegistrationService.exe",
    "jusched.exe",
    "SteelSeriesSonar.exe",
    "SearchProtocolHost.exe",
    "ShellExperienceHost.exe",
    "gamingservices.exe",
    "cmd.exe",
    "SteelSeriesSvcLauncher.exe",
    "armsvc.exe",
    "ctfmon.exe",
    "dllhost.exe",
    "SearchHost.exe",
    "AppleMobileDeviceService.exe",
    "GCC.exe",
    "LiveCodingConsole.exe",
    "StartMenuExperienceHost.exe",
    "UiPath.RobotJS.UserHost.exe",
    "spoolsv.exe",
    "csrss.exe",
    "taskhostw.exe",
    "audiodg.exe",
    "ApplicationFrameHost.exe",
    "OVRRedir.exe",
    "crashpad_handler.exe",
    "NVIDIA Web Helper.exe",
    "WmiPrvSE.exe",
    "conhost.exe",
    "OVRServiceLauncher.exe",
    "WidgetService.exe",
    "SearchIndexer.exe",
    "dwm.exe",
    "explorer.exe",
    "Widgets.exe",
    "hamachi-2.exe",
    "OfficeClickToRun.exe",
    "sihost.exe",
    "SecurityHealthService.exe",
    "gamingservicesnet.exe",
    "rundll32.exe",
    "TextInputHost.exe",
    "SteelSeriesGG.exe",
    "WindscribeService.exe",
    "services.exe",
    "UiPath.UpdateService.Worker.exe",
    "CrashReportClientEditor.exe",
    "UserOOBEBroker.exe",
    "NisSrv.exe",
    "AggregatorHost.exe",
    "MpDefenderCoreService.exe",
    "msedgewebview2.exe",
    "vgtray.exe",
    "dasHost.exe",
    "powershell.exe",
    "SteelSeriesCaptureSvc.exe",
    "XSpltVidSvc.exe",
    "nvcontainer.exe",
    "winlogon.exe",
    "UiPath.UpdateService.Agent.exe",
    "SteelSeriesEngine.exe",
    "LMIGuardianSvc.exe",
    "SystemSettingsBroker.exe",
    "nvsphelper64.exe",
    "SurSvc.exe",
    "fontdrvhost.exe",
    "zenserver.exe",
    "wininit.exe",
    "lsass.exe",
    "IntelCpHDCPSvc.exe",
    "HPPrintScanDoctorService.exe",
    "NVIDIA Share.exe",
    "MsMpEng.exe",
    "SteelSeriesPrism.exe",
    "OneApp.IGCC.WinService.exe",
    "MedalEncoder.exe",
    "smss.exe",
    "PhoneExperienceHost.exe",
    "esrv_svc.exe",
    "mDNSResponder.exe",
    "esrv.exe",
    "wlanext.exe",
    "UiPath.BrowserBridge.Portable.exe",
    "NVDisplay.Container.exe",
    "RuntimeBroker.exe",
    "AdobeCollabSync.exe",
    "TeamViewer_Service.exe",
    "Medal.exe",
    "jhi_service.exe",
    "smartscreen.exe",
    "GigabyteUpdateService.exe",
    "SecurityHealthSystray.exe",
    "OVRServer_x64.exe",
    "vgc.exe",
    "SearchFilterHost.exe",
    "GameBarPresenceWriter.exe",
    "JetBrains.Etw.Collector.Host.exe",
    "lghub_agent.exe",
    "lghub_system_tray.exe",
    "lghub_updater.exe",
    "logi_lamparray_service.exe",
    "RemoteDesktopCompanion.exe",
    "SecurityHealthHost.exe",
    "ShellHost.exe",
    "unsecapp.exe",
    "wslservice.exe",
    "IntelSoftwareAssetManagerService.exe",
    "DataExchangeHost.exe",
    "TiWorker.exe",
    "TrustedInstaller.exe",
    "ChromeNativeMessaging.exe"
]


def load_previous_data():
    """Load previously logged data from the log file into `app_times` and `pc_time`."""
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip the first line (file creation date)
                line = line.strip()  # Remove trailing whitespace
                if not line or ":" not in line:  # Skip empty lines or invalid lines
                    continue

                if line.startswith("PC RUNS:"):
                    try:
                        # Extract PC RUNS data
                        parts = line.split(", ")
                        pc_time["minutes"] = int(parts[0].split()[2])
                        pc_time["days"] = int(parts[1].split()[0])
                    except (IndexError, ValueError):
                        print(f"Invalid PC RUNS line format: {line}")
                        continue
                else:
                    try:
                        # Extract application data
                        app, rest = line.split(":", 1)
                        parts = rest.strip().split(", ")
                        if len(parts) < 2:
                            print(f"Invalid application line format: {line}")
                            continue
                        minutes = int(parts[0].split()[0])
                        days = int(parts[1].split()[0])
                        app_times[app] = (minutes, days)
                    except (IndexError, ValueError):
                        print(f"Invalid application line format: {line}")
                        continue
    except FileNotFoundError:
        print("Log file not found, initializing with default values.")



def log_usage():
    """Write the current app times and PC RUNS to the log file."""
    try:
        with open(log_file, "r") as f:
            first_line = f.readline().strip()  # Read the first line for the creation date
    except FileNotFoundError:
        # If the file doesn't exist, create the first line with the current date
        first_line = f"File created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    with open(log_file, "w") as f:
        # Write the first line (file creation date)
        #f.write(f"{first_line}\n")

        # Write PC RUNS data
        f.write(f"PC RUNS: {pc_time['minutes']} minutes, {pc_time['days']} days\n")

        f.write("\n")
        f.write("Application Tracker:")
        f.write("\n")

        # Write app usage data
        sorted_apps = sorted(app_times.items(), key=lambda x: x[0].lower())
        for app, data in sorted_apps:
            minutes, days = data
            f.write(f"{app}: {minutes} minutes, {days} days\n")

def update_days():
    """Update days for each application and PC RUNS."""
    # Update days for PC RUNS
    if pc_time["minutes"] >= 1440:  # 1440 minutes in a day
        pc_time["minutes"] %= 1440
        pc_time["days"] += 1

    # Update days for each application
    for app in app_times:
        minutes, days = app_times[app]
        if minutes >= 1440:  # 1440 minutes in a day
            app_times[app] = (minutes % 1440, days + 1)

def main():
    load_previous_data()  # Load data from the log file

    while True:
        # Increment PC RUNS time
        pc_time["minutes"] += 1

        # Get a list of all currently running processes that are not in ignored_processes
        current_apps = {
            proc.info['name'] for proc in psutil.process_iter(['name']) 
            if proc.info['name'] and proc.info['name'].endswith('.exe') and proc.info['name'] not in ignored_processes
        }

        # Increment time for each running application
        for app in current_apps:
            if app not in app_times:
                # First time the application is detected
                app_times[app] = (0, 0)  # Initialize with 0 minutes and 0 days
            else:
                # Only update the minutes and days
                minutes, days = app_times[app]
                app_times[app] = (minutes + 1, days)  # Add 1 minute

        # Update the days counter for PC RUNS and applications
        update_days()

        # Log the usage every minute
        log_usage()

        time.sleep(60)  # Wait for a minute before checking again

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting and saving log...")
        log_usage()  # Save the log before exiting