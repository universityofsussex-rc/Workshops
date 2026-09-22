---
title: GPU Exercises
permalink: /GPU/
nav_order: 12
parent: "Exercises"
has_children: true
---
<div id="top"></div>

<div align="center">
  <a href="https://universityofsussex-rc.github.io/Workshops/">
    <img src="https://universityofsussex-rc.github.io/Workshops/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Using GPUs on Artemis</h3>
  <p align="center">
    An overview of GPUs, CUDA and the Slurm scheduler on Artemis, followed by four hands-on exercises.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Contents</summary>
  <ol>
    <li><a href="#what-you-will-learn">What you will learn</a></li>
    <li><a href="#before-you-start">Before you start</a></li>
    <li><a href="#workshop-settings">Workshop settings</a></li>
    <li><a href="#what-is-a-gpu-and-when-does-it-help">What is a GPU, and when does it help?</a></li>
    <li><a href="#how-gpu-jobs-run-in-this-workshop">How GPU jobs run in this workshop</a></li>
    <li><a href="#cuda-in-five-minutes">CUDA in five minutes</a></li>
    <li><a href="#requesting-a-gpu-with-slurm">Requesting a GPU with Slurm</a></li>
    <li><a href="#reading-nvidia-smi">Reading nvidia-smi</a></li>
    <li><a href="#good-habits">Good habits</a></li>
    <li><a href="#when-things-go-wrong">When things go wrong</a></li>
    <li><a href="#the-exercises">The exercises</a></li>
    <li><a href="#learn-from-other-centres">Learn from other centres</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

## What you will learn

By the end of this workshop you will be able to:

- explain what a GPU is good at, and decide whether your own code can use one
- request a GPU on Artemis with Slurm and check what you were given
- find and load CUDA modules without breaking your environment
- run Python (PyTorch) and compiled CUDA code on a GPU
- run **your own** GPU code as a well-behaved batch job

The examples use Python and a small CUDA C program, but each exercise finishes with a "your own code" step, so you can work on whatever you bring.

## Before you start

You should have completed the Artemis basics:

- an HPC account and VPN access ([Artemis Exercises 1]({{ site.baseurl }}{% link exercises/artemis/Exercise1/README.md %}))
- you can start an interactive session and submit a simple batch job ([Artemis Exercises 2]({{ site.baseurl }}{% link exercises/artemis/Exercise2/README.md %}) or [Basic Exercises 2 and 3]({{ site.baseurl }}{% link exercises/basic/Exercise2/README.md %}))
- you know the basics of `module load` and `module purge`

<p align="right">(<a href="#top">back to top</a>)</p>

## Workshop settings

The exercises use a few settings that depend on the session you are attending. Your instructor will tell you the values; the table shows where each one is used.

| Setting | Written in the exercises as | Value for this session |
| --- | --- | --- |
| CPU partition for interactive sessions | `<CPU_PARTITION>` | **Brighton sessions: `brighton`**. Sussex sessions: `workshops` |
| GPU partition for batch jobs | `<GPU_PARTITION>` | **Brighton sessions: `brighton`** (the same partition, with a GPU requested). Sussex sessions: `workshops` |
| GPU flavour | `<GPU_FLAVOR>` | **Brighton sessions: `RTX`**. Other flavours on Artemis: `A40` |
| CUDA module | `<CUDA_MODULE>` | Probably `CUDA/12.9.1`. The RTX GPUs need a recent CUDA, see below |
| Shared Python environment (optional) | `<ENV_PATH>` | `/mnt/shared/admin/workshops/envs/rtx-brighton` |
| GPUs available to the room | n/a | Brighton sessions: 6 (3 RTX nodes with 2 GPUs each). Sussex Sessions: 28 |

> **Brighton participants:** the other exercise pages on this site say `workshops`. Wherever you see it, type `brighton` instead. Brighton accounts can only submit to the `brighton` partition, which is made up of 3 of the RTX GPU nodes.

<p align="right">(<a href="#top">back to top</a>)</p>

## What is a GPU, and when does it help?

A **CPU** has a small number of powerful cores that are good at varied, step-by-step work. A **GPU** (graphics processing unit) has thousands of simpler cores that are good at doing the *same* operation on a lot of data at once. For scale, a single NVIDIA A100 has 6,912 CUDA cores.

GPUs help when your work is dominated by:

- machine learning and deep learning (training and inference)
- large matrix and linear algebra operations
- image and signal processing
- some simulations (molecular dynamics, fluid dynamics, N-body)

A GPU does **not** make ordinary code faster. It only helps if your program was written or built to use it, either directly in CUDA or through a library such as PyTorch, TensorFlow, CuPy or a GPU-enabled application. Small problems can even run slower on a GPU, because moving data to and from the GPU has a cost.

> **Quick test:** does your software's documentation mention CUDA, GPU or NVIDIA? If not, it will not use a GPU however many you request.

## GPUs on Artemis

Artemis has 15 GPU nodes as well as CPU-only nodes, all controlled by Slurm. Each GPU node has 2 GPUs.

| GPU flavour | Nodes | GPUs per node | RAM per node | Compute capability |
| --- | --- | --- | --- | --- |
| `A40` (48 GB per GPU) | 4 | 2 | 512 GB | 8.6 (`sm_86`) |
| `A40` (48 GB per GPU) | 7 | 2 | 1 TB | 8.6 (`sm_86`) |
| `RTX` (96 GB per GPU) | 4 (3 in the `brighton` partition) | 2 | 768 GB | 12.0 (`sm_120`) |
| CPU only | 2 | none | 768 GB | n/a |

- **The RTX GPUs are a newer architecture than the A40.** Run `nvidia-smi --query-gpu=name,compute_cap --format=csv` in Exercise 1 to see exactly what you were given. If they are Blackwell-generation GPUs they have compute capability 12.0 (`sm_120`), which needs **CUDA 12.8 or newer** and a framework build that includes `sm_120`.
- **The Brighton partition** has 3 of the RTX nodes, so 6 GPUs in total. Interactive sessions on `brighton` run on one of these nodes too, but you only get a GPU if you ask for one.


<p align="right">(<a href="#top">back to top</a>)</p>

## How GPU jobs run in this workshop

Only **6 GPUs** are available to the whole room, so GPU work in this workshop is **batch only**. You can still use an interactive session, but it is a normal CPU session.

```text
 1. Interactive session (CPU)       srun -p <CPU_PARTITION> --pty bash
    Load modules, build your environment, edit and test a small case on the CPU.
                 |
 2. Write the job script            #SBATCH --gres=gpu:<flavour>:1  and a short --time
                 |
 3. Submit                          sbatch my_gpu_job.job     then     squeue --me
                 |
 4. Read the results                the .out file, nvidia-smi details, a usage log
                 |
                 +----> adjust and repeat from step 1 or 2
```

**Why this way round?**

- An interactive GPU session holds a GPU while you think and type. With 6 GPUs for the room, that would leave most people waiting.
- Downloads and installs (`pip`, `conda`, `git clone`) belong in step 1, where `module load proxy/public` gives you internet access. Do not rely on the internet from a GPU job. (The ARCHER2 GPU nodes, for example, have none.)

**Sharing the GPUs fairly:**

| Do | Avoid |
| --- | --- |
| Request **1 GPU** per job | Requesting more GPUs than your code uses |
| Set a short `--time` (minutes, not hours) | Leaving the default or a very long time limit |
| `scancel <jobid>` jobs you no longer need | Leaving a queued job you have stopped caring about |
| Test on the CPU first | Debugging typos with a GPU job |

<p align="right">(<a href="#top">back to top</a>)</p>

## CUDA in five minutes

**CUDA** is NVIDIA's platform for programming GPUs. Three pieces matter when you use it on a cluster:

| Piece | What it is | Where you meet it |
| --- | --- | --- |
| **Driver** | Installed on the GPU node by the administrators. Controls the hardware. | `nvidia-smi` |
| **CUDA toolkit** | Compiler (`nvcc`), libraries and headers used to *build* GPU software. | `module load <CUDA_MODULE>` |
| **GPU libraries** | cuDNN, cuBLAS and framework builds such as PyTorch's CUDA wheels. | `pip`/`conda` environments, or other modules |

Things to know:

- **The CUDA version shown by `nvidia-smi` is the newest CUDA the *driver* supports**, not necessarily what is loaded in your session. Your toolkit or framework must be no newer than that.
- **Module names tell you the CUDA version.** Artemis software is installed with EasyBuild, and names follow `software/version-toolchain-suffix`. For example `NCCL/2.27.7-GCCcore-14.3.0-CUDA-12.9.1` is NCCL (the multi-GPU communication library) 2.27.7, built with the `GCCcore-14.3.0` compiler toolchain and CUDA 12.9.1. Do not mix toolchains in one environment.
- **Start clean.** Run `module purge` and then load one consistent set of modules. Cambridge CSD3 advises the same on its GPU nodes.
- **Every GPU has a "compute capability"** that identifies its architecture: 8.6 for the A40 (`sm_86`), and higher for newer GPUs. When compiling your own CUDA code you target it with `nvcc -arch=sm_86` (remove the dot). You will look yours up in Exercise 1.
- **Newer GPUs need newer CUDA.** Software built with an older CUDA (for example CUDA 12.1) may not contain code for a newer GPU such as the RTX nodes. The CUDA 12.9.1 modules on Artemis are new enough. If it does not, you will see `no kernel image is available for execution on the device`. Use a CUDA module and framework build that supports your GPU's architecture.
- **Software built for one machine may not run on another.** CSD3 recommends rebuilding software on the type of node it will run on, rather than reusing binaries built elsewhere.

<p align="right">(<a href="#top">back to top</a>)</p>

## Requesting a GPU with Slurm

A GPU is a *generic resource* (`gres`) that you ask Slurm for in your job script. A complete job script looks like this (Brighton values shown):

```bash
#!/bin/bash
#SBATCH --job-name=gpu_test
#SBATCH --partition=brighton
#SBATCH --gres=gpu:RTX:1
#SBATCH --time=00:05:00
#SBATCH --output=gpu_test-%j.out

module purge
module load <CUDA_MODULE>

nvidia-smi
```

The syntax is `--gres=gpu:<flavour>:<number>`:

| Request | You get |
| --- | --- |
| `--gres=gpu:1` | Any one GPU |
| `--gres=gpu:A40:1` | One A40 |
| `--gres=gpu:RTX:2` | Two RTX GPUs |
| `--nodes=2 --gres=gpu:2` | 4 GPUs. **The number is per node**, so 2 GPUs on each of 2 nodes |

**Which should you use?**

- **Name the flavour** (`gpu:RTX:1`, `gpu:A40:1`) if your job depends on the CUDA version or GPU architecture: compiled CUDA code, a specific CUDA toolkit, or a framework build. The A40 and RTX are different generations, and code built for one may not run on the other.
- **`gpu:1` is fine** if your code only needs "a GPU" and does not care which, for example a program that just uses the GPU to render or run a standard library.

Other things to know:

- **If you do not ask for a GPU, you do not get one.**
- Slurm sets `CUDA_VISIBLE_DEVICES` so your program only sees the GPU(s) you were given.
- On the `brighton` partition every GPU is an RTX, so `gpu:1` and `gpu:RTX:1` give the same result today. Naming the flavour is still good practice, because it keeps working if the partition changes.
- In this workshop, ask for **one** GPU per job. `gpu:RTX:2` takes both GPUs on a node, a third of the room's GPUs.

> **Other centres write this differently.** Cambridge CSD3 uses `--gres=gpu:N` in its `ampere` partition (and rejects GPU jobs that do not specify it). ARCHER2 uses `--gpus=N` and does not let you specify `--ntasks` or `--cpus-per-task` for GPU jobs. Always check the documentation for the system you are on.

<p align="right">(<a href="#top">back to top</a>)</p>

## Reading nvidia-smi

`nvidia-smi` shows the state of the GPU(s) your job can see. The parts to look for:

| Field | Meaning |
| --- | --- |
| **Driver Version / CUDA Version** (header) | The installed driver, and the newest CUDA it supports |
| **Name** | The GPU model |
| **Memory-Usage** | Memory in use / total. If your job runs out of GPU memory, it fails |
| **GPU-Util** | How busy the GPU was over the last moment. Low numbers mean the GPU is idle much of the time |
| **Processes** | Programs using the GPU |

Handy variations:

```bash
nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv          # model, memory, compute capability
nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used --format=csv -l 2   # a reading every 2 seconds
```

The second command is how you build a usage log inside a job script (you will do this in Exercise 2).

<p align="right">(<a href="#top">back to top</a>)</p>

## Good habits

1. **Test small first.** Get a tiny run working on the CPU before you spend a GPU on it.
2. **Set a realistic `--time`.** Shorter jobs often start sooner because Slurm can fit them into gaps in the schedule (backfilling), and a job that hits its limit is killed.
3. **One GPU is usually enough** until your code is proven to use more.
4. **Check the GPU was actually busy.** A GPU sitting at a few percent utilisation is a sign the code is CPU-bound or the input is too small.
5. **Use job arrays** for many similar runs (parameter sweeps, several seeds), with a limit such as `--array=1-8%2`, instead of submitting jobs in a loop.
6. **Do not poll the scheduler.** Checking `squeue --me` roughly once a minute is plenty.
7. **Look after your storage.** Conda environments are large. Build big ones on Lustre (`conda create -p <path>`), and remove finished ones with `conda env remove` and `conda clean --all`.
8. **Save your work.** Copy anything you want to keep into your own storage; local storage is deleted after the job.

<p align="right">(<a href="#top">back to top</a>)</p>

## When things go wrong

| What you see | Likely cause and fix |
| --- | --- |
| Job stays `PENDING` (`Priority` or `Resources`) | Other jobs are ahead of you, or all 6 GPUs are busy. Wait, or make `--time` shorter and more realistic. `squeue --me --start` gives an estimate |
| `Invalid account or account/partition combination` | Wrong partition. Brighton users must use `brighton` for CPU work; check the GPU partition with your instructor |
| `CUDA available: False` in Python | The job did not request a GPU (`--gres`), or your environment has a CPU-only build of PyTorch |
| `no kernel image is available for execution on the device` | Your software was built for a different GPU architecture. Use a newer CUDA module or framework build, or request the flavour it was built for (for example `gpu:A40:1`) |
| Job rejected at submission because of the `--gres` request | Check the flavour spelling (`A40`, `RTX`) and the format `gpu:<flavour>:<number>`. Your partition must also have that flavour: `brighton` only has `RTX` |
| `CUDA out of memory` | The problem does not fit in GPU memory. Reduce the batch or matrix size |
| `module: command not found` or module conflicts | `module purge`, then load one consistent set with explicit versions |
| Job state `TIMEOUT` | It reached its `--time` limit. Test a smaller case to estimate the run time |
| `oom-kill event` | Ran out of *CPU* memory. Increase `--mem` |
| `NODE_FAIL` | Hardware fault, not your script. Resubmit |

<p align="right">(<a href="#top">back to top</a>)</p>

## The exercises

| Exercise | Time | You will |
| --- | --- | --- |
| [GPU Exercises 1]({{ site.baseurl }}{% link exercises/gpu/Exercise1/README.md %}) | 15 min | Submit your first GPU batch job and read what you were given |
| [GPU Exercises 2]({{ site.baseurl }}{% link exercises/gpu/Exercise2/README.md %}) | 25 min | Build a Python environment on the CPU, then run PyTorch on the GPU |
| [GPU Exercises 3]({{ site.baseurl }}{% link exercises/gpu/Exercise3/README.md %}) | 25 min | Find CUDA modules, compile and run CUDA C, and run a GPU benchmark |
| [GPU Exercises 4]({{ site.baseurl }}{% link exercises/gpu/Exercise4/README.md %}) | remaining time | Run your own code, then scale up with a job array |

Example job scripts and code for these exercises are in the `job_scripts/gpu/` folder of this repository. Copy them to your own storage rather than editing them in place. They are also available on the HPC under `/mnt/shared/public/workshops/HPC-Workshop/gpu/`.

## Learn from other centres

- Cambridge CSD3: [Running jobs](https://docs.hpc.cam.ac.uk/hpc/user-guide/batch.html) and [Ampere (A100) GPU nodes](https://docs.hpc.cam.ac.uk/hpc/user-guide/a100.html)
- ARCHER2: [Running jobs](https://docs.archer2.ac.uk/user-guide/scheduler/) and [GPU development platform](https://docs.archer2.ac.uk/user-guide/gpu/)
- [NVIDIA CUDA documentation](https://docs.nvidia.com/cuda/)
- [PyTorch: get started](https://pytorch.org/get-started/locally/)

<p align="right">(<a href="#top">back to top</a>)</p>
