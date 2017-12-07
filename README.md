# Nethereum.Docs
Nethereum documentation

## Contributing guidelines
1. One pull request per document at a time, this way they can be reviewed and edited for corrections.
2. Any code sample, interaction, should be created as a workbook.
3. Any general introduction and when workbooks do not make any sense obviously NOT, for example Azure BaaS interaction, Code generation, Service structure, Getting started with Unity3d, BUT ideally the aim is to have everything in Worbooks and unit tested.

## Workbooks contributionn
1. Any modificactions should be pushed on the Nethereum.Worbooks repository
2. Any new workbooks need to have a unit test associated with it, or changes unit tested before hand.
  For an introduction on unit testing workbooks [Check this blog post](https://medium.com/@juanfranblanco/unit-or-integration-tests-of-xamarin-workbooks-6f206b8483d6)
3. All the workbooks need to be in the same folder and indexed in the index.md file. See previous entry on how to format links.

## Workbooks submodule update
1. To update the workbooks submodule run ```git submodule update --rebase --remote```
