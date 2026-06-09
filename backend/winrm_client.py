import winrm


def get_windows_info(ip, username, password):

    session = winrm.Session(
        f"http://{ip}:5985/wsman",
        auth=(username, password)
    )

    ps_script = """
    $os = Get-CimInstance Win32_OperatingSystem

    $cpu = (Get-Counter '\\Processor(_Total)\\% Processor Time').CounterSamples.CookedValue

    $ram = Get-CimInstance Win32_OperatingSystem

    @{
        Hostname = $env:COMPUTERNAME
        User = $env:USERNAME
        OS = $os.Caption
        RAMPercent = [math]::Round((($ram.TotalVisibleMemorySize - $ram.FreePhysicalMemory) / $ram.TotalVisibleMemorySize) * 100,2)
        TotalRAMGB = [math]::Round($ram.TotalVisibleMemorySize / 1MB,2)
        CPU = [math]::Round($cpu,2)
    } | ConvertTo-Json
    """

    result = session.run_ps(ps_script)

    return result.std_out.decode()