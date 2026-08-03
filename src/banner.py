from datetime import datetime


def show_banner(server_count, config):
    print("\n" + "=" * 80)
    print("        INFRASTRUCTURE MONITORING & SELF-HEALING PLATFORM")
    print("                          Version 1.0.0")
    print("=" * 80)

    print(f" Started        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Servers        : {server_count}")
    print(f" Execution Mode : Concurrent (ThreadPoolExecutor)")
    print(f" Python         : 3.12+")
    print(f" SSH            : Paramiko")
    print(f" Dashboard      : Enabled")
    print(f" Reports        : Enabled")
    print(f" Alerts         : Enabled")
    print(f" Self-Healing   : Enabled")
    print(f" Scheduler      : Ready")

    print("-" * 80)

    print(" Threshold Configuration")
    print(f"   CPU Threshold      : {config['cpu_threshold']}%")
    print(f"   Memory Threshold   : {config['memory_threshold']}%")
    print(f"   Disk Threshold     : {config['disk_threshold']}%")
    print(f"   Check Interval     : {config['check_interval']} seconds")

    print("=" * 80)