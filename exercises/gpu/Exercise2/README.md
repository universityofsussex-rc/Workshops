---
title: GPU Exercises 2
permalink: /GPU/Exercise2
nav_order: 14
parent: "GPU Exercises"
grand_parent: "Exercises"
---
<div id="top"></div>

<div align="center">
  <a href="https://universityofsussex-rc.github.io/Workshops/">
    <img src="https://universityofsussex-rc.github.io/Workshops/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GPU Exercises #2</h3>
  <p align="center">
    Python on the GPU: build an environment on the CPU, then run PyTorch as a GPU batch job.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Exercises</summary>
  <ol>
    <li><a href="#option-a-use-the-shared-environment">Option A: use the shared environment</a></li>
    <li><a href="#option-b-build-your-own-environment">Option B: build your own environment</a></li>
    <li><a href="#run-the-check-as-a-gpu-job">Run the check as a GPU job</a></li>
    <li><a href="#understand-the-results">Understand the results</a></li>
    <li><a href="#extension-your-own-python-gpu-code">Extension: your own Python GPU code</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

**Time:** about 25 minutes. Do [GPU Exercises 1]({{ site.baseurl }}{% link exercises/gpu/Exercise1/README.md %}) first.

Python is the example here, but everything in this exercise works the same way for other GPU software: **prepare on the CPU, then run on the GPU**.

> **Why prepare on the CPU?** Installing packages needs the internet, which you get in a normal session with `module load proxy/public`. It also takes minutes that would waste a scarce GPU. Do it all in a CPU interactive session first.

Start (or return to) a CPU session in your workshop folder:

```bash
srun -p <CPU_PARTITION> --pty bash
cd ~/HPC-Workshop/workdir/GPU
```

## Option A: use the shared environment

Building PyTorch for 20 people at once is slow for everyone. If your instructor has prepared a shared environment, use it and skip to [Run the check as a GPU job](#run-the-check-as-a-gpu-job).

```bash
module load Anaconda3/2022.10
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate <ENV_PATH>
python -c "import torch; print(torch.__version__, torch.version.cuda)"
```

## Option B: build your own environment

This can take 10 to 20 minutes and downloads a couple of gigabytes, so start it now and read on while it runs.

1. Load Python tools and internet access:

    ```bash
    module purge
    module load Anaconda3/2022.10
    module load proxy/public
    source "$(conda info --base)/etc/profile.d/conda.sh"
    ```

2. Create the environment on **Lustre**, not in your home directory (environments are large):

    ```bash
    ENV_PATH=/mnt/lustre/users/<dep>/<username>/envs/gpu-workshop
    conda create -y -p $ENV_PATH python=3.11 pip
    conda activate $ENV_PATH
    ```

3. Install a CUDA build of PyTorch. **Which build matters, because the GPU flavours are different generations.** The number after `cu` must be no newer than the CUDA version reported by `nvidia-smi` in Exercise 1, *and* the build must contain code for your GPU's architecture. Newer GPUs such as the RTX nodes need a newer build than the A40 does (for compute capability 12.0 you need CUDA 12.8 or newer). For example:

    ```bash
    pip install torch --index-url https://download.pytorch.org/whl/cu128
    ```

    An older build such as `cu121` will install without complaint but may fail on a newer GPU with `no kernel image is available for execution on the device`. See [pytorch.org/get-started](https://pytorch.org/get-started/locally/) for the current command for your CUDA version.


4. Check the install (on the CPU, so `CUDA available` will be `False` here, which is expected):

    ```bash
    python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
    python -c "import torch; print(torch.cuda.get_arch_list())"
    ```

    `torch.version.cuda` should show a version number. If it shows `None`, you installed a CPU-only build. The second command lists the GPU architectures this build contains, such as `sm_86`. **Your GPU's architecture (from Exercise 1, written the same way: 8.6 is `sm_86`) must be in that list.**

> **Tidy up later:** when you have finished with the environment, remove it: `conda env remove -p $ENV_PATH`, then `conda clean --all`.

<p align="right">(<a href="#top">back to top</a>)</p>

## Run the check as a GPU job

1. Look at `gpu_check.py`. It multiplies two square matrices on the CPU, then on the GPU if one is visible, and prints both times.

2. Test it quickly on the CPU, still inside your interactive session, with a small matrix:

    ```bash
    python gpu_check.py --n 1024 --repeats 2
    ```

    It will time the CPU and then tell you no GPU is visible. That is the correct answer here.

3. Open `gpu_check.job`. Replace `<GPU_PARTITION>`, `<GPU_FLAVOR>`, `<CUDA_MODULE>` and `<ENV_PATH>`. Because this depends on the GPU architecture, **name the flavour** (Brighton: `--gres=gpu:RTX:1`). Notice it also starts a **usage log** in the background:

    ```bash
    nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used --format=csv -l 2 > gpu_usage-$SLURM_JOB_ID.csv &
    MON_PID=$!
    python gpu_check.py --n 8192 --repeats 10
    kill $MON_PID
    ```

4. Submit it and watch:

    ```bash
    sbatch gpu_check.job
    squeue --me
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Understand the results

When the job finishes, read `gpu_check-<jobid>.out` and look at the usage log `gpu_usage-<jobid>.csv`.

1. Was CUDA available? Which GPU did PyTorch find? Did the `Build supports` line include your GPU's architecture? If a `WARNING` was printed, the build does not contain code for your GPU: go back to step 3 of Option B.
2. How much faster was the GPU than the CPU (the speed-up)?
3. In the usage log, when did GPU utilisation rise, and how high did it get? What was the GPU doing the rest of the time?
4. Change `--n` in the job script to 512, then 2048, then 16384 (keep runs short) and resubmit. How does the speed-up change? Why do you think small problems benefit less?
5. `CUDA out of memory` means the matrices did not fit in GPU memory. Roughly how large can `n` be for your GPU?

> **Only one submission at a time please:** the 6 GPUs are shared. Wait for a job to finish (or `scancel` it) before submitting the next.

<p align="right">(<a href="#top">back to top</a>)</p>

## Extension: your own Python GPU code

If you have Python code that uses a GPU (PyTorch, TensorFlow, CuPy, Numba, JAX), adapt it:

1. Install what it needs into your environment **in the CPU session**.
2. Test a tiny input on the CPU first, if your code supports it.
3. Copy `gpu_check.job` to `my_python.job`, change the last command to run your script, and keep `--time` short.
4. Add a line to your script that prints whether it found the GPU, so a failure is obvious from the output.

Carry on in [GPU Exercises 4]({{ site.baseurl }}{% link exercises/gpu/Exercise4/README.md %}) for a full checklist.

Next: [GPU Exercises 3]({{ site.baseurl }}{% link exercises/gpu/Exercise3/README.md %}).

<p align="right">(<a href="#top">back to top</a>)</p>
