

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
	rm -rf _build
       
.PHONY : html
html:
	jupyter-book build .
	
.PHONY : html-hub
html-hub:
	jupyter-book config sphinx .
	sphinx-build  . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
	cd _build/html 
	python -m http.server
	@echo "url:https://stat159.datahub.berkeley.edu/user-redirect/proxy/8000/index.html"
	@echo "if error, please check to make sure you are running python >= 3.6 for this particular command"
	