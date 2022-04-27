

.PHONY : env
env:
	mamba env create -f environment.yml -p ~/envs/ligo
	bash -ic 'conda activate ligo;python -m ipykernel install --user --name ligo --display-name "IPython - ligo"'
        
.PHONY : all
all:
	jupyter execute index.ipynb
        
.PHONY : clean
clean:
	rm -f $(wildcard figures/*.png)
	rm -f $(wildcard audio/*.wav)
       
        