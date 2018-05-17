echo Linux, Mac ou Windows?
echo Favor editar esse arquivo descomentando o seu caso!
exit 1
#wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O conda.sh
#wget https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe -O conda.sh
#wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O conda.sh
bash conda.sh -u
source ~/.bashrc
conda create --name datascience
source activate datascience
pip install requirements.txt
