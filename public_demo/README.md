# FreshWise public demonstration

Prepared by Lan. This deployment package preserves the original Python decision tools and conversation controller. It adds a public navigation shell with Prep plan, AI assistant and Impact views.

## Scope

- No Gemini key is supplied by the host. Each visitor enters a personal key for AI chat only.
- The key is transmitted to the hosting server in that visitor's session, then to Google when a request is made. It is not written to files, added to traces or shared through a global cache. Clear key and conversation removes it from the session.
- Manual planning and Impact require no API key.
- Centre 13, meals 1198, 2306, 2444 and 2664 use labelled historical forecast snapshots for planning week 146. This site does not train a forecast model, ingest live inventory or forecast the current calendar week.
- Preparation and manager-adjustment quantities are calculated by the original FreshWise Python tools. Numerical AI explanations use the original controller's templates and confirmation flow.
- Impact values are the final simulation results reported by the team. Across all meals, unmet orders worsen under the default; both waste and service are shown. No final evaluation was rerun.
- No original CSVs, credentials or virtual environments are included.

## Run

Python 3.12 is recommended.

```sh
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Upload this directory as the repository root or as a dedicated deployment subdirectory, preserving src/, data/ and assets/. Select the repository and branch, set the entrypoint to public_demo/app.py (or app.py for a standalone repository), and choose Python 3.12 in advanced settings. requirements.txt is next to the entrypoint. Do not configure a shared GEMINI_API_KEY. Verify the public app's visibility and test its deployed URL after publishing.

A Streamlit account, acceptance of its terms and GitHub repository access must be completed by the account holder. If the source repository is private, approve only the repository access required for this deployment. This package has not been published until a deployed URL is verified.

## Ownership

Lan: conversation interface, Gemini integration, application adapter, confirmation flow, integration testing and public-deployment packaging. Silvia: forecasting model and tools. Ari: preparation policy and decision tools. Original FreshWise and SALLAS logos are retained.
