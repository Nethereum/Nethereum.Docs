# Nethereum.Docs
Nethereum documentation

## Contributing guidelines
1. One pull request per document at a time, this way they can be reviewed and edited for corrections.
2. Any code sample, interaction, should be created as a workbook.
3. Any general introduction and when workbooks do not make any sense obviously NOT, for example Azure BaaS interaction, Code generation, Service structure, Getting started with Unity3d, BUT ideally the aim is to have everything in Worbooks and unit tested.

## Workbooks contribution
1. Any modificactions should be pushed on the Nethereum.Workbooks repository
2. Any new workbooks need to have a unit test associated with it, or changes unit tested before hand.
  For an introduction on unit testing workbooks [Check this blog post](https://medium.com/@juanfranblanco/unit-or-integration-tests-of-xamarin-workbooks-6f206b8483d6)
3. All the workbooks need to be in the same folder and indexed in the index.md file. See previous entry on how to format links.

## Workbooks submodule update
1. To update the workbooks submodule run ```git submodule update --rebase --remote```

## Setting up a local environment
To visualise the docs in context and to see how they'll look when published, you'll need a local environment.  This will involve a process to build (aka serve) the documents locally and view them via a browser.  These are rough and ready instructions to set up a local mkdocs environment. The instructions were tested against a Windows 10 PC.  Previous versions of mkdocs and related extensions were removed first.

**These steps are ONLY intended to allow you to view the documents - it excludes setup necessary to build and run workbooks.  The install commands may require administrative priveleges.**

Tested against:
* Windows 10
* Python 3.7.4 (``` python --version ```)
* mkdocs-material 4.4.2 (``` pip show mkdocs-material ```)
* mkdocs 1.0.4 (``` pip show mkdocs ```)
* markdown 3.1.1 (``` pip show markdown ```)
* markdown-include 0.5.1 (``` pip show markdown-include ```)
* Firefox 69.0

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