# Running the Azure Dev Ops Integration
## Requirements
What you will need from Azure Dev Ops and LeanIX in order to make the connection effective:
- The Azure DevOps access token.
- Name of Azure DevOps organization.
- Name of Azure DevOps project.
- LeanIX token.
- LeanIX domain.

**How To Get Requirements**
This paragraph is separated from the last in order to service both new and experienced users. This paragraph will break down how to go about getting all the requirements needed.

**Azure DevOps access token**
Microsoft has documentation on creating the personal access token needed here: https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page

**Azure DevOps Organization and Project**
While it's assumed that you would know this one, you will need the name of the Azure DevOps organization and project which you are attempting to connect to. For more information on projects within Azure DevOps, the following documentation is pasted here: https://docs.microsoft.com/en-us/azure/devops/organizations/projects/about-projects?view=azure-devops.

**Connecting to LeanIX**
For this script, the work has been done to authenticate with LeanIX. All one would need to do is to plugin the base url which the script is targeting as well as an API token. In order to generate the token, you can visit https://dev.leanix.net/docs/technical-users for more details. As far as the base url, it is reflected in the url of your LeanIX workspace. As an example in https://dev.leanix.net/docs/rest-api#section-check-details-of-the-synchronisation you see for a customer with SSO enabled that the url is customer.leanix.net. For a customer without SSO the base url looks something like demo-eu.leanix.net or demo-us.leanix.net, and is best to be copied from your workspace url when logging into your LeanIX workspace.

**Setting the Environment variables**
On Mac, you can use the export command like so: `export LEANIX_DOMAIN=demo-us.leanix.net`.
On PC, there is documentation on the matter here: https://docs.python.org/3/using/windows.html#configuring-python. Lines 9-13 of pipeline2Ldif.py has the names of the variables needed.

## Usage
If you are located within the root directory of the project, you can call the script as you would any Python script like so:
`python azure-devops/pipeline2Ldif.py`