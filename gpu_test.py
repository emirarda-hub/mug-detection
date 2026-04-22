import torch
import sys
import subprocess

print("Python version:", sys.version.split()[0])
print("Torch version:", torch.__version__)

print("\n=== CUDA Check ===")
print("cuda.is_available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("CUDA device:", torch.cuda.get_device_name(0))

print("\n=== MPS (Apple GPU) Check ===")
print("mps.is_available:", torch.backends.mps.is_available())
print("mps.is_built:", torch.backends.mps.is_built())

if torch.backends.mps.is_available():
    print("Device: Apple GPU (MPS backend)")

print("\n=== System GPU Info ===")
subprocess.run(["system_profiler", "SPDisplaysDataType"])

