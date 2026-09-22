#!/usr/bin/env python3
"""GPU sanity check and CPU-vs-GPU timing with PyTorch.

Multiplies two n x n float32 matrices on the CPU and (if one is visible) on the GPU,
and prints the timings. Used in GPU Exercise 2.

Usage:  python gpu_check.py [--n 4096] [--repeats 5]
"""
import argparse
import os
import sys
import time


def best_time(fn, repeats, sync=None):
    """Run fn() `repeats` times and return the fastest time in seconds."""
    times = []
    for _ in range(repeats):
        if sync:
            sync()
        start = time.perf_counter()
        fn()
        if sync:
            sync()
        times.append(time.perf_counter() - start)
    return min(times)


def main():
    parser = argparse.ArgumentParser(description="PyTorch GPU check and CPU vs GPU matrix multiply")
    parser.add_argument("--n", type=int, default=4096, help="matrix size (n x n), default 4096")
    parser.add_argument("--repeats", type=int, default=5, help="timing repeats, default 5")
    args = parser.parse_args()

    try:
        import torch
    except ImportError:
        sys.exit("PyTorch is not installed in this environment. Activate the environment you "
                 "built in the CPU interactive session (see GPU Exercise 2).")

    print(f"Host                 : {os.uname().nodename if hasattr(os, 'uname') else 'unknown'}")
    print(f"SLURM job id         : {os.environ.get('SLURM_JOB_ID', 'not in a Slurm job')}")
    print(f"CUDA_VISIBLE_DEVICES : {os.environ.get('CUDA_VISIBLE_DEVICES', 'not set')}")
    print(f"PyTorch version      : {torch.__version__}")
    print(f"Built for CUDA       : {torch.version.cuda}")
    print(f"CUDA available       : {torch.cuda.is_available()}")

    n = args.n
    flops = 2 * n ** 3  # multiply-adds in an n x n matrix multiply

    a = torch.randn(n, n)
    b = torch.randn(n, n)
    cpu_time = best_time(lambda: torch.matmul(a, b), args.repeats)
    print(f"\nCPU  {n} x {n} matmul : {cpu_time:.4f} s  ({flops / cpu_time / 1e9:.1f} GFLOP/s)")

    if not torch.cuda.is_available():
        print("\nNo GPU is visible to PyTorch. Check that:")
        print("  - this is a batch job that requested a GPU (--gres=gpu:1 or the syntax for this cluster)")
        print("  - your environment has a CUDA build of PyTorch (torch.version.cuda is not None)")
        sys.exit(1)

    device = torch.device("cuda")
    props = torch.cuda.get_device_properties(device)
    print(f"GPU                  : {props.name}, {props.total_memory / 2**30:.1f} GiB, "
          f"compute capability {props.major}.{props.minor}")

    # Does this PyTorch build contain code for this GPU's architecture? Newer GPUs need newer builds.
    arch_list = torch.cuda.get_arch_list()
    gpu_arch = f"sm_{props.major}{props.minor}"
    print(f"Build supports       : {' '.join(arch_list)}")
    if gpu_arch not in arch_list:
        print(f"\nWARNING: this PyTorch build has no {gpu_arch} code for this GPU. It may fail with 'no kernel "
              f"image is available', or run slowly.\n         Install a build made with a newer CUDA (see GPU Exercise 2).\n")

    a_gpu = a.to(device)
    b_gpu = b.to(device)
    torch.matmul(a_gpu, b_gpu)          # warm-up: the first call pays start-up costs
    torch.cuda.synchronize()
    gpu_time = best_time(lambda: torch.matmul(a_gpu, b_gpu), args.repeats, sync=torch.cuda.synchronize)
    print(f"GPU  {n} x {n} matmul : {gpu_time:.4f} s  ({flops / gpu_time / 1e9:.1f} GFLOP/s)")
    print(f"\nSpeed-up (CPU time / GPU time): {cpu_time / gpu_time:.1f}x")


if __name__ == "__main__":
    main()
