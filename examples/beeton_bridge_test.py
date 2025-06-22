import serial
import threading
import sys
import re
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Serial console with filtering")
    parser.add_argument("--port", default="/dev/ttyACM2", help="Serial port")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--modules", nargs="+", default=["Beeton", "LightThread"], help="Modules to show")
    parser.add_argument("--levels", nargs="+", default=["DEBUG", "INFO", "WARN","ERROR"], help="Levels to show (case-insensitive)")
    return parser.parse_args()

def extract_tags(line):
    # Match full ESP32 log format + [Module]
    # Example: [12345][I][File.cpp:42] func(): [LightThread] message...

    module_match = re.search(r'\[(\w+)\]\s', line)
    level_match = re.search(r'\[(V|D|I|W|E)\]', line)
    
    
    if module_match:
        module = module_match.group(1)
    else:
        module = "UNKNOWN"
    level_code = level_match.group(1) if level_match else "I"
    level_map = {
        "D": "DEBUG",
        "I": "INFO",
        "W": "WARN",
        "E": "ERROR"
    }
    level = level_map.get(level_code, "INFO")

    return module, level


def read_from_serial(ser, allowed_modules, allowed_levels):
    try:
        while True:
            raw_line = ser.readline().decode(errors='ignore').strip()
            if not raw_line:
                continue

            module, level = extract_tags(raw_line)
            if module == "USB" or module in allowed_modules and level.upper() in allowed_levels:
                print(f">>> {raw_line}")
    except Exception as e:
        print(f"[ERROR] {e}")

def write_to_serial(ser):
    try:
        while True:
            cmd = input()
            if cmd:
                ser.write((cmd + '\n').encode())
    except Exception as e:
        print(f"[ERROR] {e}")

def main():
    args = parse_args()

    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
        print(f"Connected to {args.port} @ {args.baud} baud")
        print(f"Filtering modules: {args.modules}, levels: {args.levels}")
        reader = threading.Thread(target=read_from_serial, args=(ser, args.modules, [lvl.upper() for lvl in args.levels]), daemon=True)
        writer = threading.Thread(target=write_to_serial, args=(ser,), daemon=True)

        reader.start()
        writer.start()

        reader.join()
        writer.join()
    except serial.SerialException as e:
        print(f"Could not open port: {e}")
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()

