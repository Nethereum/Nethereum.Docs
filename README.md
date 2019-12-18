# Nethereum.Docs
Nethereum documentation

## Contributing guidelines
 One pull request per document at a time, this way they can be reviewed and edited for corrections.

## Setting up a local environment
To visualise the docs in context and to see how they'll look when published, you'll need a local environment.  This will involve a process to build (aka serve) the documents locally and view them via a browser.  These are rough and ready instructions to set up a local mkdocs environment. The instructions were tested against a Windows 10 PC.  Previous versions of mkdocs and related extensions were removed first.

### Prerequisites
**Python must be installed first**.  Preferably 3.7.4, other version may work but are untested.  

### Instructions
Make sure your "Path" environmental variable includes the path to the python install.  If using the windows installer, tick this box during the install process.  If you have had previous versions of python or mkdocs installed you may run into issues.  If in doubt - and if possible, try uninstalling python completely and removing any python paths from your "Path" environmental variable.  Then reinstalling python and mkdocs afresh.

Mkdocs and theme setup (installs markdown and mkdocs)
1. ``` pip install mkdocs-material ```
2. ``` pip install markdown-include ```

Running Mkdocs 
1. in a console, navigate to the Nethereum.Docs directory 
2. ``` mkdocs serve ```
4. open http://127.0.0.1:8000 in your browser
