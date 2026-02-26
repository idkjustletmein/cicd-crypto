# CryptoLab Status Setup Instructions

I have prepared the Upptime configuration for your standalone status repository. Because this needs to live in a completely separate GitHub repository from `cicd-crypto`, you need to set it up in your GitHub account. 

Here are the 4 easy steps:

### 1. Create a Repository from the Upptime Template
1. Go to this link: [https://github.com/upptime/upptime/generate](https://github.com/upptime/upptime/generate)
2. Name the repository exactly **`cryptolab-status`**.
3. Make sure to check **"Include all branches"**.
4. Click **"Create repository from template"**.

### 2. Enable GitHub Pages
1. In your new `cryptolab-status` repository, go to **Settings** > **Pages**.
2. Under "Build and deployment" -> "Source", select **GitHub Actions**.
3. (Optional) Let GitHub Actions run. Upptime will automatically build your site.

### 3. Apply This Configuration
Copy the contents of the `.upptimerc.yml` file in this directory and paste it into the `.upptimerc.yml` file in your new `cryptolab-status` repository on GitHub. Commit the changes directly to `master`/`main`.

### 4. Provide GitHub Token
Upptime creates issues when your site goes down and updates code automatically, so it needs a Personal Access Token:
1. Generate a new Personal Access Token in your GitHub developer settings with `repo` and `workflow` scopes.
2. Go to your `cryptolab-status` repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.
3. Name it **`GH_PAT`** and paste the token.

Once you commit the updated `.upptimerc.yml` file, Upptime's GitHub Actions will kick in, check your API, and generate an incredibly beautiful, animated status page that includes your badges, pipeline architecture, and secrets table!
