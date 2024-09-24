import psutil
import time
from datetime import datetime

# Log file to store the tracked time
log_file = "app_usage_log.txt"

# Store running times in minutes, days, and start date
app_times = {}

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
]

# Function to log the times into the file
def log_usage():
    with open(log_file, "w") as f:
        sorted_apps = sorted(app_times.items(), key=lambda x: x[0].lower())
        for app, data in sorted_apps:
            minutes, days, start_date = data
            f.write(f"{app}: {minutes} minutes, {days} days, started on {start_date}\n")

def update_days():
    """Update days for each application."""
    for app in app_times:
        minutes, days, start_date = app_times[app]
        if minutes >= 1440:  # 1440 minutes in a day
            app_times[app] = (minutes % 1440, days + 1, start_date)

def main():
    while True:
        # Get a list of all currently running processes that are not in ignored_processes
        current_apps = {
            proc.info['name'] for proc in psutil.process_iter(['name']) 
            if proc.info['name'] and proc.info['name'].endswith('.exe') and proc.info['name'] not in ignored_processes
        }

        # Increment time for each running application
        for app in current_apps:
            if app not in app_times:
                # First time the application is detected, log the current date/time
                start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                app_times[app] = (0, 0, start_date)  # Initialize with 0 minutes, 0 days, and start date
            else:
                # Only update the minutes and days, keep the start date unchanged
                minutes, days, start_date = app_times[app]
                app_times[app] = (minutes + 1, days, start_date)  # Add 1 minute

        # Update the days counter for applications
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