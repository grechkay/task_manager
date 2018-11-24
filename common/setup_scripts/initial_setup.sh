bash Miniconda3-latest-Linux-x86_64.sh

conda install nb_conda_kernels 
conda install -c conda-forge jupyterlab
conda install matplotlib
pip install taskw

conda env create -f basenv.yml
bash copy_rc.sh

# Add copy scripts to copy .rc files
