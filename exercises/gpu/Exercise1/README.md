---
title: GPU Exercises 1
permalink: /GPU/Exercise1
nav_order: 13
parent: "GPU Exercises"
grand_parent: "Exercises"
---
<div id="top"></div>

<div align="center">
  <a href="https://universityofsussex-rc.github.io/Workshops/">
    <img src="https://universityofsussex-rc.github.io/Workshops/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GPU Exercises #1</h3>
  <p align="center">
    Your first GPU job: prepare on the CPU, run on the GPU, and read what you were given.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Exercises</summary>
  <ol>
    <li><a href="#prepare-in-a-cpu-session">Prepare in a CPU session</a></li>
    <li><a href="#write-the-job-script">Write the job script</a></li>
    <li><a href="#submit-and-watch">Submit and watch</a></li>
    <li><a href="#read-the-results">Read the results</a></li>
    <li><a href="#job-composer-repair-the-slurm_gpu-template">Job Composer: repair the slurm_gpu template</a></li>
    <li><a href="#extension-what-happens-without-a-gpu-request">Extension: what happens without a GPU request?</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

**Time:** about 15 minutes. Read the [GPU overview]({{ site.baseurl }}{% link exercises/gpu/README.md %}) first, especially *How GPU jobs run in this workshop*.

> **Which partition?** Brighton sessions use `brighton` for everything: interactive (CPU) sessions and GPU jobs. Sussex sessions use `workshops` for interactive sessions. Below, `<CPU_PARTITION>` is the partition for interactive sessions, `<GPU_PARTITION>` is the partition for GPU jobs and `<GPU_FLAVOR>` is the GPU flavour (Brighton: `RTX`). Your instructor will give you these and the `<CUDA_MODULE>`.

## Prepare in a CPU session

There are only 6 GPUs, so you will **not** start an interactive GPU session. Start an ordinary CPU session to get set up.

1. Log in to Artemis (browser shell from Open OnDemand, or SSH).

2. Start an interactive CPU session:

    ```bash
    srun -p <CPU_PARTITION> --pty bash
    ```

3. Make a folder for this workshop and move into it:

    ```bash
    mkdir -p ~/HPC-Workshop/workdir/GPU
    cd ~/HPC-Workshop/workdir/GPU
    ```

    If you completed [Artemis Exercises 1]({{ site.baseurl }}{% link exercises/artemis/Exercise1/README.md %}) you already have `HPC-Workshop/workdir`.

4. Copy the example files for the GPU exercises:

    ```bash
    cp /mnt/shared/public/workshops/HPC-Workshop/gpu/* .
    ls
    ```

5. Find the CUDA modules that are installed. Note the exact name of one, including its version:

    ```bash
    module avail CUDA
    module spider CUDA
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Write the job script

Open `gpu_test.job` in an editor (or the Open OnDemand file editor) and read it:

```bash
#!/bin/bash
#SBATCH --job-name=gpu_test
#SBATCH --partition=<GPU_PARTITION>
#SBATCH --gres=gpu:<GPU_FLAVOR>:1
#SBATCH --time=00:05:00
#SBATCH --output=gpu_test-%j.out

echo "Job $SLURM_JOB_ID on $(hostname) at $(date)"
echo "Submitted from: $SLURM_SUBMIT_DIR"

module purge
module load <CUDA_MODULE>

nvidia-smi
nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv
```

1. Replace `<GPU_PARTITION>`, `<GPU_FLAVOR>` and `<CUDA_MODULE>` with the values for this session. For Brighton the request line becomes `#SBATCH --gres=gpu:RTX:1`.
2. Which line asks Slurm for a GPU? What would happen if you deleted it?
3. Read the `--gres` line as `gpu:<flavour>:<number>`. What does `gpu:1` (no flavour) mean? When would you name the flavour?
4. Why is `--time` set to only 5 minutes?

<p align="right">(<a href="#top">back to top</a>)</p>

## Submit and watch

```bash
sbatch gpu_test.job
squeue --me
```

- Note the job id that `sbatch` prints.
- With only 6 GPUs shared by the room, your job may spend a little time `PENDING` (`PD`). That is normal. Do not resubmit it.
- Check on it about once a minute, no more often.
- When it has finished, look at the accounting record:

    ```bash
    sacct -j <jobid> --format=JobID,JobName,Partition,Elapsed,State,ExitCode
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Read the results

Open the output file `gpu_test-<jobid>.out` (for example `cat gpu_test-12345.out`) and answer:

1. Which compute node did the job run on?
2. Which GPU model did you get, and how much memory does it have?
3. What is the GPU's **compute capability**? Write it down. You will use it in Exercises 2 and 3. (For comparison, an A40 is 8.6. If yours is higher, it is a newer architecture that needs a newer CUDA, and you will see why that matters in Exercise 2.)
4. What CUDA version does `nvidia-smi` report in its header? What does that number mean? (See *CUDA in five minutes* in the overview.)
5. What was the GPU doing when you ran `nvidia-smi`? Look at the memory usage and the utilisation.

Now add two more lines of your own to `gpu_test.job`, **before** the `nvidia-smi` line, that also print the current directory and the number of CPUs your job was given (`$SLURM_CPUS_ON_NODE`). Submit it again and check the output.

<p align="right">(<a href="#top">back to top</a>)</p>

## Job Composer: repair the slurm_gpu template

The Open OnDemand Job Composer has a template with deliberate mistakes in its GPU request, from [Artemis Exercises 2]({{ site.baseurl }}{% link exercises/artemis/Exercise2/README.md %}) (Exercise 14).

1. Create a new job from the template:
   `/mnt/shared/public/workshops/HPC-Workshop/exercise2/templates/slurm_gpu`
2. Find and fix the problems so the job requests **one GPU** in the right partition.
3. Make it print the GPU details, then submit it.
4. Compare your fix with the script you wrote above.

<p align="right">(<a href="#top">back to top</a>)</p>

## Extension: what happens without a GPU request?

1. Copy the script: `cp gpu_test.job no_gpu.job`.
2. Delete the `#SBATCH --gres=...` line and change `--job-name` to `no_gpu`.
3. Submit it and read the output. What does `nvidia-smi` say now?
4. Why does this matter when you run your own code?

## Extension: `gpu:1` or a named flavour?

1. Copy the script again: `cp gpu_test.job any_gpu.job`, and change `--job-name` to `any_gpu`.
2. Change the request to `#SBATCH --gres=gpu:1` (no flavour) and submit it.
3. Compare the GPU name in the output with your first job. On the `brighton` partition they should match, because every GPU there is an RTX. Why might they *not* match on a partition that has more than one flavour?

<p align="right">(<a href="#top">back to top</a>)</p>

## Checkpoint

- I submitted a GPU job with `sbatch`, not an interactive GPU session.
- I know which GPU I was given and its compute capability.
- I can explain why we request one GPU and a short `--time`.

Next: [GPU Exercises 2]({{ site.baseurl }}{% link exercises/gpu/Exercise2/README.md %}).

<p align="right">(<a href="#top">back to top</a>)</p>
