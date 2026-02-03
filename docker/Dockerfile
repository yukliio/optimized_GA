# AutoGrow4 Dockerfile - uses Python 3.8 env for rdkit (do not install rdkit in base)
# Get the base image from ubuntu (20.04+ needed: Miniconda requires GLIBC >= 2.28)
FROM ubuntu:20.04

LABEL maintainer="Jacob Durrant <durrantj@pitt.edu>"

ENV DEBIAN_FRONTEND=noninteractive

# Install programs through apt-get
RUN apt-get -yqq update
RUN apt-get -fyqq install
RUN apt-get -yqq install wget
RUN apt-get -yqq update
RUN apt-get -yqq install openbabel
RUN apt-get -yqq install zip
# RUN apt-get -yqq install git

# Install python
RUN apt-get -yqq install bzip2
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN chmod -R a+rwx Miniconda3-latest-Linux-x86_64.sh
RUN ./Miniconda3-latest-Linux-x86_64.sh -b
RUN rm ./Miniconda3-latest-Linux-x86_64.sh
RUN echo "alias python=/root/miniconda3/bin/python" >> /root/.bashrc
RUN echo "alias conda=/root/miniconda3/bin/conda" >> /root/.bashrc
RUN echo "alias pip=/root/miniconda3/bin/pip" >> /root/.bashrc

# Accept Anaconda Terms of Service (required by recent Miniconda for default channels)
RUN /root/miniconda3/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    /root/miniconda3/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# rdkit 2020.03.1 requires Python <3.9; Miniconda-latest ships Python 3.13. Create env with Python 3.8.
RUN /root/miniconda3/bin/conda create -n autogrow python=3.8 -y

# Get python dependencies in the autogrow env
RUN /root/miniconda3/bin/conda install -n autogrow -y -c conda-forge rdkit=2020.03.1
RUN /root/miniconda3/bin/conda install -n autogrow -y numpy=1.18.1 scipy=1.4.1
RUN /root/miniconda3/envs/autogrow/bin/pip install matplotlib==3.2.1 func_timeout==4.3.5

# Use autogrow env by default (rdkit-compatible Python 3.8)
ENV PATH="/root/miniconda3/envs/autogrow/bin:$PATH"

# Install mgltools (use current Scripps URL; old mgltools.scripps.edu returns HTML)
RUN wget -q -O mgltools_x86_64Linux2_1.5.6.tar.gz "https://ccsb.scripps.edu/mgltools/download/495/" \
    && tar xvfz mgltools_x86_64Linux2_1.5.6.tar.gz \
    && rm mgltools_x86_64Linux2_1.5.6.tar.gz
RUN cd /mgltool*/ && \
    ./install.sh
# RUN echo "alias python=/mgltools*/bin/pythonsh" >> /root/.bashrc

# Copy over autogrow files
RUN mkdir /autogrow4/
ADD ./autogrow4 /autogrow4

# Copy over User files for AutoGrow Run
RUN mkdir /UserFiles
ADD ./temp_user_files /UserFiles

# Copy over the autogrow run script
ADD ./run_autogrow_in_container.bash /autogrow/run_autogrow_in_container.bash
RUN chmod -R a+rwx /autogrow/run_autogrow_in_container.bash
ADD ./run_autogrow_in_container_windows.bash /autogrow/run_autogrow_in_container_windows.bash
# Strip CR (Windows line endings) so bash in Linux does not see \r as part of commands
RUN sed -i 's/\r$//' /autogrow/run_autogrow_in_container_windows.bash
RUN chmod -R a+rwx /autogrow/run_autogrow_in_container_windows.bash

# Make directories for mounted host file systems
RUN mkdir /Outputfolder


RUN ls autogrow4
# ENTRYPOINT ["bash", "/autogrow/run_autogrow_in_container.bash"]
ENTRYPOINT ["bash", "/autogrow/run_autogrow_in_container_windows.bash"]


# Windows version. Automatically turned on by autogrow_in_docker.py


# ENTRYPOINT ["bash"]